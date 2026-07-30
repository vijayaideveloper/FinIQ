from app.utils.database import Base
from sqlalchemy import Column,Integer,String,Float


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)



class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    title = Column(String)
    amount = Column(Float)

class Expense(Base):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    title = Column(String)
    amount = Column(Float)