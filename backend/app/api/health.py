'''
Health Check API
==================

Why do we need a Health API?

Every enterprise application exposes a health endpoint.

It is used by:

Azure App Service
Kubernetes
Docker
Azure Load Balancer
DevOps Pipelines
Monitoring Tools

This endpoint tells whether the application is alive and ready to serve requests

'''

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    """
    Health Check API

    Returns:
        dict: Application health status.
    """
    return {
        "status": "Healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }