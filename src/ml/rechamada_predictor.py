import pandas as pd
from typing import List
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class RechamadaPredictor:
    def __init__(self, features: List[str], target: str) -> None:
        """
        Inicializa o preditor com as colunas de entrada (features)
        e o nome da coluna de destino (target).
        """
        self.features = features
        self.target = target
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def treinar(self, df_historico: pd.DataFrame) -> float:
        """
        Treina o modelo usando os dados históricos.

        Parâmetros:
            df_historico (pd.DataFrame): DataFrame com os dados históricos de chamadas.

        Retorno:
            float: Acurácia do modelo em percentual.
        """
        # Separa variáveis preditoras e alvo
        X = df_historico[self.features]
        y = df_historico[self.target]

        # Divide em dados de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Treina o modelo
        self.model.fit(X_train, y_train)

        # Avaliação
        y_pred_test = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred_test)

        return acc * 100  # em percentual

    def prever(self, df_dia_atual: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica o modelo ao DataFrame do dia atual e retorna apenas os casos
        previstos como rechamada.

        Parâmetros:
            df_dia_atual (pd.DataFrame): Dados do dia atual a serem previstos.

        Retorno:
            pd.DataFrame: Subconjunto do df contendo apenas os casos previstos como rechamada,
                          com as colunas: id, cliente_id, data_atendimento.
        """
        if df_dia_atual.empty:
            print("[INFO] Nenhum dado encontrado para previsão no dia atual.")
            return pd.DataFrame(columns=["num_cliente"])

        # Copia o DataFrame para não modificar o original
        df_dia = df_dia_atual.copy()

        # Gera previsões
        X_dia = df_dia[self.features]
        y_pred = self.model.predict(X_dia)
        df_dia["previsto_rechamada"] = y_pred

        # Filtra apenas os que foram previstos como rechamada (1)
        df_rechamada = df_dia[df_dia["previsto_rechamada"] == 1]

        # Retorna apenas as colunas solicitadas com nome correto
        return df_rechamada[["num_cliente"]]
