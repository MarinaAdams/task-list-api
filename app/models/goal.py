from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Goal(db.Model): # Declares model Coal, inherits from db.Model, tells SQLAlchemy to map Goal to db table
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    tasks: Mapped[List["Task"]] = relationship(back_populates="goal") # Task relathionships, tells Goal has many Tasks, sets up one-many-relat*p, connects goal attr in Task to make it 2-way-relat*p
    
    def to_dict(self): # Transforms Goal to dict to return in API responses
        return {"id": self.id, "title": self.title}

    @classmethod # Creates Goal from dict data to read JSON-requests
    def from_dict(cls, data):
        return cls(title=data["title"])
