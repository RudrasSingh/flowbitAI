from fastapi import APIRouter, Depends, HTTPException
from app.db import db
from app.models import Ticket, TicketCreate, TicketUpdate, TicketResponse, User
from app.auth import get_current_user
from app.rbac import Role, check_role
from bson import ObjectId
from datetime import datetime
from typing import List
import os
import requests

router = APIRouter()

def trigger_n8n_workflow(ticket_data):
    # Fixed: Use correct webhook path matching n8n workflow
    n8n_url = os.getenv("N8N_API_URL", "http://n8n:5678/webhook/flowbit-ticket")
    secret = os.getenv("N8N_WEBHOOK_SECRET", "your_n8n_webhook_secret")
    payload = {
        "ticket_id": ticket_data["id"],
        "customer_id": ticket_data["customer_id"],
        "title": ticket_data["title"],
        "description": ticket_data["description"],
        "status": ticket_data["status"],
    }
    headers = {"X-Shared-Secret": secret}
    try:
        response = requests.post(n8n_url, json=payload, headers=headers, timeout=5)
        print(f"N8N workflow triggered: {response.status_code}")
    except Exception as e:
        print(f"Failed to trigger n8n workflow: {e}")

@router.get("/", response_model=List[TicketResponse])
async def get_tickets(current_user: User = Depends(get_current_user)):
    tickets = db.get_collection("tickets")
    ticket_list = list(tickets.find({"customer_id": current_user.customer_id}))
    
    # Convert ObjectId to string
    for ticket in ticket_list:
        ticket["id"] = str(ticket["_id"])
        del ticket["_id"]
    
    return ticket_list

@router.post("/", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, current_user: User = Depends(get_current_user)):
    tickets = db.get_collection("tickets")
    ticket_data = {
        "title": ticket.title,
        "description": ticket.description,
        "status": "Open",
        "customer_id": current_user.customer_id,
        "created_by": current_user.email,
        "created_at": datetime.utcnow(),
        "updated_at": None
    }
    
    result = tickets.insert_one(ticket_data)
    ticket_data["id"] = str(result.inserted_id)
    
    # Fix the syntax error - proper way to delete the key
    if "_id" in ticket_data:
        del ticket_data["_id"]
    
    trigger_n8n_workflow(ticket_data)
    return ticket_data

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str, current_user: User = Depends(get_current_user)):
    tickets = db.get_collection("tickets")
    try:
        ticket = tickets.find_one({
            "_id": ObjectId(ticket_id), 
            "customer_id": current_user.customer_id
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket["id"] = str(ticket["_id"])
    del ticket["_id"]
    return ticket

@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, ticket: TicketUpdate, current_user: User = Depends(get_current_user)):
    tickets = db.get_collection("tickets")
    update_data = ticket.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    try:
        result = tickets.update_one(
            {"_id": ObjectId(ticket_id), "customer_id": current_user.customer_id},
            {"$set": update_data}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    updated_ticket = tickets.find_one({"_id": ObjectId(ticket_id)})
    updated_ticket["id"] = str(updated_ticket["_id"])
    del updated_ticket["_id"]
    return updated_ticket

@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: str, current_user: User = Depends(get_current_user)):
    tickets = db.get_collection("tickets")
    try:
        result = tickets.delete_one({
            "_id": ObjectId(ticket_id), 
            "customer_id": current_user.customer_id
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ticket ID")
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {"detail": "Ticket deleted successfully"}