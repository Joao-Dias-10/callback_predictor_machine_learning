import logging
from src.utils.logger import LoggerConfig
import os

def test_logger_cria_arquivo(tmp_path):
    logger_path = tmp_path / "logs"
    logger_config = LoggerConfig(
        log_path=str(logger_path),
        log_filename="teste.log",
        log_level="INFO",
        logger_name="test_logger"
    )
    logger = logger_config.configurar()

    logger.info("Mensagem de teste")
    log_file = logger_path / "teste.log"

    logger.handlers[0].flush()  # força flush do log

    assert log_file.exists()
    with open(log_file, "r", encoding="utf-8") as f:
        conteudo = f.read()
        assert "Mensagem de teste" in conteudo
