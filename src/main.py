from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuration CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}




@app.get("/users")
def read_root():
    return {"message": "all users"}