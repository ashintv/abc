from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: str = ""
    priority: int = 3
    tags: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    tags: Optional[list[str]] = None


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: int
    tags: list[str]
    created_at: datetime
    updated_at: datetime
