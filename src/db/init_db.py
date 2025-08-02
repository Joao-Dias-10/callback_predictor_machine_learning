from src.db.models import Base
from src.db.connection import DatabaseConnection
from src.utils.config import DATABASE_URL

# Instanciando a classe DatabaseConnection
db_connection = DatabaseConnection(DATABASE_URL)

# Cria as tabelas no banco usando o engine da conexão
Base.metadata.create_all(bind=db_connection.engine)
