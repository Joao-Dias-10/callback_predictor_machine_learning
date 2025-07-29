import logging
import os
from typing import Optional

class LoggerConfig:
    def __init__(self, log_path: Optional[str] = './logs', log_filename: str = 'execucao.log', log_level: str = 'INFO',logger_name: str = "app"):
        self.log_path = log_path
        self.log_filename = log_filename
        self.log_level = log_level.upper()
        self.logger_name = logger_name   
        self.logger = logging.getLogger(self.logger_name)

    def configurar(self) -> logging.Logger:
        os.makedirs(self.log_path, exist_ok=True)
        self.logger.setLevel(self.log_level)
        if self.logger.hasHandlers():
            return self.logger
        log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        formatter = logging.Formatter(log_format)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        log_file_path = os.path.join(self.log_path, self.log_filename)
        file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)
        return self.logger