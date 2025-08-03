import os
import logging
import pytest
from src.utils.logger import LoggerConfig

@pytest.fixture
def temp_log_dir(tmp_path):
    return tmp_path / "logs"

def test_logger_creation(temp_log_dir):
    # Configura o logger
    logger_config = LoggerConfig(
        log_path=str(temp_log_dir),
        log_filename='teste_execucao.log',
        log_level='INFO',
        logger_name='test_logger'
    )
    logger = logger_config.configure()

    # Valida se o logger foi configurado corretamente
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'test_logger'
    assert logger.level == logging.INFO

    # Testa se log é realmente escrito no arquivo
    logger.info("Teste de log de informação")
    log_file = temp_log_dir / 'teste_execucao.log'
    assert log_file.exists()

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Teste de log de informação" in content
