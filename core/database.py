from sqlmodel import create_engine


DB_ENGINE = create_engine("sqlite+pysqlite:///db.sqlite3:", echo=True)
