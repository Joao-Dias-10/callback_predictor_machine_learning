import csv
import pandas as pd

class FileOrchestration:
    def __init__(self, caminho_arquivo: str, nome_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.nome_arquivo = nome_arquivo
        self.caminho_completo = rf'{caminho_arquivo}\{nome_arquivo}'

    def gerar_csv(self, chamadas):
        """Gera o arquivo CSV com os dados das chamadas"""
        with open(self.caminho_completo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            
            # Escrever o cabeçalho automaticamente com base nos atributos do objeto 'Chamada'
            if chamadas:
                header = chamadas[0].__dict__.keys()  # Pega os nomes dos atributos do primeiro objeto
                writer.writerow(header)  # Escreve o cabeçalho
            
            # Escrever os dados de cada chamada
            for chamada in chamadas:
                writer.writerow([getattr(chamada, col) for col in header])  # Escreve os valores dos atributos
      

    def carregar_csv(self):
        """Carrega os dados do CSV para um DataFrame do pandas"""
        df = pd.read_csv(self.caminho_completo)

        return df
