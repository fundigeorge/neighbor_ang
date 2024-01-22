import streamlit as st
import pandas as pd
import numpy as np

class Neighbors:
    """This class
    ......
    Attributes
    ---------------
    sitename: str
            The site name for the source transmitter
    transmitter: str
            The source transmitter
    Methods
    ---------
    neighbor_ranking(s_neigh:pd.DataFrame)
        calculate neighbor ranking based on dst12(0.7) and intersection(0.3)
    bi_directional(neighbors:pd.DataFrame)
        get the bi-direction neighbor relations
    get_cellname(neigh_rel:pd.DataFrame)
        lookup the transmitters params(cellname,rnc, cellid, psc, rac, lac) for both source and target
    
    def get_existing_neighbors(cellname:str, db_conn):
        get the existing neighbors and generate script for deleting existing neighbors

    def generate_intrafreq_script(neigh_rel:pd.DataFrame):
        generate the uintrafreq addition script

    """
    def __init__(self,sitename, transmitter) -> None:
        self.sitename = sitename
        self.transmitter = transmitter

    def neighbor_ranking(self, s_neighs:pd.DataFrame):
        #filter out the source site transmitters. captured by co_site relations
        #get transmitter with same sitename and whose distance from source < 50m. the 50m consider sector not at source but
        #they are not far away to be considered ERRU and filter them out negation    
        s_neighs = s_neighs.loc[~(s_neighs['site'].isin([self.sitename])&(s_neighs['dst12'] < 0.050))] #filter site displaced sector or ERRU
        s_neighs = s_neighs.loc[s_neighs['intersection'] != "source point"] #filter out site co-sector
        s_neighs['intersection'] = pd.to_numeric(s_neighs['intersection'])

        #rank the neighbor by weighting intersection and dst12 variables. dst12 weight =0.7 and intersection = 0.3.
        #dst12 carries more weight because it shows a neighbor is near. transimmiter can be far and intersect closely
        s_neighs['neighborhood'] = s_neighs.loc[:, 'dst12'] * 0.7 + s_neighs.loc[:, 'intersection'] * 0.3 

        #ensure the neighborhood columns is numerical
        s_neighs['neighborhood'] = pd.to_numeric(s_neighs['neighborhood'])
        
        #set the top neighbor to select
        top_neighbor = st.number_input(label='Select number of top neighbor', min_value=10, max_value=32)

        #sort the neighbor based on neighborhood and pick top 20
        s_neighs = s_neighs.sort_values(by='neighborhood').nsmallest(n=top_neighbor, columns='neighborhood').reset_index()

        #add the source site and transmitter to the neighbor
        s_neighs['source_site'] = self.sitename
        s_neighs['source_transmitter'] = self.transmitter
        
        #modify the site->target_site and transmitter->target_transmitter
        s_neighs = s_neighs.rename(columns={'site':'target_site', 'transmitter':'target_transmitter'} )
        
        #re-arrange columns
        source_target_col = ['source_site', 'source_transmitter', 'target_site', 'target_transmitter' ]
        st.text_area(label='BEFORE ARRANGED COLUMNS')
        st.dataframe(s_neighs)
        s_neighs = s_neighs[source_target_col]

        #label the ranked neighbors
        s_neighs['rank'] = range(s_neighs.shape[0])    
        
        return s_neighs

    def bi_directional(self, neighbors:pd.DataFrame):
        #get neighbors columns order
        neigh_columns = neighbors.columns
        #create a dataframe with source as target and target as source
        bi_neighbors = neighbors.loc[:, ['target_site', 'target_transmitter', 'source_site', 'source_transmitter', 'rank']]
        #align the bi_neighbors columns to be like neighbors columns
        bi_neighbors.columns = neigh_columns
        #concatenate the two dataframe
        neighbors = pd.concat([neighbors, bi_neighbors], ignore_index=True)

        return neighbors



    def get_cellname(self, neigh_rel:pd.DataFrame, db_conn):
        #define the query to select transmitter
        #get the transmitter in the relations, target_transmitter has all transmitter due to defined bi-direction relations
        transmitters = neigh_rel.loc[:, 'target_transmitter'].drop_duplicates()
        transmitters = tuple(transmitters)
        query = f""" select atoll_transmitter, bsc_name, logical_rnc_id, cell_name, cell_id, psc, lac, rac 
                from umts_cells where atoll_transmitter IN {transmitters}"""
        transmitters_params = pd.read_sql(query, con = db_conn)
        #merge neigh_relation to get the source_transmitter and target_transmitter cell names and other details like, rncid
        #get the source_transmitter details
        neigh_rel = pd.merge(neigh_rel, transmitters_params, how='left', 
                            left_on='source_transmitter', right_on='atoll_transmitter',
                            )
        
        #rename the source transmitter rnc, cellname, cellid as sources
        neigh_rel = neigh_rel.rename(columns={
                                                'bsc_name':'source_bscname',
                                                'logical_rnc_id':'source_rncid',
                                                'cell_id':'source_cellid',
                                                'cell_name':'source_cellname',
                                                })
        
        #for the source transmitter remove psc, rac, lac and merging column(atoll_transmitter) not needed for source Txs
        neigh_rel = neigh_rel.drop(columns=['atoll_transmitter', 'psc', 'lac', 'rac'])
        #get the target transmitter details
        neigh_rel = pd.merge(neigh_rel, transmitters_params, how='left', 
                            left_on='target_transmitter', right_on='atoll_transmitter')
        
        #rename the target transmitter rnc, cellname, cellid, psc .. as target
        neigh_rel = neigh_rel.rename(columns =  {
                                                'bsc_name':'target_bscname',
                                                'logical_rnc_id':'target_rncid',
                                                'cell_id':'target_cellid',
                                                'cell_name':'target_cellname',
                                                'psc':'target_psc',
                                                'lac':'target_lac',
                                                'rac':'target_rac'
                                                })
        #drop the megrging columns
        neigh_rel = neigh_rel.drop(columns=['atoll_transmitter'])
        #convert the rncid, cellid, psc, rac, lac float to integers
        neigh_rel = neigh_rel.convert_dtypes()
        return neigh_rel
    

    def get_existing_neighbors(self, cellname:str, db_conn):
        existing_neighbors_script = pd.DataFrame()
        return existing_neighbors_script

    def generate_intrafreq_script(self, neigh_rel:pd.DataFrame):
        #create the mml command for creating new neighbors
        #iterate through the rows
        for row in neigh_rel.itertuples(index=False):
            neigh_rel['uintrafreq_cmd'] = "ADD UINTRAFREQ RNC =" + str(row.source_rncid) + "SCELLID=" + str(row.source_cellid)
        
        return neigh_rel

