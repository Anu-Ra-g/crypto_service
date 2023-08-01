from sqlalchemy import Column, Integer, String, text
from sqlalchemy.types import BigInteger, Numeric
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Crypto(Base):
    __tablename__ = "crypto"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    symbol = Column(String)
    total_supply = Column(BigInteger, nullable=True, server_default=text('0'))
    max_supply = Column(BigInteger, nullable=True, server_default=text('0'))
    circulating_supply = Column(BigInteger, nullable=True, server_default=text('0'))
    price = Column(Numeric(scale=20), nullable=True)


