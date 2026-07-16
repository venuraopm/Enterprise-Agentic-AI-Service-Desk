from fastapi import FastAPI

app = FastAPI(
    title="AI Service Desk",
    version="1.0"
)

@app.get("/")
def home():

    return {

        "message":"AI Service Desk Running"

    }


@app.post("/incident")
def create_incident(issue:str):

    return {

        "ticket_id":"INC000001",

        "issue":issue,

        "status":"Open"

    }