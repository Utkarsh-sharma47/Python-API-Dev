from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# This line tells the plumber to build the tables based on the blueprints (models)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. READ (Get all students)
@app.get("/students")
def read_students(db: Session = Depends(get_db)):
    # db.query(models.Student) is SQLAlchemy logic to "Select *"
    return db.query(models.Student).all()

# 2. CREATE (Add a student)
@app.post("/students")
def create_student(name: str, course: str, db: Session = Depends(get_db)):
    new_student = models.Student(name=name, course=course)
    db.add(new_student) # Stage the change
    db.commit()        # Save to Postgres
    db.refresh(new_student) # Get the generated ID back
    return new_student