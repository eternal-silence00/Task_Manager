from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str
    
class TaskResponse(BaseModel):
    id: int
    title: str
    is_active: bool
    status: str
    
    class Config:
        from_attributes = True
        
class TaskPatch(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    is_active: Optional[bool]
    