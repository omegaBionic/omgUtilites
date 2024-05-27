
import jaydebeapi

host = "myhost"
user = "user"
password = "psw"
port = 9999
database_name = "Database"
url = f"jdbc:denodo://{host}:{port}/{database_name};user={user};password={password}"
query = """
SELECT *
FROM "IT".iv_csv_bouygues_facture_conso;
"""
conn = jaydebeapi.connect("com.denodo.vdp.jdbc.Driver", url, jars="C:/Users/jboully/AppData/Roaming/DBeaverData/drivers/remote/drivers/jdbc/8.0/denodo-vdp-jdbcdriver")
curs = conn.cursor()
curs.execute(query)
data = curs.fetchall()
for row in data:
    print(row)
curs.close()
conn.close()