from fastapi import FastAPI
from .db.session import engine, Base
from .api.v1.routes import types

app = FastAPI()

# TEMP: Drop and recreate all tables (for dev only!)
Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

@app.get('/healthcheck', tags=["Health Check"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "API is running"}

app.include_router(types.router)

