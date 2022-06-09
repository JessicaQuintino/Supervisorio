"""
Ojbetos do sqlalchemy core para a relização da conexão e 
operação do Banco de Dados
"""

from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_CONNECTION = 'sqlite:///data\data.db?check_same_thread=False'
engine = create_engine(DB_CONNECTION,echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
