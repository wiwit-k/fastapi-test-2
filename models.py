from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base, engine

# Step 2 ORM Class
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)