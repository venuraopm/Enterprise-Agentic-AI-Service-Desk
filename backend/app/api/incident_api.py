from fastapi import APIRouter, HTTPException
from app.models.incident import IncidentCreate, IncidentUpdate
from app.services.incident_service import incident_service

router = APIRouter(
    prefix="/incidents",
    tags=["Incident Management"]
)

@router.post("/")
def create_incident(request: IncidentCreate):
    incident = incident_service.create_incident(
        title=request.title,
        description=request.description,
        priority=request.priority
    )
    return incident


@router.get("/")
def get_all_incidents():
    return incident_service.get_all_incidents()



@router.get("/{incident_id}")
def get_incident(incident_id: str):
    incident = incident_service.get_incident_by_id(incident_id)

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident

print("PUT endpoint registered")

@router.put("/{incident_id}")
def update_incident(incident_id: str, request: IncidentUpdate):
    incident = incident_service.update_incident(
        incident_id=incident_id,
        title=request.title,
        description=request.description,
        priority=request.priority,
        status=request.status,
        assigned_to=request.assigned_to
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident