from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseConnection:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(self.database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """Retorna uma sessão do banco de dados como gerador."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
