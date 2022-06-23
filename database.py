from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("credentials.txt", 'r') as c_fh:
	username, password = c_fh.readline().strip().split(":")

#SQLALCHEMY_DATABASE_URI = "sqlite:///ackbar.db"
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@ackbar-vm/ackbar?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=False,
    pool_recycle=3600
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
