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

    def read_csv(self)-> pd.DataFrame:
        """Carrega os dados do CSV para um DataFrame do pandas"""
        df = pd.read_csv(self.caminho_completo)
        return df
    
    def generate_csv(self, dados: Union[pd.DataFrame, list]) -> None:
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

