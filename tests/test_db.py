import pytest
import pandas as pd
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, Chamada, CallbackScore72h
from src.db.queries import ChamadaDB


@pytest.fixture
def session():
    """Cria uma sessão de banco em memória com tabelas"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def test_get_call_history(session):
    # Preenche o banco com chamadas antigas e recentes
    ontem = date.today() - timedelta(days=1)
    um_ano_e_meio = date.today() - timedelta(days=540)

    chamadas = [
        Chamada(num_cliente="1", data=ontem),
        Chamada(num_cliente="2", data=um_ano_e_meio),
    ]
    session.add_all(chamadas)
    session.commit()

    db = ChamadaDB(session)
    historico = db.get_call_history()

    # Apenas a chamada recente deve estar no resultado
    assert len(historico) == 1
    assert historico[0].num_cliente == "1"


def test_insert_callback_score(session):
    df = pd.DataFrame({
        "num_cliente": ["10", "20", "30"]
    })
    dia = date(2025, 8, 1)

    db = ChamadaDB(session)
    db.insert_callback_score(df, dia)

    # Verifica se as linhas foram inseridas corretamente
    resultados = session.query(CallbackScore72h).all()
    assert len(resultados) == 3
    for item in resultados:
        assert item.data == dia
        assert item.num_cliente in ["10", "20", "30"]
