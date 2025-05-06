from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from app.core.config import settings
from app.models.base import Base

# SA_DATABASE_URL = "postgresql://user:password@jeopardyze.xyz:5432/jeopardyze"

engine = sa.create_engine(settings.SQLITE_LOCAL_DSN)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Session Factory

def create_tables():
    print("Creating tables")
    Base.metadata.create_all(bind=engine)
    print("Tables created")
def get_db():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()
        