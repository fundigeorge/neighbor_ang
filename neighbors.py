import streamlit as st
import pandas as pd


def neighbor_ranking(s_neighs:pd.DataFrame, sitename, transmitter):
    #filter out the source site transmitters. captured by co_site relations
    #get transmitter with same sitename and whose distance from source < 50m. the 50m consider sector not at source but
    #they are not far away to be considered ERRU and filter them out negation
    print(s_neighs.head(20))
    s_neighs = s_neighs.loc[~(s_neighs['site'].isin([sitename])&(s_neighs['dst12'] < 0.050))] #filter site displaced sector or ERRU
    s_neighs = s_neighs.loc[s_neighs['intersection'] != "source point"] #filter out site co-sector
    s_neighs['intersection'] = pd.to_numeric(s_neighs['intersection'])
    print(s_neighs.head(20))
    #rank the neighbor by weighting intersection and dst12 variables. dst12 weight =0.7 and intersection = 0.3.
    #dst12 carries more weight because it shows a neighbor is near. transimmiter can be far and intersect closely
    s_neighs['neighborhood'] = s_neighs.loc[:, 'dst12'] * 0.7 + s_neighs.loc[:, 'intersection'] * 0.3 
    #ensure the neighborhood columns is numerical
    s_neighs['neighborhood'] = pd.to_numeric(s_neighs['neighborhood'])
    print(s_neighs.head(20))
    #set the top neighbor to select
    top_neighbor = st.number_input(label='Select number of top neighbor', min_value=10, max_value=32)
    #sort the neighbor based on neighborhood and pick top 20
    s_neighs = s_neighs.sort_values(by='neighborhood').nsmallest(n=top_neighbor, columns='neighborhood').reset_index()
    #add the source site and transmitter to the neighbor
    s_neighs['source_site'] = sitename
    s_neighs['source_transmitter'] = transmitter
    print(s_neighs.head(20))
    #modify the site->target_site and transmitter->target_transmitter
    s_neighs = s_neighs.rename(columns={'site':'target_site', 'transmitter':'target_transmitter'} )
    print(s_neighs.head(20))
    #re-arrange columns
    source_target_col = ['source_site', 'source_transmitter', 'target_site', 'target_transmitter' ]
    st.text_area(label='BEFORE ARRANGED COLUMNS')
    st.dataframe(s_neighs)
    s_neighs = s_neighs[source_target_col]
    print(s_neighs.head(20))
    s_neighs['rank'] = range(s_neighs.shape[0])
    print(s_neighs.head(20))
    
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
    query = "select * from transmitter_cellname where transmitter = %s"
    transmitters = tuple(neigh_rel.loc[:,'source_transmitter'].drop_duplicates())
    transmitter_cellname = pd.read_sql(query, con = db_conn, params=('12001_NW_NI20010'))
    #join the neigh_rel table with cellname
    print(transmitter_cellname)
