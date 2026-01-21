from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:admin123@localhost:5432/demodb"
)

while True:
    try:
        engine = create_engine(DATABASE_URL, echo=True, future=True)
        conn = engine.connect()
        print("PostgreSQL is ready!")
        conn.close()
        break
    except Exception as e:
        print("PostgreSQL not ready, retrying in 3s...")
        time.sleep(3)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
