from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from src.db.connection import DatabaseConnection
from src.utils.config import DATABASE_URL

# Instanciando a classe DatabaseConnection
db_connection = DatabaseConnection(DATABASE_URL)

# Acessando o 'engine' a partir da instância
engine = db_connection.engine

Base = declarative_base()

class Chamada(Base):
    __tablename__ = 'chamadas'  

    chamada_id = Column(Integer, primary_key=True, autoincrement=True)  
    num_contrato = Column(String(50), index=True)
    num_cliente = Column(String(50))
    cd_skill = Column(String(50)) 
    passo_chamada = Column(Integer)
    turno = Column(String(20))
    veterano_novato = Column(String(20))
    motivo_script = Column(String(100))
    submotivo_script = Column(String(100))
    data = Column(Date)
    rechamada_72h = Column(Boolean)

class CallbackScore72h(Base):
    __tablename__ = 'callback_score_72h'
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(String(50))
    data_atendimento = Column(DateTime)
