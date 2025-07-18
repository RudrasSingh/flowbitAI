# Support Tickets App

This README provides information about the Support Tickets micro-frontend within the Flowbit Multitenant Application.

## Overview

The Support Tickets App is a micro-frontend that allows users to manage support tickets in a tenant-aware manner. It integrates with the main Flowbit application and communicates with the backend API to perform various operations related to support tickets.

## Features

- Tenant-aware authentication and role-based access control (RBAC).
- Dynamic loading of screens based on the logged-in tenant.
- Integration with n8n for workflow automation.
- Real-time updates to the UI based on ticket status changes.

## Setup

To set up the Support Tickets App, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd flowbit-multitenant-app/frontend/support-tickets-app
   ```

2. **Install Dependencies**
   Ensure you have Node.js installed, then run:
   ```bash
   npm install
   ```

3. **Run the Application**
   Start the development server:
   ```bash
   npm start
   ```

4. **Access the Application**
   Open your browser and navigate to `http://localhost:3000` (or the port specified in your configuration).

## Development

- The main entry point for the application is located in `src/index.tsx`.
- The main component is defined in `src/App.tsx`.
- For any changes related to the UI or functionality, modify the respective files in the `src` directory.

## Testing

To run tests for the Support Tickets App, use the following command:
```bash
npm test
```

## Contribution

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.