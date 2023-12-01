import streamlit as st
import pandas as pd


def neighbor_ranking(s_neighs:pd.DataFrame, sitename, transmitter):
    #filter out the source site transmitters. captured by co_site relations
    #get transmitter with same sitename and whose distance from source < 50m. the 50m consider sector not at source but
    #they are not far away to be considered ERRU and filter them out negation
    neigh_ranked = s_neighs.loc[~(s_neighs['site'].isin([sitename])&(s_neighs['dst12'] < 0.050))]
    #rank the neighbor by weighting intersection and dst12 variables. dst12 weight =0.7 and intersection = 0.3.
    #dst12 carries more weight because it shows a neighbor is near. transimmiter can be far and intersect closely
    neigh_ranked['neighborhood'] = neigh_ranked.loc[:, 'dst12'] * 0.7 + neigh_ranked.loc[:, 'intersection'] * 0.3 
    #ensure the neighborhood columns is numerical
    neigh_ranked['neighborhood'] = pd.to_numeric(neigh_ranked['neighborhood'])
    #set the top neighbor to select
    top_neighbor = st.number_input(label='Select number of top neighbor', min_value=10, max_value=32)
    #sort the neighbor based on neighborhood and pick top 20
    neigh_ranked = neigh_ranked.sort_values(by='neighborhood').nsmallest(n=top_neighbor, columns='neighborhood').reset_index()
    #add the source site and transmitter to the neighbor
    neigh_ranked['source_site'] = sitename
    neigh_ranked['source_transmitter'] = transmitter
    #modify the site->target_site and transmitter->target_transmitter
    neigh_ranked = neigh_ranked.rename(columns={'site':'target_site', 'transmitter':'target_transmitter'} )
    #re-arrange columns
    source_target_col = ['source_site', 'source_transmitter', 'target_site', 'target_transmitter' ]
    st.text_area(label='BEFORE ARRANGED COLUMNS')
    st.dataframe(neigh_ranked)
    neigh_ranked = neigh_ranked[source_target_col]
    neigh_ranked['rank'] = range(neigh_ranked.shape[0])
    
    return neigh_ranked

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