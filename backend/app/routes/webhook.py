from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from app.db import db
from bson import ObjectId

router = APIRouter()

class WebhookPayload(BaseModel):
    customer_id: str
    status: str
    ticket_id: str

@router.post("/ticket-done")  # Remove duplicate "/webhook"
async def ticket_done(payload: WebhookPayload, request: Request):
    secret_header = request.headers.get("X-Shared-Secret")
    expected_secret = os.getenv("N8N_WEBHOOK_SECRET", "your_n8n_webhook_secret")

    if secret_header != expected_secret:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid secret")

    tickets = db.get_collection("tickets")
    
    try:
        result = tickets.update_one(
            {"_id": ObjectId(payload.ticket_id), "customer_id": payload.customer_id},
            {"$set": {"status": payload.status}}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ticket ID: {str(e)}")
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found for this tenant")

    return JSONResponse(status_code=200, content={"message": "Ticket status updated successfully"})