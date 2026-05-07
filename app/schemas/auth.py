from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        from_attributes = True
        
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        from_attributes = True