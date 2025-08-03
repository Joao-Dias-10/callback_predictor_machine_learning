from unittest.mock import MagicMock
from src.db.queries import ChamadaDB
from datetime import date

def test_inserir_callback_score():
    session_mock = MagicMock()
    db = ChamadaDB(session=session_mock)

    df_fake = MagicMock()
    df_fake.iterrows.return_value = [((0, ), {'num_cliente': '123', 'data': date.today()})]

    db.inserir_callback_score(df_fake, date.today())
    assert session_mock.commit.called
