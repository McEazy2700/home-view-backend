from sqlmodel import create_engine

from core.settings import DB_URL


DB_ENGINE = create_engine(DB_URL, echo=True)
