from neo4j import GraphDatabase
import pandas as pd
import neo4j

#define url
url= "neo4j://localhost:7687"
user = "neo4j"
password = "csfbgraph"
driver = GraphDatabase.driver(url, auth=(user, password))
driver.verify_connectivity()


class UmtsTransmitterGraph:
    def __init__(self, umts_transmitter, database) -> None:
        self.transmitter = umts_transmitter
        self.database =  database
        

    #get movies acted by a particular person
    def get_movies(self):          
        #define unit of work
        def actor_movies_tx(tx, name):
            #query
            query = "match (tom:Person{name:$name})-[movie_acted:ACTED_IN]->(movie:Movie) return tom, movie_acted, movie"
            #transaction: unit of work
            results = tx.run(query, name=name)
            keys = results.keys() #return a tuple of flatten out node, rel, properties
            #parse to a df, consume the results
            results = pd.DataFrame(results.to_df(expand=True))
            #columns to drop like element_id columns
            columns_to_drop = []
            for key in keys:
                #construct str of columns to drop
                node_element_id = key + "().element_id"
                columns_to_drop.append(node_element_id)
                rel_element_id = key + "->.element_id"
                columns_to_drop.append(rel_element_id)
                rel_start_element_id = key + "->.start.element_id"
                columns_to_drop.append(rel_start_element_id)
                rel_end_element_id = key + "->.end.element_id"
                columns_to_drop.append(rel_end_element_id)

            for c in columns_to_drop:
                try:
                    results = results.drop(columns=[c])
                except KeyError as err:
                    pass
        
            #format the columns name to remove char i.e "()", ".", "prop"
            results.columns = results.columns.str.replace("()", "_").str.replace(".","").str.replace("->","_").str.replace("prop","")
            #remove "()" from labels
            #results["tom_labels"] = results.loc[:, "tom_labels"].apply(lambda x: str(x).replace("(", "").replace(")", ""))
        
            return results

        with driver.session(database=self.database) as session:
            results= session.execute_read(get_movies, name=self.transmitter)
        return results

query = "match (tom:Person{name:$name})-[movie_acted:ACTED_IN]->(movie:Movie) return tom, movie_acted, movie"
#a unit of work:transaction
def get_movies(tx, name):
    #run the transaction
    results = tx.run(query, name=name)
    keys = results.keys() #return a tuple of flatten out node, rel, properties
    #parse to a df, consume the results
    results = pd.DataFrame(results.to_df(expand=True))
    #columns to drop like element_id columns
    columns_to_drop = []
    for key in keys:
        #construct str of columns to drop
        node_element_id = key + "().element_id"
        columns_to_drop.append(node_element_id)
        rel_element_id = key + "->.element_id"
        columns_to_drop.append(rel_element_id)
        rel_start_element_id = key + "->.start.element_id"
        columns_to_drop.append(rel_start_element_id)
        rel_end_element_id = key + "->.end.element_id"
        columns_to_drop.append(rel_end_element_id)

    for c in columns_to_drop:
        try:
            results = results.drop(columns=[c])
        except KeyError as err:
            pass
    
    #format the columns name to remove char i.e "()", ".", "prop"
    results.columns = results.columns.str.replace("()", "_").str.replace(".","").str.replace("->","_").str.replace("prop","")
    #remove "()" from labels
    #results["tom_labels"] = results.loc[:, "tom_labels"].apply(lambda x: str(x).replace("(", "").replace(")", ""))
    
    return results

with driver.session(database="moviegraph") as session:
    results= session.execute_read(get_movies, name="Tom Hanks")
    #session.run("",).keys()

# print(results.iloc[:, 0:])
# results["tom_labels"] = results.loc[:, "tom_labels"].apply(lambda x: str(x).replace("frozenset({'", "").replace("'})", ""))
# print(results.dtypes)
# print(results.iloc[:, 0:5])
# print(results.dtypes)
#print(driver.execute_query(query, name="Tom Hanks", database_="movieGraph", result_transformer_=lambda res: res.to_df(True)))