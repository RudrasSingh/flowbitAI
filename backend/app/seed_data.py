from app.db import db
from app.auth import get_password_hash
from datetime import datetime

def seed_data():
    """Seed initial data for testing"""
    users_collection = db.get_collection("users")
    tickets_collection = db.get_collection("tickets")
    
    # Clear existing data
    users_collection.delete_many({})
    tickets_collection.delete_many({})
    
    # Create test users
    test_users = [
        {
            "email": "admin@tenantA.com",
            "hashed_password": get_password_hash("password"),
            "customer_id": "TenantA",
            "role": "Admin",
            "created_at": datetime.utcnow()
        },
        {
            "email": "user@tenantA.com", 
            "hashed_password": get_password_hash("password"),
            "customer_id": "TenantA",
            "role": "User",
            "created_at": datetime.utcnow()
        },
        {
            "email": "admin@tenantB.com",
            "hashed_password": get_password_hash("password"),
            "customer_id": "TenantB", 
            "role": "Admin",
            "created_at": datetime.utcnow()
        },
        {
            "email": "user@tenantB.com",
            "hashed_password": get_password_hash("password"),
            "customer_id": "TenantB",
            "role": "User", 
            "created_at": datetime.utcnow()
        }
    ]
    
    users_collection.insert_many(test_users)
    
    # Create test tickets
    test_tickets = [
        {
            "title": "TenantA Issue 1",
            "description": "First issue for Tenant A",
            "status": "Open",
            "customer_id": "TenantA",
            "created_by": "user@tenantA.com",
            "created_at": datetime.utcnow(),
            "updated_at": None
        },
        {
            "title": "TenantA Issue 2", 
            "description": "Second issue for Tenant A",
            "status": "In Progress",
            "customer_id": "TenantA",
            "created_by": "user@tenantA.com",
            "created_at": datetime.utcnow(),
            "updated_at": None
        },
        {
            "title": "TenantB Issue 1",
            "description": "First issue for Tenant B", 
            "status": "Open",
            "customer_id": "TenantB",
            "created_by": "user@tenantB.com",
            "created_at": datetime.utcnow(),
            "updated_at": None
        }
    ]
    
    tickets_collection.insert_many(test_tickets)
    print("✅ Seed data inserted successfully!")

if __name__ == "__main__":
    seed_data()