from fastapi import APIRouter, Depends, HTTPException
from app.db import db
from app.models import User, UserResponse
from app.auth import get_current_user
from app.rbac import Role, check_role
from bson import ObjectId
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_user)):
    """Get all users for the current tenant (Admin only)"""
    check_role(current_user, Role.Admin)
    
    users = list(db.get_collection("users").find(
        {"customer_id": current_user.customer_id},
        {"hashed_password": 0}  # Exclude password field
    ))
    
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
    
    return users

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    """Delete a user (Admin only, cannot delete self)"""
    check_role(current_user, Role.Admin)
    
    # Prevent admin from deleting themselves
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    users = db.get_collection("users")
    user = users.find_one({"_id": ObjectId(user_id), "customer_id": current_user.customer_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    
    return {"detail": "User deleted successfully"}