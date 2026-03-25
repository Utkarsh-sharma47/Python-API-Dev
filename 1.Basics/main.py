from sqlalchemy import create_engine, text

# Replace with your actual credentials
DATABASE_URL = "postgresql://postgres:qpalzm@localhost:5432/fastapi_sqlalchemy"

engine = create_engine(DATABASE_URL, echo=True)

# Best practice: use a "with" block. It closes the connection automatically!
with engine.connect() as conn:
    # 1. Execute the command (Note the added table name 'users')
    conn.execute(text("CREATE TABLE IF NOT EXISTS users (name VARCHAR, age INT)"))
    
    # 2. Commit the change
    conn.commit()