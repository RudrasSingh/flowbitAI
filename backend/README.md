# Flowbit Multitenant Application - Backend

## Overview
This backend service is built using FastAPI and is designed to support a multitenant architecture. It includes authentication, role-based access control (RBAC), and secure data isolation for different tenants. The backend interacts with a MongoDB database and integrates with n8n for workflow automation.

## Features
- **Authentication**: Users can log in using email and password. JWT tokens are used for session management, carrying user roles and tenant information.
- **RBAC**: Middleware restricts access to certain routes based on user roles (Admin or User).
- **Tenant Data Isolation**: Each MongoDB collection includes a `customerId` to ensure data is isolated per tenant.
- **Dynamic Use-Case Registry**: Hard-coded use cases are defined in `registry.json`, allowing the application to serve different screens based on the logged-in tenant.
- **Webhook Integration**: The backend can receive webhook calls from n8n to update ticket statuses.

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd flowbit-multitenant-app
   ```

2. **Install Dependencies**
   Navigate to the backend directory and install the required packages:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Copy the `.env.example` to `.env` and update the values as needed.

4. **Run the Application**
   Use Docker Compose to start the application along with MongoDB and other services:
   ```bash
   docker-compose up
   ```

5. **Access the API**
   The API will be available at `http://localhost:8000`. You can use tools like Postman to interact with the endpoints.

## Testing
Unit tests for tenant data isolation can be found in the `tests` directory. Run the tests using:
```bash
pytest tests/
```

## Endpoints
- **Authentication**
  - `POST /api/auth/login`: Login and receive a JWT token.
  
- **Admin Routes**
  - `GET /admin/*`: Restricted to Admin users only.

- **Ticket Management**
  - `POST /api/tickets`: Trigger a workflow in n8n.

- **Webhook**
  - `POST /webhook/ticket-done`: Endpoint for n8n to call back after processing.

## Contribution
Feel free to contribute to this project by submitting issues or pull requests. Ensure to follow the coding standards and include tests for new features.

## License
This project is licensed under the MIT License. See the LICENSE file for details.