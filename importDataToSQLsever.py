import os
import sqlalchemy
from sqlalchemy.orm  import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc
import urllib
from CofactsDataTest.importData import engine as engine_localhost
from CofactsDataTest.importData import Articles
server = "peason-project.database.windows.net"
database = "Cofacts"
username = "peason6759"
if os.getenv("Cofact_db_password") != None:
    password =  os.getenv("Cofact_db_password")
else:
    print("password haven't set in env")

password = '_P5e8a2s5on58'
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
    'charset=utf8mb4;')   
connect_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure_db = sqlalchemy.create_engine(connect_str)

# metadata = sqlalchemy.MetaData()
# articles_table = sqlalchemy.Table('articles', metadata,
#     sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True),
#     sqlalchemy.Column('origin_id', sqlalchemy.String(64), primary_key=True, nullable=False),
#     sqlalchemy.Column('article', sqlalchemy.Text),
#     sqlalchemy.Column('rumor_status', sqlalchemy.Boolean, nullable=False)
# )

Base = declarative_base()

class Articles(Base):
    __tablename__ = "articles"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement=True,nullable = False)
    origin_id = sqlalchemy.Column(sqlalchemy.String(64), primary_key = True, nullable = False)
    article = sqlalchemy.Column(sqlalchemy.UnicodeText(), nullable = True)
    rumor_status = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False)

if __name__ == "__main__":
    
    Base.metadata.drop_all(engine_azure_db)
    Base.metadata.create_all(engine_azure_db) 

    Session_azure_db = sessionmaker()
    Session_azure_db.configure(bind=engine_azure_db)
    session_azure_db = Session_azure_db()

    azure_db_newArticles= []

    stmt = sqlalchemy.select(Articles)

    with engine_localhost.connect() as conn:
        for row in conn.execute(stmt):
            print(row[0])
            if len(azure_db_newArticles) < 500:
                azure_db_newArticles.append(
                    Articles(origin_id = row[1],
                          article = row[2],
                          rumor_status = row[3]))
            else:
                try:
                    session_azure_db.bulk_save_objects(azure_db_newArticles)
                    session_azure_db.commit()
                    azure_db_newArticles= []
                except:  
                    session_azure_db.rollback()  
                    print(f"Error while trying to commit")
    
    
    