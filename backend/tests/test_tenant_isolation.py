import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import db
from app.auth import create_access_token
from bson import ObjectId
from datetime import datetime

client = TestClient(app)

def create_test_jwt(email, customer_id, role):
    """Create JWT token for testing"""
    return create_access_token({
        "sub": email,
        "customer_id": customer_id,
        "role": role
    })

def test_tenant_isolation_admin_cannot_access_other_tenant_data():
    """Test that Admin from Tenant A cannot read Tenant B's data"""
    # Setup test data
    tickets_collection = db.get_collection("tickets")
    
    # Create ticket for TenantA
    tenant_a_ticket = {
        "title": "TenantA Secret Ticket",
        "description": "This is confidential to TenantA",
        "status": "Open",
        "customer_id": "TenantA",
        "created_by": "user@tenantA.com",
        "created_at": datetime.utcnow(),
        "updated_at": None
    }
    ticket_a_result = tickets_collection.insert_one(tenant_a_ticket)
    ticket_a_id = str(ticket_a_result.inserted_id)
    
    # Create ticket for TenantB  
    tenant_b_ticket = {
        "title": "TenantB Secret Ticket",
        "description": "This is confidential to TenantB",
        "status": "Open", 
        "customer_id": "TenantB",
        "created_by": "user@tenantB.com",
        "created_at": datetime.utcnow(),
        "updated_at": None
    }
    ticket_b_result = tickets_collection.insert_one(tenant_b_ticket)
    ticket_b_id = str(ticket_b_result.inserted_id)

    try:
        # TenantA Admin tries to access TenantB's ticket
        tenant_a_jwt = create_test_jwt("admin@tenantA.com", "TenantA", "Admin")
        headers = {"Authorization": f"Bearer {tenant_a_jwt}"}
        
        # Should return 404 (not found) since ticket belongs to different tenant
        response = client.get(f"/api/tickets/{ticket_b_id}", headers=headers)
        assert response.status_code == 404
        
        # TenantA Admin should be able to access their own ticket
        response = client.get(f"/api/tickets/{ticket_a_id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == "TenantA"
        assert data["title"] == "TenantA Secret Ticket"
        
        # TenantB Admin should only see their own tickets
        tenant_b_jwt = create_test_jwt("admin@tenantB.com", "TenantB", "Admin")
        headers_b = {"Authorization": f"Bearer {tenant_b_jwt}"}
        
        response = client.get("/api/tickets/", headers=headers_b)
        assert response.status_code == 200
        tickets = response.json()
        
        # Verify TenantB only sees their own tickets
        for ticket in tickets:
            assert ticket["customer_id"] == "TenantB"
            
    finally:
        # Cleanup test data
        tickets_collection.delete_one({"_id": ObjectId(ticket_a_id)})
        tickets_collection.delete_one({"_id": ObjectId(ticket_b_id)})

def test_rbac_user_cannot_access_admin_routes():
    """Test that regular User cannot access Admin routes"""
    # Regular user tries to access admin route
    user_jwt = create_test_jwt("user@tenantA.com", "TenantA", "User")
    headers = {"Authorization": f"Bearer {user_jwt}"}
    
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == 403
    
    # Admin should be able to access admin routes
    admin_jwt = create_test_jwt("admin@tenantA.com", "TenantA", "Admin") 
    admin_headers = {"Authorization": f"Bearer {admin_jwt}"}
    
    response = client.get("/admin/users", headers=admin_headers)
    assert response.status_code == 200