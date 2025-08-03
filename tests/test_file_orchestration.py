import pandas as pd
from src.utils.file_orchestration import FileOrchestration

def test_gerar_e_carregar_csv(tmp_path):
    df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})

    # Cria instância com caminho e nome do CSV
    fo = FileOrchestration(str(tmp_path), 'teste.csv')

    # Usa os métodos reais da classe
    fo.generate_csv(df)
    df_lido = fo.read_csv()

    # Verifica se os dados lidos são os mesmos que os salvos
    assert df_lido.equals(df)
