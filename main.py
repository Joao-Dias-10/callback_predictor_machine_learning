from src.utils.logger import LoggerConfig   
from src.utils.config import TESTE

def run():
    try:
        
        log_config = LoggerConfig(log_path='./logs',log_filename='execucao.log',log_level='DEBUG',logger_name='app' )
        logger = log_config.configurar()

        logger.info("Processo iniciado.")

    except Exception as e:
        logger.error(f"Erro registrado: {e}\n\n", exc_info=True)

if __name__ == "__main__":
    run()