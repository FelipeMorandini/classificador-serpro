from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from database.database_config import Base


class Candidato(Base):
    __tablename__ = 'candidato'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # New ID field
    inscricao = Column(Integer, unique=True)
    tipo = Column(Integer)
    nome = Column(String)
    nota_p1 = Column(Float)
    nota_p2 = Column(Float)
    nota_p3 = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())