import pandas as pd
from src.ml.rechamada_predictor import RechamadaPredictor

def test_treinar_e_prever_modelo():
    df = pd.DataFrame({
        'num_contrato': [1, 2, 3], 'num_cliente': ['1', '2', '3'],
        'cd_skill': [101, 102, 103], 'passo_chamada': [1, 2, 1],
        'turno': [0, 1, 2], 'veterano_novato': [1, 0, 1],
        'motivo_script': [0, 1, 1], 'submotivo_script': [2, 3, 2],
        'rechamada_72h': [0, 1, 0]
    })

    features = ['num_contrato', 'num_cliente', 'cd_skill', 'passo_chamada',
                'turno', 'veterano_novato', 'motivo_script', 'submotivo_script']
    target = 'rechamada_72h'

    model = RechamadaPredictor(features, target)
    acc = model.treinar(df)
    previsoes = model.prever(df)

    assert 'rechamada_prevista' in previsoes.columns
    assert 0 <= acc <= 100
    assert all(previsoes['rechamada_prevista'].isin([0, 1]))
