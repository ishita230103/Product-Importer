from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1 import upload, products, webhooks, progress
from backend.app.db.base import Base, engine
from backend.app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Order matters — progress must be last
app.include_router(upload.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(webhooks.router, prefix="/api/v1")
app.include_router(progress.router, prefix="/api/v1")  # <-- KEEP LAST
