import databases
import sqlalchemy

DATABASE_URL = "mysql+pymysql://admin:Sire!@207.148.22.117:3306/Sire"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={}
)
