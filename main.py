from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import front_desk, finance, housekeeping
from db.database import engine
from models import room, guest, reservation

# Tabloları oluştur
room.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hotel PMS Pro",
    description="Professional Hotel Property Management System",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Rotaları
app.include_router(front_desk.router)
app.include_router(finance.router)
app.include_router(housekeeping.router)

@app.get("/")
async def root():
    return {"message": "Hotel PMS API is running"}

@app.get("/health")
async def health_check():
    return {"status
