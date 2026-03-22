from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Provide your connection details
# Format: postgresql://USER:PASSWORD@HOST/DATABASE_NAME
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qpalzm@localhost/fastapi test1"

# 2. The engine handles the actual communication
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. SessionLocal is a class used to create a "bank teller" for every request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base is what our database classes will inherit from
Base = declarative_base()

# 5. This helper function opens/closes the DB connection for every API call
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()