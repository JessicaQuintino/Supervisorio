from datetime import time
from sqlalchemy.engine import interfaces
from sqlalchemy.sql.sqltypes import TIMESTAMP, PickleType
from db import Base
from sqlalchemy import Column,Integer,DateTime

class DadosCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadoclp'
    id = Column(Integer,primary_key=True,autoincrement=True)
    timestamp = Column(DateTime)
    Freq_desejada = Column(Integer)
    Freq_medida = Column(Integer)
    Tensao=Column(Integer)
    Rotacao=Column(Integer)
    Pot_entrada=Column(Integer)
    Corrente=Column(Integer)
    Temp_Estator=Column(Integer)
    Vel_Esteira=Column(Integer)
    Carga=Column(Integer)
    
    def get_attr_printable_list(self):
        return [self.id,
        self.timestamp.strftime('%d/%m/%Y %H:%M:%S.%f'),
        self.Freq_desejada,
        self.Freq_medida,
        self.Tensao,
        self.Rotacao,
        self.Pot_entrada,
        self.Corrente,
        self.Temp_Estator,
        self.Vel_Esteira,
        self.Carga]