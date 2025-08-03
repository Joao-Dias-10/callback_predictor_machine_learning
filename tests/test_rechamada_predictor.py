import pytest
import pandas as pd
from src.ml.rechamada_predictor import RechamadaPredictor


@pytest.fixture
def sample_data():
    # Dados fictícios para treino/teste
    data = {
        "tempo_atendimento": [5, 15, 8, 20, 12, 3, 17, 6, 14, 9],
        "qtd_contatos": [1, 3, 2, 4, 3, 1, 2, 1, 4, 2],
        "tipo_solicitacao": [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        "rechamada": [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def predictor():
    features = ["tempo_atendimento", "qtd_contatos", "tipo_solicitacao"]
    target = "rechamada"
    return RechamadaPredictor(features=features, target=target)


def test_train_accuracy(predictor, sample_data):
    acc = predictor.train(sample_data)
    assert 0 <= acc <= 100, "Acurácia deve estar entre 0 e 100"


def test_predict_rechamada(predictor, sample_data):
    predictor.train(sample_data)

    # Simulando dia atual com dois registros
    dia_atual = pd.DataFrame({
        "tempo_atendimento": [18, 4],
        "qtd_contatos": [3, 1],
        "tipo_solicitacao": [1, 0],
        "num_cliente": [1001, 1002]
    })

    df_resultado = predictor.predict(dia_atual)

    # Deve conter apenas clientes previstos como rechamada (previsto == 1)
    assert isinstance(df_resultado, pd.DataFrame)
    assert "num_cliente" in df_resultado.columns
    assert set(df_resultado.columns) == {"num_cliente"}
    assert all(df_resultado["num_cliente"].isin(dia_atual["num_cliente"]))


def test_predict_empty_input(predictor):
    empty_df = pd.DataFrame(columns=["tempo_atendimento", "qtd_contatos", "tipo_solicitacao", "num_cliente"])
    result = predictor.predict(empty_df)
    assert result.empty
    assert list(result.columns) == ["num_cliente"]
