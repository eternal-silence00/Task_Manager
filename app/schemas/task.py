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
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    