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

# /////////////////////////////////////////////////////////////////////


import pandas as pd
import json
aa  = pd.read_csv('aa.csv')
z  = pd.read_csv('zd.csv')


def merge_x_y(x,y, z):
    x = json.loads(x)
    y = json.loads(y)
    xy = [[x[i], y[i], z] for i in range(len(x))]
    return xy

df = pd.merge(aa,z,how='inner', on='Name')
df['polygon'] = df.apply(lambda row: merge_x_y(row['x'], row['y'], row['z']),axis=1)
df.drop(['x', 'y'], inplace=True, axis=1)
j = df.to_json(orient='records')
with open('a.json', 'w') as f:
    f.write(j)
    # j.dumps(f)

