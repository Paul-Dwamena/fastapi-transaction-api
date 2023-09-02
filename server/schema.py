from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum
from enum import Enum as PyEnum
import os
from decouple import Config

# Get the absolute path to the .env file
current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current module (db.py)
env_file_path = os.path.join(current_dir, '..', 'env')



config=Config(env_file_path)
database_url = config("DATABASE_URL", default="postgresql://postgres:mypassword@postgres:5432/postgres")


engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TransactionType(str, PyEnum):
    credit = "credit"
    debit = "debit"

class TransactionModel(BaseModel):
    transaction_id:int
    user_id: int
    full_name: str
    transaction_date: datetime
    transaction_amount: float
    transaction_type: TransactionType



class UpdateModel(BaseModel):
    transaction_date: datetime
    transaction_amount: float
    transaction_type: TransactionType




class TransactionCreateModel(BaseModel):
    user_id: int
    full_name: str
    transaction_date: datetime
    transaction_amount: float
    transaction_type: TransactionType




class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    full_name = Column(String)
    transaction_date = Column(DateTime)
    transaction_amount = Column(Float)
    transaction_type = Column(Enum(TransactionType))

   