def neighbor_ranking(s_neighs:pd.DataFrame, sitename, transmitter):
    #filter out the source site transmitters. captured by co_site relations
    #get transmitter with same sitename and whose distance from source < 50m. the 50m consider sector not at source but
    #they are not far away to be considered ERRU and filter them out negation    
    s_neighs = s_neighs.loc[~(s_neighs['site'].isin([sitename])&(s_neighs['dst12'] < 0.050))] #filter site displaced sector or ERRU
    s_neighs = s_neighs.loc[s_neighs['intersection'] != "source point"] #filter out site co-sector
    s_neighs['intersection'] = pd.to_numeric(s_neighs['intersection'])

    #rank the neighbor by weighting intersection and dst12 variables. dst12 weight =0.7 and intersection = 0.3.
    #dst12 carries more weight because it shows a neighbor is near. transimmiter can be far and intersect closely
    s_neighs['neighborhood'] = s_neighs.loc[:, 'dst12'] * 0.7 + s_neighs.loc[:, 'intersection'] * 0.3 

    #ensure the neighborhood columns is numerical
    s_neighs['neighborhood'] = pd.to_numeric(s_neighs['neighborhood'])
    
    #set the top neighbor to select
    top_neighbor = st.number_input(label='Select number of top neighbor', min_value=10, max_value=32)

    #sort the neighbor based on neighborhood and pick top 20
    s_neighs = s_neighs.sort_values(by='neighborhood').nsmallest(n=top_neighbor, columns='neighborhood').reset_index()

    #add the source site and transmitter to the neighbor
    s_neighs['source_site'] = sitename
    s_neighs['source_transmitter'] = transmitter
    
    #modify the site->target_site and transmitter->target_transmitter
    s_neighs = s_neighs.rename(columns={'site':'target_site', 'transmitter':'target_transmitter'} )
    
    #re-arrange columns
    source_target_col = ['source_site', 'source_transmitter', 'target_site', 'target_transmitter' ]
    st.text_area(label='BEFORE ARRANGED COLUMNS')
    st.dataframe(s_neighs)
    s_neighs = s_neighs[source_target_col]

    #label the ranked neighbors
    s_neighs['rank'] = range(s_neighs.shape[0])    
    
    return s_neighs

