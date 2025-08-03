import pandas as pd
from datetime import date
from typing import Tuple
from sklearn.preprocessing import LabelEncoder


class PreprocessingPipeline:
    """
    Classe responsável por preparar os dados para treinamento e previsão do modelo.
    """

    def prepare_data_for_model(self, dia_atual: date, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Limpa, codifica e separa os dados entre histórico e dia atual.

        Retorna:
            - df_dia_atual: dados do dia da previsão
            - df_historico: dados anteriores para o treinamento
        """
        # Remove nulos
        df = df.dropna()

        # Formata data e cliente
        df['data'] = pd.to_datetime(df['data'])
        df['num_cliente'] = df['num_cliente'].astype(str)

        # Codifica colunas categóricas
        features = [col for col in df.columns if not col.startswith('_')]

        for col in features:
            if df[col].dtype == 'object':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))

        # Divide entre atual e histórico
        df_dia_atual = df[df['data'].dt.date == dia_atual].copy()
        df_historico = df[df['data'].dt.date < dia_atual].copy()

        return df_dia_atual, df_historico
