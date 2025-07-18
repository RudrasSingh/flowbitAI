from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.db import db
from app.models import User
from passlib.context import CryptContext
from jose import JWTError, jwt
import os

router = APIRouter()

# Constants
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Request/Response Models
class UserCreate(BaseModel):
    email: str
    password: str
    customer_id: str
    role: str = "User"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Utility Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        customer_id: str = payload.get("customer_id")  # Get from JWT
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    users = db.get_collection("users")
    user = users.find_one({"email": email})
    if user is None:
        raise credentials_exception
    
    # Convert ObjectId to string
    user["id"] = str(user["_id"])
    del user["_id"]
    
    return User(**user)

# Routes
@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    users = db.get_collection("users")
    user = users.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Include customer_id and role in JWT payload
    access_token = create_access_token(
        data={
            "sub": user["email"], 
            "customer_id": user["customer_id"],
            "role": user["role"]
        }, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(user_data: UserCreate):
    users = db.get_collection("users")
    
    # Check if user already exists
    if users.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_data.password)
    user_doc = {
        "email": user_data.email,
        "hashed_password": hashed_password,
        "customer_id": user_data.customer_id,
        "role": user_data.role,
        "created_at": datetime.utcnow()
    }
    
    result = users.insert_one(user_doc)
    
    # Return user without sensitive data
    response_user = {
        "id": str(result.inserted_id),
        "email": user_doc["email"],
        "customer_id": user_doc["customer_id"],
        "role": user_doc["role"],
        "created_at": user_doc["created_at"]
    }
    
    return {"message": "User created successfully", "user": response_user}