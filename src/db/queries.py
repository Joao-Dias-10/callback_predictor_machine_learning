from sqlalchemy.orm import Session
import pandas as pd
from src.db.models import Chamada, CallbackScore72h
from datetime import date, timedelta

class ChamadaDB:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_call_history(self):
        """Consulta registros dos últimos 12 meses da tabela chamadas"""
        data_limite = date.today() - timedelta(days=365)
        return (
            self.db.query(Chamada)
            .filter(Chamada.data >= data_limite)
            .all()
        )

    def insert_callback_score(self, df: pd.DataFrame, dia_de_estudo:date):
        """Insere os dados do DataFrame na tabela callback_score_72h"""
        for index, row in df.iterrows():
            nova_entrada = CallbackScore72h(
                num_cliente=str(row['num_cliente']),
                data=dia_de_estudo
            )
            self.db.add(nova_entrada)
        self.db.commit()
