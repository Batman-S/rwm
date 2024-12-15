# **Remote Waitlist Manager**

This project is a waitlist system designed to efficiently manage restaurant waitlists.

---

## **Setup Instructions**

The project is containerized with Docker to simplify setup and ensure consistency across environments.

### **1. Running the Project**

To start the entire project, including the frontend, backend, and required services (Redis, MongoDB), follow these steps:

1. Ensure you have **Docker** installed.
2. Navigate to the root directory of the project (`rwm`).
3. Run the following command to spin up all services:

   ```bash
   docker-compose up
   ```
   This will:
   - Start the backend API, frontend app, Redis, and MongoDB.
   - Bind the backend to the default Unicorn host string (e.g., `127.0.0.1:8000`).
   - Bind the frontend to the default development port (e.g., `http://localhost:5173`).

4. Access the app at `http://localhost:5173`

### **2. Running Tests**
#### Backend Tests
1. Navigate to the backend folder:
 ```bash
   cd rwm/backend
   ```
2. Run the backend tests
```bash
   pytest
   ```
#### Frontend Tests
1. Navigate to the frontend folder:
 ```bash
   cd rwm/client
   ```
2. Run the backend tests
```bash
   yarn test
   ```

## **Project Architecture Overview**

### **Frontend Architecture**
The frontend is built using **React** with **Recoil** for state management and includes the following key features:

#### 1. **State Management with Recoil**
Recoil is used to manage application-wide state:
- **Party Status**: Tracks the party's current status (`waiting`, `ready`, `checked_in`, `completed`).
- **Conditional Routing**: Based on the party's status, the app dynamically adjusts the user's view, ensuring a consistent experience based on user status across multiple browser sessions.

Recoil was chosen for:
- **Fine-grained Re-renders**: Only components that depend on specific atoms/selectors re-render.

#### 2. **React for Component-Based UI**
React was chosen for the frontend interface primarly for:
- **Reusable Components**
- **Efficient State Updates**
#### 3. **Waitlist Service Layer**
A dedicated service layer abstracts API calls, providing:
- **Separation of Concerns**: Keeps API interaction logic separate from UI components.

#### 4. **Real-time WebSocket Updates**
The frontend listens for updates from the backend using WebSockets, ensuring users receive real-time updates on party status changes.

---

### **Backend Architecture**
The backend is built with **FastAPI**, **Redis**, **MongoDB**.

#### 1. **Redis for High-performance Locking and Caching**
Redis is used for:
- **Distributed Locks**: Ensures that updates to shared resources (e.g., `available_seats`) are atomic and free from race conditions.
- **Storage**: Stores the `available_seats` variable due to the frequent reads/writes per application. 
    * *Note: A more permanent solution would be needed for production. Right now `available_seats` is stored in-memory so this would not be appropriate to release.

#### 2. **MongoDB for Flexible, Scalable, and Atomic Data Storage**
MongoDB is used as the primary database to store waitlist data, including party details (`name`, `party_size`, `user_id`, `status`, `created_at`). It is well-suited for the system because of its:

- **Schema Flexibility**
- **Efficient Querying**
- **Horizontal Scalability**

MongoDB also ensures **atomicity** for its read and write operations, even in multi-document transactions:
- **Atomic Writes**: Updates to individual documents are atomic, ensuring no partial updates occur, even under concurrent requests.
- **Transactions for Complex Operations**: When multiple documents need to be updated together (e.g., adjusting a waitlist entry and associated metadata), MongoDB's multi-document transactions ensure consistency.
- **Avoiding Conflicts**: Built-in locks on a per-document level prevent race conditions during simultaneous read/write requests.


#### 3. **WebSockets for Real-time Updates**
WebSockets push real-time status updates to the frontend, ensuring:
- **Low-latency Communication**: Parties are notified of status changes instantly.
- **Scalability**: WebSocket servers can handle many connections simultaneously.

---
