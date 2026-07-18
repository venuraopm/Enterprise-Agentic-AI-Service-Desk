from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(
    title="Enterprise AI Service Desk",
    description="Enterprise AI Service Desk powered by Agentic AI",
    version="1.0.0",

)

app.include_router(health_router)


@app.get("/")
def home():

    return {

        "message":"Welcome to Enterprise AI Service Desk"

    }

