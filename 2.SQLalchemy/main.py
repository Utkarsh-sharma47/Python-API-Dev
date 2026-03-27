from sqlalchemy import (
    create_engine, Table, Column, Integer, String, Float,
    MetaData, ForeignKey, select, update, delete, func
)

# ---------------- DATABASE SETUP ----------------

DATABASE_URL = "postgresql://postgres:qpalzm@localhost:5432/fastapi_sqlalchemy"

engine = create_engine(DATABASE_URL, echo=True)
# echo=True → prints SQL queries in terminal

meta = MetaData()
# Stores table schema


# ---------------- TABLE: PEOPLE ----------------

people = Table(
    "people",
    meta,
    Column('id', Integer, primary_key=True),       # Primary key
    Column('name', String, nullable=False),        # Required field
    Column('age', Integer)
)


# ---------------- TABLE: THINGS ----------------

things = Table(
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False),
    Column('value', Float),
    Column('owner', Integer, ForeignKey('people.id'))  # Relation to people table
)

# One person → many things (1-to-many relationship)


# ---------------- CREATE TABLES ----------------

meta.create_all(engine)


# ---------------- CONNECT ----------------

conn = engine.connect()


# ================= INSERT =================

# Single insert
conn.execute(people.insert().values(id=1, name="Utkarsh", age=21))

# Multiple insert
conn.execute(people.insert(), [
    {"id": 2, "name": "Rahul", "age": 22},
    {"id": 3, "name": "Aman", "age": 23}
])

# Insert things (linked using owner)
conn.execute(things.insert(), [
    {"id": 1, "description": "Laptop", "value": 80000, "owner": 1},
    {"id": 2, "description": "Phone", "value": 30000, "owner": 1},
    {"id": 3, "description": "Bike", "value": 100000, "owner": 2}
])

conn.commit()


# ================= SELECT =================

print("\n--- ALL PEOPLE ---")
for row in conn.execute(select(people)):
    print(row)

print("\n--- ALL THINGS ---")
for row in conn.execute(select(things)):
    print(row)


# ================= JOIN =================

print("\n--- JOIN: PEOPLE + THEIR THINGS ---")

result = conn.execute(
    select(people.c.name, things.c.description, things.c.value)
    .join(things, people.c.id == things.c.owner)
)

for row in result:
    print(row)


# ================= GROUP BY + COUNT =================

print("\n--- COUNT ITEMS PER PERSON ---")

result = conn.execute(
    select(
        people.c.name,
        func.count(things.c.id).label("total_items")
    )
    .join(things, people.c.id == things.c.owner)
    .group_by(people.c.name)
)

for row in result:
    print(row)


# ================= GROUP BY + SUM =================

print("\n--- TOTAL VALUE PER PERSON ---")

result = conn.execute(
    select(
        people.c.name,
        func.sum(things.c.value).label("total_value")
    )
    .join(things, people.c.id == things.c.owner)
    .group_by(people.c.name)
)

for row in result:
    print(row)


# ================= GROUP BY + AVG =================

print("\n--- AVERAGE VALUE PER PERSON ---")

result = conn.execute(
    select(
        people.c.name,
        func.avg(things.c.value).label("avg_value")
    )
    .join(things, people.c.id == things.c.owner)
    .group_by(people.c.name)
)

for row in result:
    print(row)


# ================= UPDATE =================

# Update one person
conn.execute(
    update(people)
    .where(people.c.id == 1)
    .values(name="Utkarsh Sharma")
)

# Update multiple things
conn.execute(
    update(things)
    .where(things.c.value < 50000)
    .values(value=50000)
)

conn.commit()


# ================= DELETE =================

# Delete one thing
conn.execute(
    delete(things)
    .where(things.c.id == 2)
)

# Delete people with age > 22
conn.execute(
    delete(people)
    .where(people.c.age > 22)
)

conn.commit()


# ================= FINAL STATE =================

print("\n--- FINAL PEOPLE ---")
for row in conn.execute(select(people)):
    print(row)

print("\n--- FINAL THINGS ---")
for row in conn.execute(select(things)):
    print(row)


# ---------------- CLOSE CONNECTION ----------------

conn.close()