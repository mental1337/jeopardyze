from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from app.core.config import settings
from app.models.base import Base

# SA_DATABASE_URL = "postgresql://user:password@jeopardyze.xyz:5432/jeopardyze"

engine = sa.create_engine(settings.SQLITE_LOCAL_DSN)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Session Factory

def get_db():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()


### For testing and development

def create_tables():
    print("Creating tables")
    Base.metadata.create_all(bind=engine)
    print("Tables created")


def recreate_users_table():
    """Drop and recreate the users table with the new schema."""
    print("Recreating users table")
    from app.models.user import User
    
    # Drop the existing table
    User.__table__.drop(engine, checkfirst=True)
    
    # Create the new table
    User.__table__.create(engine)
    
    print("Users table has been recreated successfully!")


def recreate_guests_table():
    """Drop and recreate the guests table."""
    print("Recreating guests table")
    from app.models.guest import Guest
    
    # Drop the existing table
    Guest.__table__.drop(engine, checkfirst=True)
    
    # Create the new table
    Guest.__table__.create(engine)
    
    print("Guests table has been recreated successfully!")


def recreate_game_sessions_table():
    """Drop and recreate the game_sessions table."""
    print("Recreating game_sessions table")
    from app.models.game_session import GameSession
    
    # Drop the existing table
    GameSession.__table__.drop(engine, checkfirst=True)
    
    # Create the new table
    GameSession.__table__.create(engine)
    
    print("Game sessions table has been recreated successfully!")


## Run as `python -m app.core.database --action create_tables` or `python -m app.core.database --action recreate_users_table`
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database management script.")
    parser.add_argument(
        "--action",
        choices=["create_tables", "recreate_users_table", "recreate_guests_table", "recreate_game_sessions_table"],
        required=True,
        help="The action to perform: 'create_tables', 'recreate_users_table', 'recreate_guests_table', or 'recreate_game_sessions_table'."
    )
    args = parser.parse_args()

    print(f"Running this file as a script with action: {args.action}")

    if args.action == "create_tables":
        create_tables()
    elif args.action == "recreate_users_table":
        recreate_users_table()
    elif args.action == "recreate_guests_table":
        recreate_guests_table()
    elif args.action == "recreate_game_sessions_table":
        recreate_game_sessions_table()