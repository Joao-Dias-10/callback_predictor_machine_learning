from src.utils.logger import LoggerConfig
from src.db.connection import DatabaseConnection
from src.db.queries import ChamadaDB
from src.utils.file_orchestration import FileOrchestration
from src.utils.config import DATABASE_URL, PATH_RAW, PATH_PROCESSED
from src.db.models import Base
from sqlalchemy import create_engine

def run():
    try:
        # Configuração do Logger
        log_config = LoggerConfig(log_path='./logs', log_filename='execucao.log', log_level='DEBUG', logger_name='app')
        logger = log_config.configurar()
        
        logger.info("Processo iniciado. Criar o banco de dados e as tabelas caso não existam.")
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)  

        logger.info("ORM concluído. Obter a sessão diretamente do gerador.")
        db_connection = DatabaseConnection(DATABASE_URL)
        db = next(db_connection.get_session())  

        try:
            logger.info("Consultar todas as chamadas.")
            chamada_db = ChamadaDB(db)  
            chamadas = chamada_db.consultar_todas()  

            logger.info("Chamadas consultadas. Gerando o CSV.") 
            gerador_csv = FileOrchestration(PATH_RAW, 'historico_rechamada.csv') 
            gerador_csv.gerar_csv(chamadas) 
        
            logger.info("CSV gerado com sucesso. Gerando o df para processamento.")
            gerador_csv = FileOrchestration(PATH_PROCESSED, 'rechamadas_previstas.csv')
            df = gerador_csv.carregar_csv()
        
            logger.info("O df gerado com sucesso. Inserindo os dados no banco Postgres.")
            chamada_db.inserir_callback_score(df)  

            logger.info("Dados inseridos no banco Postgres com sucesso.")
        
        finally:
            db.close()  
            logger.info("Sessão fechada com sucesso.\n\n")
        
    except Exception as e:
        logger.error(f"Erro registrado: {e}\n\n", exc_info=True)

if __name__ == "__main__":
    run()
