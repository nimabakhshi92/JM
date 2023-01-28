import pandas as pd
import mysql.connector

# conn = mysql.connector.connect(host='localhost', database='JM', user='root', password='newpassword')
df = pd.read_csv('./quran clean.csv')
df = df.loc[0:6235,]
#
# df.to_sql(con=conn, name='QuranVerseC', if_exists='replace', schema='JM')

import sqlalchemy

database_username = 'root'
database_password = 'newpassword'
database_ip = ''
database_name = 'JM'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password,
                                                      database_ip, database_name))
df.to_sql(con=database_connection, name='QuranVerse', if_exists='append', index=False)