def bi_directional(neighbors:pd.DataFrame):
    #get neighbors columns order
    neigh_columns = neighbors.columns
    #create a dataframe with source as target and target as source
    bi_neighbors = neighbors.loc[:, ['target_site', 'target_transmitter', 'source_site', 'source_transmitter', 'rank']]
    #align the bi_neighbors columns to be like neighbors columns
    bi_neighbors.columns = neigh_columns
    #concatenate the two dataframe
    neighbors = pd.concat([neighbors, bi_neighbors], ignore_index=True)

    return neighbors



def get_cellname(neigh_rel:pd.DataFrame, db_conn):
    #define the query to select transmitter
    #get the transmitter in the relations, target_transmitter has all transmitter due to defined bi-direction relations
    transmitters = neigh_rel.loc[:, 'target_transmitter'].drop_duplicates()
    transmitters = tuple(transmitters)
    query = f""" select atoll_transmitter, bsc_name, logical_rnc_id, cell_name, cell_id, psc, lac, rac 
              from umts_cells where atoll_transmitter IN {transmitters}"""
    transmitters_params = pd.read_sql(query, con = db_conn, dtype={'logical_rnc_id':'int64', 'cell_id':'int64'})
    #merge neigh_relation to get the source_transmitter and target_transmitter cell names and other details like, rncid
    #get the source_transmitter details
    print(transmitters_params.dtypes)
    neigh_rel = pd.merge(neigh_rel, transmitters_params, how='left', 
                         left_on='source_transmitter', right_on='atoll_transmitter',
                         )
    
    #rename the source transmitter rnc, cellname, cellid as sources
    neigh_rel = neigh_rel.rename(columns={
                                            'bsc_name':'source_bscname',
                                            'logical_rnc_id':'source_rncid',
                                            'cell_id':'source_cellid',
                                            'cell_name':'source_cellname',
                                            })
    
    #for the source transmitter remove psc, rac, lac and merging column(atoll_transmitter) not needed for source Txs
    neigh_rel = neigh_rel.drop(columns=['atoll_transmitter', 'psc', 'lac', 'rac'])
    #get the target transmitter details
    neigh_rel = pd.merge(neigh_rel, transmitters_params, how='left', 
                         left_on='target_transmitter', right_on='atoll_transmitter')
    
    #rename the target transmitter rnc, cellname, cellid, psc .. as target
    neigh_rel = neigh_rel.rename(columns =  {
                                            'bsc_name':'target_bscname',
                                            'logical_rnc_id':'target_rncid',
                                            'cell_id':'target_cellid',
                                            'cell_name':'target_cellname',
                                            'psc':'target_psc',
                                            'lac':'target_lac',
                                            'rac':'target_rac'
                                            })
    #drop the megrging columns
    neigh_rel = neigh_rel.drop(columns=['atoll_transmitter'])
    #convert the rncid, cellid, psc, rac, lac float to integers
    neigh_rel = neigh_rel.convert_dtypes()
    return neigh_rel
 

def get_existing_neighbors(cellname:str, db_conn):
    existing_neighbors_script = pd.DataFrame()
    return existing_neighbors_script

def generate_intrafreq_script(neigh_rel:pd.DataFrame):
    #create the mml command for creating new neighbors
    #iterate through the rows
    for row in neigh_rel.itertuples(index=False):
        neigh_rel['uintrafreq_cmd'] = "ADD UINTRAFREQ RNC =" + str(row.source_rncid) + "SCELLID=" + str(row.source_cellid)
    
    return neigh_rel