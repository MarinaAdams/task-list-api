from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..db import db
from typing import Optional

class Task(db.Model): # Declares model Task, tells SQLAlchemy to map Task to db table
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    goal_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("goal.id"), nullable=True) # Adds foreign key reference to goal.id, each task can be linked to one goal
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks") # Sets up many-to-one-relat*p from task to Goal

    def to_dict(self): # Method, prepares dict of task to JSON in API responses
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
            }
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        
        return task_dict
        
    @classmethod # Method, builds Task obj from dict dats to read JSON-requests
    def from_dict(cls, task_data):
        
        return cls(
            title=task_data["title"], 
            description=task_data["description"], 
            completed_at=task_data.get("completed_at")
            )
            