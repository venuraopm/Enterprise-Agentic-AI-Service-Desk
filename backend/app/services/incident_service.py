from app.models.incident import Incident

class IncidentService:
    def __init__(self):
        self.incidents = []
        self.counter = 1

    def create_incident(self, title, description, priority):
        incident = Incident(
            incident_id=f"INC-{self.counter:04d}",
            title=title,
            description=description,
            priority=priority
        )

        self.counter += 1
        self.incidents.append(incident)

        return incident

    def get_all_incidents(self):
        return self.incidents

    def get_incident_by_id(self, incident_id):
        for incident in self.incidents:
            if incident.incident_id == incident_id:
                return incident
        return None

    def update_incident(self, incident_id, title=None, description=None, priority=None, status=None, assigned_to=None):
        incident = self.get_incident_by_id(incident_id)
        if not incident:
            return None

        if title is not None:
            incident.title = title
        if description is not None:
            incident.description = description
        if priority is not None:
            incident.priority = priority
        if status is not None:
            incident.status = status
        if assigned_to is not None:
            incident.assigned_to = assigned_to

        return incident

    def delete_incident(self, incident_id):
        incident = self.get_incident_by_id(incident_id)
        if not incident:
            return False

        self.incidents.remove(incident)
        return True
    


incident_service = IncidentService()