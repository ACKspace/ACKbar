from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#SQLALCHEMY_DATABASE_URI = "sqlite:///ackbar.db"
with open("../connection.txt", 'r') as c_fh:
	SQLALCHEMY_DATABASE_URI = c_fh.readline().strip()

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_recycle=3600
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
