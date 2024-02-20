from sqlalchemy import Column, Integer, String
from database import Base


class Users(Base):
    __tablename__ = "users"

    name = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    age = Column(Integer)
    recommendations = Column(String)
    zip = Column(String)
