from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

# 1. SETUP: The Connection
DATABASE_URL = "postgresql://postgres:qpalzm@localhost:5432/fastapi_sqlalchemy"
engine = create_engine(DATABASE_URL, echo=False) # Set echo=True to see raw SQL

# 2. BLUEPRINT: The Models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    
    # Back-population: This is a Python-only list of posts owned by this user
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Back-population: This lets us do 'post.owner' to get the User object
    owner = relationship("User", back_populates="posts")

# 3. INITIALIZE: Create tables
Base.metadata.create_all(engine)

# 4. SESSION: Create the "Bank Teller" factory
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

try:
    # --- OPERATION: INSERT (Create) ---
    new_user = User(username="utkarsh_dev")
    session.add(new_user)
    session.commit() # Save user first to get an ID
    
    # --- OPERATION: RELATIONSHIP INSERT ---
    post1 = Post(title="My First API", content="Learning FastAPI is fun!", owner=new_user)
    post2 = Post(title="SQLAlchemy Pro", content="ORM is powerful", owner=new_user)
    session.add_all([post1, post2])
    session.commit()

    # --- OPERATION: QUERY & FILTER (Read) ---
    # Fetch one user by username
    user = session.query(User).filter(User.username == "utkarsh_dev").first()
    print(f"User Found: {user.username} with {len(user.posts)} posts")

    # --- OPERATION: UPDATE ---
    post_to_edit = session.query(Post).filter(Post.title == "My First API").first()
    post_to_edit.title = "My Updated API Title"
    session.commit() # Changes are saved to DB

    # --- OPERATION: JOINS ---
    # Get all posts along with the username of the owner
    results = session.query(Post, User).join(User).all()
    for post, user in results:
        print(f"Post: {post.title} | Author: {user.username}")

    # --- OPERATION: DELETE ---
    # We will delete post2
    session.delete(post2)
    session.commit()

except Exception as e:
    print(f"Error: {e}")
    session.rollback() # Undo changes if something crashes
finally:
    session.close() # Close the connection