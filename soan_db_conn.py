import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

"""
mssql-server is not support on ubuntu 22.04, therefore, create a mssql-server docker container. the mssql-server can be
accessed from within container or outside container(from host environment) using sqlcmd or vscode or python using drivers
"""
#disable pooling to ensure pyodbc server is deactivated after sqlalchemy engine is disposed
pyodbc.pooling = False
#
#
#connection credential
driver = "ODBC Driver 18 for SQL Server"
server = "localhost"
username = "SA"
pwd = "Preston#1234"
db = "sites"

#create the connection string
connection_string = "DRIVER={" + driver + "};SERVER=" + server + ";TrustServerCertificate=yes;DATABASE=" + db+ ";UID=" + username + ";PWD=" + pwd
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

#create connections using both pyodbc and sqlalchemy
connection_db = pyodbc.connect(connection_string)
conn_db  = engine.connect()

#create cursor for both pyodbc
cursor = connection_db.cursor()



# df = pd.read_sql_table("gikomba_sites", conn_sqlalchemy)
# print(df)
# df = pd.read_sql_query("select * from gikomba_sites", conn_sqlalchemy)
# print(df)


# #read table
# # r = cursor.execute("select * from UmtsTransmitter").fetchall()
# df = pd.read_sql("select * from umts_transmitter", connection_db)
# #print(df)
# #modify data on db
# # update_query = "UPDATE UmtsTransmitter set bearing=bearing+20"
# # cursor.execute(update_query)
# # cursor.commit()


# df = pd.read_sql_table("umts_transmitter", conn_db)
# #print(df)
# df = pd.read_sql("select top 3 * from umts_transmitter where height >10 and azimuth =20 or azimuth= 120", connection_db)
# #print(df)
# lat = -1.26123
# lon = 36.798874
# grid = [[-1.26123, 36.798874 ], [-1.2613, 36.798]]
# df = pd.read_sql(f"select top 3 * from umts_transmitter where latitude = {lat}", conn_db)
# print(df, f'the value of lat is {lat}')
# df = pd.read_sql(f"select top 3 * from umts_transmitter where latitude > {grid[0][0]}", conn_db)
# print(df, f'the value of lat is {lat}')

