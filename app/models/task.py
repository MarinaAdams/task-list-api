from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..db import db
from typing import Optional

class Task(db.Model): 
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    goal_id: Mapped[Optional[int]] = mapped_column(db.ForeignKey("goal.id"), nullable=True) 
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks") 

    def to_dict(self): 
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
            }
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        
        return task_dict
        
    @classmethod 
    def from_dict(cls, task_data):
        
        return cls(
            title=task_data["title"], 
            description=task_data["description"], 
            completed_at=task_data.get("completed_at")
            )
            