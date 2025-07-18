from fastapi import HTTPException

class Role:
    Admin = "Admin"
    User = "User"

def check_role(current_user, required_role: str):
    # Handle both dict and User object
    user_role = getattr(current_user, "role", None) or current_user.get("role") if hasattr(current_user, "get") else None
    if user_role != required_role:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    return True