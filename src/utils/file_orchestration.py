import csv
import pandas as pd
from datetime import date
from typing import Tuple, Union
from sklearn.preprocessing import LabelEncoder


class FileOrchestration:
    def __init__(self, caminho_arquivo: str, nome_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.nome_arquivo = nome_arquivo
        self.caminho_completo = rf'{caminho_arquivo}\{nome_arquivo}'

    def carregar_csv(self)-> pd.DataFrame:
        """Carrega os dados do CSV para um DataFrame do pandas"""
        df = pd.read_csv(self.caminho_completo)
        return df
    
    def gerar_csv(self, dados: Union[pd.DataFrame, list]) -> None:
        """
        Gera o arquivo CSV com os dados fornecidos. 
        Suporta tanto lista de objetos (ORM) quanto DataFrame do pandas.
        """
        with open(self.caminho_completo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)

            if isinstance(dados, pd.DataFrame):
                # Escreve o cabeçalho do DataFrame
                writer.writerow(dados.columns.tolist())
                # Escreve cada linha do DataFrame
                for row in dados.itertuples(index=False):
                    writer.writerow(list(row))

            elif isinstance(dados, list) and dados:
                # Para listas de objetos com __dict__ (como registros ORM)
                header = dados[0].__dict__.keys()
                writer.writerow(header)
                for chamada in dados:
                    writer.writerow([getattr(chamada, col) for col in header])

            else:
                raise ValueError("[ERRO] Nenhum dado válido fornecido para exportar. A função esperava um DataFrame ou uma lista de objetos.")

    def listar_colunas(self, df: pd.DataFrame) -> list[str]:
        """
        Retorna a lista com os nomes das colunas do DataFrame fornecido,
        ignorando colunas internas que começam com underline.
        """
        return [col for col in df.columns if not col.startswith('_')]

    def preparar_dados_para_modelo(self, dia_atual: date, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Pré-processa os dados do DataFrame recebido, retornando:
        - df_dia_atual: dados exatamente do dia informado
        - df_historico: dados anteriores ao dia informado
        """

        # 1. Remove linhas com valores nulos
        df = df.dropna()

        # 2. Converte a coluna 'data' para datetime
        df['data'] = pd.to_datetime(df['data'])
        df['num_cliente'] = df['num_cliente'].astype(str)

        # 3. Colunas que serão tratadas com LabelEncoder
        features = [col for col in df.columns if not col.startswith('_')]

        # 4. Codifica variáveis categóricas (object) com LabelEncoder
        for col in features:
            if df[col].dtype == 'object':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))

        # 5. Filtra os dados do dia informado
        df_dia_atual = df[df['data'].dt.date == dia_atual].copy()

        # 6. Filtra os dados históricos (anteriores à data)
        df_historico = df[df['data'].dt.date < dia_atual].copy()

        return df_dia_atual, df_historico
