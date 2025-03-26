# Task Manager

Task Manager is a Django-based application that allows users to create, assign, and manage tasks efficiently. It provides both a web interface and a REST API for task management.

## Features
- User authentication (Register, Login, Logout)
- Task creation 
- Assign a task to users
- Update task status
- View tasks assigned to a user
- REST API endpoints for task management

---

## **Web Routes (UI)**

| Route | Method | Description |
|--------|--------|-------------|
| `/login/` | GET, POST | User login page |
| `/register/` | GET, POST | User registration page |
| `/logout/` | GET | Logout user and redirect to login |
| `web/tasks/` | GET | Displays tasks created by or assigned to the logged-in user |
| `web/tasks/create/` | GET, POST | GET: Displays the task creation form. POST: Creates a new task.|
| `web/tasks/<task_id>/assign/` | GET, POST | GET: Show available users for assignment. POST: Assigns users to the task.|
| `web/tasks/update_status/<task_id>/` | POST | Update the status of a task |

---

## **API Endpoints**

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `web/api/tasks/` | GET | Fetch all tasks assigned to a specific user (requires `email` query parameter) |
| `web/api/tasks/create/` | POST | Create a new task |
| `web/api/tasks/<task_id>/assign/` | POST | Assign a task to users |

### **API Request & Response Examples**

#### 1️⃣ Create a Task (POST `web/api/tasks/create/`)
##### Request:
```json
{
    "name": "Fix Bug",
    "description": "Resolve issue in login system",
    "task_type": "Bug",
    "assigned_users": [1, 2]  
}
```
##### Response:
```json
{
    "message": "Task created successfully",
    "task_id": 11,
    "task_name": "Fix Bug"
}
```

#### 2️⃣ Assign Users to a Task (POST `/api/tasks/<task_id>/assign/`)
##### Request:
```json
{
    "assigned_users": [3, 4]
}
```
##### Response:
```json
{
    "message": "Users assigned successfully."
}
```

#### 3️⃣ Fetch Tasks for a User (GET `/api/tasks/?email=user@example.com`)
##### Response:
```json
{
    "tasks": [
        {
            "id": 11,
            "name": "Fix Bug",
            "description": "Resolve issue in login system",
            "task_type": "Bug",
            "status": "Pending",
            "created_at": "2025-03-26T12:00:00Z",
            "completed_at": null
        }
    ]
}
```

---

## **Setup Instructions**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/task-manager.git
cd task-manager
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Run Migrations**
```sh
python manage.py makemigrations\python manage.py migrate
```

### **4️⃣ Create a Superuser**
```sh
python manage.py createsuperuser
```

### **5️⃣ Start the Server**
```sh
python manage.py runserver
```

Now visit `http://127.0.0.1:8000/` to use the web UI or test the API routes using Postman or Curl.

---

## **Additional Notes**
- The application does not require authentication for API calls.
- If `created_by` is `null`, tasks will be assigned to a default system user.
- Tasks cannot be assigned after they are marked **Completed**.
- Tasks can only be updated by assigned users.

Happy Coding! 🚀

