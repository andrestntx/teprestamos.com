from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import mysql.connector

# mysql-python mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>
# mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine('mysql+mysqldb://root:dondepauto@104.198.72.53:3306/dbprestamos')
Base = declarative_base(engine)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
dbsession = Session()
