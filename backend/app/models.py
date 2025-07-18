from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MongoBaseModel(BaseModel):
    class Config:
        validate_by_name = True
        populate_by_name = True
        arbitrary_types_allowed = True

class User(MongoBaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: str
    hashed_password: str
    customer_id: str
    role: str = "User"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserResponse(BaseModel):
    """User model without sensitive data"""
    id: str
    email: str
    customer_id: str
    role: str
    created_at: datetime

class Ticket(MongoBaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str
    status: str = "Open"
    customer_id: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TicketResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    customer_id: str
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class UseCase(MongoBaseModel):
    tenant: str
    screen_url: str

class Screen(MongoBaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    tenant: str
    url: str