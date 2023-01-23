import mysql.connector
from mysql.connector.constants import ClientFlag
import sqlalchemy

config = {
    'user': 'root',
    'password': 'pi1234',
    'host': '34.155.207.12'
}

# now we establish our connection
config['database'] = 'testdb'  # add new database to config dict
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()
#Fetching : select sql query
query = ("SELECT * FROM barcodes WHERE user = 'gdai'")
# then we execute with every row in our dataframe
cursor.execute(query)
result = cursor.fetchall()
print(result)
