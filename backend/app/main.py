from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import admin, tickets, webhook, me
from app import auth

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
app.include_router(me.router, prefix="/me", tags=["me"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flowbit Multitenant App API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}