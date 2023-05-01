import os 
import sqlalchemy
import urllib
import pyodbc
from CofactsDataTest.importData import Articles
server = "peason-project.database.windows.net"
database = "Cofacts"
username = "peason6759"
password =  os.getenv("Cofact_db_password")
driver = '{ODBC Driver 18 for SQL Server}'
params = urllib.parse.quote_plus(
    'Driver=%s;' % driver +
    'Server=tcp:%s,1433;' % server +
    'Database=%s;' % database +
    'Uid=%s;' % username +
    'Pwd={%s};' % password +
    'Encrypt=yes;' +
    'TrustServerCertificate=no;' +
    'Connection Timeout=30;' + 
    'charset=utf8;')   
connect_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure_db = sqlalchemy.create_engine(connect_str)

stmt = sqlalchemy.select(Articles)
with engine_azure_db.connect() as conn:
     for row in conn.execute(stmt):
          print(row)