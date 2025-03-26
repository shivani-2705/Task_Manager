# Task Manager

Task Manager is a Django-based application that allows users to create, assign, and manage tasks efficiently. It provides both a web interface and a REST API for task management.

## Features
- User authentication (Register, Login, Logout)
- Task creation 
- Assign task to users
- Update task status
- View tasks assigned to a user
- REST API endpoints for task management

---

## **Web Routes (UI)**

| Route | Method | Description |
|--------|--------|-------------|
| `/web/login/` | GET, POST | User login page |
| `/web/register/` | GET, POST | User registration page |
| `/web/logout/` | GET | Logout user and redirect to login |
| `/web/tasks/` | GET | Displays tasks created by or assigned to the logged-in user |
| `/web/tasks/create/` | GET, POST | Create a new task  |
| `/web/tasks/<task_id>/assign/` | GET, POST | Assign users to an existing task |
| `/web/tasks/update_status/<task_id>/` | POST | Update the status of a task |

---

## **API Endpoints**

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/web/api/tasks/` | GET | Fetch all tasks assigned to a specific user (requires `email` query parameter) |
| `/web/api/tasks/create/` | POST | Create a new task |
| `/web/api/tasks/<task_id>/assign/` | POST | Assign a task to users |

### **API Request & Response Examples**

#### 1️⃣ Create a Task (POST `/web/api/tasks/create/`)
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

#### 2️⃣ Assign Users to a Task (POST `/web/api/tasks/<task_id>/assign/`)
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

#### 3️⃣ Fetch Tasks for a User (GET `/web/api/tasks/?email=user@example.com`)
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
git clone https://github.com/shivani-2705/Task_Manager.git
cd task_manager
```

### **2️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
Create a `.env` file in the root directory and add the following:
```ini
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=task_manager
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### **4️⃣ Configure Database (PostgreSQL)**
Ensure PostgreSQL is installed and running. Then create a database:
```sh
psql -U your_db_user -c "CREATE DATABASE task_manager;"
```
Update `settings.py` to use environment variables for database configuration:
```python
import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}
```

### **5️⃣ Run Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```

### **6️⃣ Create a Superuser**
```sh
python manage.py createsuperuser
```

### **7️⃣ Start the Server**
```sh
python manage.py runserver
```

Now visit `http://127.0.0.1:8000/` to use the web UI or test the API routes using Postman or Curl.

---

## **Additional Notes**
- The application does not require authentication for API calls.
- Tasks must be created with a `created_by` user; it cannot be null.
- Tasks cannot be assigned after they are marked **Completed**.
- Tasks can only be updated by assigned users.

Happy Coding! 🚀

