from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

SA_DATABASE_URL = "sqlite:///./jeopardy.db"
# SA_DATABASE_URL = "postgresql://mental:TODO@jeopardyze.xyz:5432/jeopardyze"

engine = sa.create_engine(SA_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Session Factory
Base = declarative_base()

def get_db():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()
        
           