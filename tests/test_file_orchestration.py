import pandas as pd
from src.utils.file_orchestration import FileOrchestration
from datetime import date

def test_gerar_e_carregar_csv(tmp_path):
    df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
    fo = FileOrchestration(tmp_path, 'teste.csv')
    fo.gerar_csv(df)

    df_lido = fo.carregar_csv()
    assert df_lido.equals(df)

def test_preparar_dados_para_modelo(tmp_path):
    dados = {
        'num_cliente': ['1', '2', '3'],
        'data': ['2025-07-29', '2025-07-28', '2025-07-29'],
        'turno': ['manhã', 'tarde', 'noite'],
        'rechamada_72h': [0, 1, 0]
    }
    df = pd.DataFrame(dados)
    fo = FileOrchestration(tmp_path, 'dummy.csv')
    dia = date(2025, 7, 29)

    atual, historico = fo.preparar_dados_para_modelo(dia, df)

    assert all(atual['data'].dt.date == dia)
    assert all(historico['data'].dt.date < dia)
    assert 'num_cliente' in atual.columns
