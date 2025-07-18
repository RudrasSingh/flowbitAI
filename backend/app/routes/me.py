from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.models import User
import json
import os

router = APIRouter()

@router.get("/screens")
async def get_screens(current_user: User = Depends(get_current_user)):
    """Get available screens for the current user's tenant"""
    try:
        registry_path = os.path.join(os.path.dirname(__file__), "..", "registry.json")
        with open(registry_path, "r") as f:
            registry = json.load(f)
        
        # Filter screens by user's customer_id
        screens = [
            {"tenant": uc["tenant"], "screenUrl": uc["screenUrl"]}
            for uc in registry["useCases"]
            if uc["tenant"] == current_user.customer_id
        ]
        
        # If no screens found for tenant, return default
        if not screens:
            screens = [{"tenant": current_user.customer_id, "screenUrl": "/support"}]
        
        return screens
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Registry configuration not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading screens: {str(e)}")

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "customer_id": current_user.customer_id,
        "role": current_user.role,
        "created_at": current_user.created_at
    }