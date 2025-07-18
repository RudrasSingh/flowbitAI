# Flowbit Multitenant App - React Shell

## Overview
This directory contains the React shell for the Flowbit multitenant application. The React shell serves as the main entry point for users to interact with the application, providing a dynamic interface that loads micro-frontends based on tenant-specific configurations.

## Features
- **Tenant-aware Authentication**: Users can log in using their email and password, with JWT tokens managing authentication and role-based access control (RBAC).
- **Dynamic Micro-Frontend Loading**: The application dynamically loads micro-frontends based on the tenant's configuration, allowing for a customized user experience.
- **Secure API Integration**: The shell communicates with a secure backend API, ensuring strict tenant data isolation.

## Setup Instructions
1. **Install Dependencies**: Navigate to the `frontend/shell` directory and run:
   ```
   npm install
   ```

2. **Run the Application**: Start the development server with:
   ```
   npm start
   ```

3. **Access the Application**: Open your browser and go to `http://localhost:3000` to access the React shell.

## Development
- The main application logic is located in the `src` directory, with key components including:
  - `App.tsx`: The main component that initializes the application.
  - `Sidebar.tsx`: The component responsible for rendering the navigation sidebar.
  - `api.ts`: Contains functions for making API calls to the backend.

## Testing
- Ensure that all components are tested adequately. Use Jest for unit testing and ensure that tenant data isolation is verified.

## Additional Notes
- This application is designed to work seamlessly with the backend services defined in the `docker-compose.yml` file. Ensure that all services are running for full functionality.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.