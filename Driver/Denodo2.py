import pyodbc

host = "myhost"
user = "user"
password = "psw"
port = 9999
database_name = "Database"
driver= '{DenodoODBC}'
connection_string = f"Driver={driver};ServerName={host};Port={port};Database={database_name};UID={user};PWD={password}"
query = """
SELECT "Centre Payeur",
       "Facture id",
       substring("Facture id" from 3 FOR 14) as "Facture id2",
       substring("Facture id" from 3 FOR LENGTH("Facture id")-3) as "Facture id3"
FROM "IT".iv_csv_bouygues_facture_conso;
"""
conn = pyodbc.connect(connection_string)
curs = conn.cursor()
curs.execute(query)
data = curs.fetchall()
for row in data:
    print(row)
curs.close()
conn.close()