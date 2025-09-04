from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def init_engine_and_session(database_url: str):
  engine = create_engine(database_url, pool_pre_ping=True)
  SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
  return engine, SessionLocal
