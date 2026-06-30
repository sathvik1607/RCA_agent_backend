from fastapi import FastAPI

from app.api import router as incident_router

app = FastAPI()

app.include_router(incident_router)
