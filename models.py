from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class ProductBD(Base):
    __tablename__="produtos"

    id=Column(Integer, primary_key=True, index=True)
    nome=Column(String, nullable=False)
    categoria=Column(String, nullable=False)
    preco=Column(Float, nullable=False)
    disponivel=Column(Boolean, default=True)