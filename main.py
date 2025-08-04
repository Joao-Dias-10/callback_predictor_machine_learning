from src.utils.logger import LoggerConfig
from src.utils.config import DATABASE_URL, PATH_RAW, PATH_PROCESSED, FEATURES, TARGET
from src.utils.file_orchestration import FileOrchestration

from src.db.connection import DatabaseConnection
from src.db.queries import ChamadaDB
from src.db.models import Base

from src.ml.rechamada_predictor import RechamadaPredictor

from src.preprocessing.preprocessing_pipeline import PreprocessingPipeline

from sqlalchemy import create_engine

from datetime import datetime,  timedelta

def run():
    try:
        # Configuração do Logger
        log_config = LoggerConfig(log_path='./logs', log_filename='execucao.log', log_level='DEBUG', logger_name='app')
        logger = log_config.configure()
        
        logger.info("Processo iniciado. Criar o banco de dados e as tabelas caso não existam.")
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)  

        logger.info("ORM concluído. Obter a sessão diretamente do gerador.")
        db_connection = DatabaseConnection(DATABASE_URL)
        db = next(db_connection.get_session())  

        try:
            logger.info("Consultar todas as chamadas.")
            chamada_db = ChamadaDB(db)  
            chamadas = chamada_db.get_call_history()  

            logger.info("Chamadas consultadas. Gerando o CSV.") 
            csv_orchestration = FileOrchestration(PATH_RAW, 'historico_rechamada.csv') 
            csv_orchestration.generate_csv(chamadas) 

            logger.info("O CSV gerado. Gerando dia... usa ontem se for antes das 2h, senão usa a data de hoje.")
            dia_de_estudo = (datetime.now() - timedelta(days=1)).date() if datetime.now().hour < 2 else datetime.now().date()

            logger.info(f"Dia {dia_de_estudo} gerado. Carregando df da consulta e preparando dados.") 
            df_chamdas = csv_orchestration.read_csv()
            pipeline = PreprocessingPipeline()
            df_dia_atual, df_historico = pipeline.prepare_data_for_model(dia_de_estudo, df_chamdas)

            logger.info("Configurado. Instanciando predictor e treinando para obter acurácia.") 
            predictor = RechamadaPredictor(features=FEATURES, target=TARGET)
            acuracia = predictor.train(df_historico)

            logger.info(f"Acurácia do modelo: {acuracia:.2f}%. Prevendo rechamadas do dia atual") 
            df_rechamadas_previstas = predictor.predict(df_dia_atual)

            logger.info("Previsão finalizada. Gerando csv da mesma para log.")
            csv_orchestration = FileOrchestration(PATH_PROCESSED, 'rechamadas_previstas.csv')
            csv_orchestration.generate_csv(df_rechamadas_previstas)
        
            logger.info("O csv gerado com sucesso. Inserindo o df de previsão no banco Postgres.")
            chamada_db.insert_callback_score(df_rechamadas_previstas, dia_de_estudo)  

            logger.info("Dados inseridos no banco Postgres com sucesso.")
        
        finally:
            db.close()  
            logger.info("Sessão fechada com sucesso.\n\n")
        
    except Exception as e:
        logger.error(f"Erro registrado: {e}\n\n", exc_info=True)

if __name__ == "__main__":
    run()
