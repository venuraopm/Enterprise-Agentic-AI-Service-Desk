from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class Incident(BaseModel):
    incident_id: str
    title: str
    description: str
    priority : str 
    status: str = "open"
    assigned_to: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
class IncidentCreate(BaseModel):
    title: str
    description: str
    priority: str

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
