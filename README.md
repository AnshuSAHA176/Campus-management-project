# 🎓 Campus Management & Scheduling System

A production-oriented backend for managing **students, teachers, subjects, batches, classrooms, class schedules, timetables, notifications, conflicts, and administrative operations**.

Built with **Django REST Framework, PostgreSQL, Redis, Django Channels, Celery, JWT Authentication, Docker, and OpenAPI/Swagger**.

---

## ✨ Overview

The Campus Management & Scheduling System is designed to solve the problems that occur when managing academic schedules manually.

It provides a centralized backend where administrators and teachers can:

- Manage students and teachers
- Manage batches, subjects, and rooms
- Schedule classes
- Detect scheduling conflicts automatically
- Manage cancellations and rescheduling
- Generate student, teacher, and admin timetables
- Track administrative activities
- Send real-time notifications
- Schedule background tasks
- Monitor campus-level scheduling information

The system is designed around **database-level consistency**, role-based access control, asynchronous processing, and real-time communication.

---

# 🚀 Features

## 🔐 Authentication & Authorization

- JWT-based authentication
- Custom Django User model
- Email-based login
- Role-based access control
- Supported roles:
  - 👨‍🎓 Student
  - 👨‍🏫 Teacher
  - 👨‍💼 Admin
  - 🏛️ HOD

---

## 👨‍🎓 Student Management

Administrators can manage:

- Student profiles
- Student IDs
- Batch assignment
- Contact information
- Enrollment information
- Profile pictures

Students automatically see classes associated with their assigned batch.

---

## 👨‍🏫 Teacher Management

Teacher management includes:

- Employee ID
- Teacher profile
- Department
- Designation
- Contact information
- Profile picture

Teachers can access their own scheduled classes and timetable.

---

## 📚 Academic Management

The system supports management of:

- Departments
- Subjects
- Batches
- Sections
- Students
- Teachers

---

# 🗓️ Smart Class Scheduling

Classes are represented by `ClassSession`.

Each class contains:

```text
Subject
Teacher
Batch
Room
Date
Start Time
End Time
Status
Created By
```

Supported class states include:

```text
SCHEDULED
CANCELLED
```

---

# 🛡️ Conflict Detection

One of the core features is automatic scheduling conflict detection.

The system prevents:

### 👨‍🏫 Teacher Conflicts

A teacher cannot have two classes at the same time.

### 👨‍🎓 Batch Conflicts

A batch cannot have two classes at the same time.

### 🏫 Room Conflicts

A classroom cannot be assigned to two overlapping classes.

### 🔒 Database-Level Protection

Scheduling conflicts are enforced using PostgreSQL exclusion constraints.

This means conflict protection doesn't rely only on application-level validation.

Even concurrent requests are protected by the database.

---

# 🔄 Rescheduling & Cancellation

Existing classes can be modified using the existing class-session API.

### Reschedule

```json
{
  "date": "2026-10-01",
  "start_time": "14:00:00",
  "end_time": "15:00:00",
  "room": 2
}
```

### Cancel

```json
{
  "status": "CANCELLED",
  "cancellation_reason": "Teacher unavailable"
}
```

The system validates the updated schedule before applying changes.

---

# 📅 Timetable System

The timetable is generated directly from `ClassSession`.

No redundant timetable table is required.

### Student Timetable

Students receive classes belonging to their batch.

### Teacher Timetable

Teachers receive classes assigned to them.

### Admin/HOD Timetable

Administrators can view the complete campus schedule.

Example:

```json
{
  "id": 16,
  "date": "2026-10-10",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "subject_name": "Data Structures",
  "teacher_name": "Bikash Roy",
  "batch_name": "BCA-3B",
  "status": "SCHEDULED"
}
```

---

# 🔎 Filtering

Class schedules can be filtered using Django Filter.

Supported filters include:

```text
date
date__gt
date__lt
date_range
teacher
batch
room
subject
status
```

Example:

```http
GET /scheduling/class-sessions/?status=SCHEDULED
```

---

# 🔔 Real-Time Notifications

The system uses:

```text
Django Channels
        +
Redis
        +
WebSockets
```

Students can maintain a WebSocket connection and receive notifications related to their batch.

Example:

```text
/ws/notification/?token=<JWT_ACCESS_TOKEN>
```

Notifications can be triggered when:

- A class is created
- A class is cancelled
- A class is rescheduled
- The class date changes
- The class time changes
- The classroom changes

---

# ⚡ Background Tasks

Celery is used for asynchronous processing.

Architecture:

```text
Django
   │
   ├── Celery
   │      │
   │      └── Redis
   │
   └── PostgreSQL
```

Current scheduled notification workflow:

```text
Class Created
      │
      ├──────────────► Immediate Task
      │
      └── 15 Minutes Before
                     │
                     ▼
              Background Task
```

Class-specific tasks use Celery ETA scheduling.

---

# 📊 Admin Dashboard

The backend provides dashboard metrics such as:

### Overview

```text
Total Students
Total Teachers
Total Subjects
Total Batches
Total Rooms
```

### Today's Classes

```text
Total Classes
Ongoing Classes
Scheduled Classes
Completed Classes
```

### Weekly Schedule

```text
Classes This Week
Classes Next Week
Cancelled This Week
Rescheduled This Week
```

### Room Usage

```text
Total Rooms
Rooms In Use
Available Rooms
Utilization Percentage
```

### Activity

Recent administrative scheduling activity is tracked for dashboard visibility.

---

# 🧾 Activity & Audit Tracking

The system records important scheduling activities such as:

```text
CLASS_CREATED
CLASS_RESCHEDULED
CLASS_CANCELLED
```

This provides administrators with visibility into recent system activity.

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      Client Apps     │
                    │ Web / Mobile / APK   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Django REST      │
                    │        API           │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        PostgreSQL          Redis          Celery Worker
              │                │                │
              │                │                │
              │                ▼                │
              │          Django Channels       │
              │                │                │
              └────────────────┼────────────────┘
                               │
                               ▼
                         WebSocket
                        Notifications
```

---

# 🛠️ Tech Stack

## Backend

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST API |
| PostgreSQL | Primary database |
| Redis | Cache / message broker |
| Celery | Background tasks |
| Django Channels | WebSockets |
| Simple JWT | Authentication |
| django-filter | API filtering |
| drf-spectacular | OpenAPI / Swagger |

## Infrastructure

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| PostgreSQL Docker | Database |
| Redis Docker | Redis service |
| Git | Version control |
| GitHub | Source control |

---

# 📁 Project Structure

```text
campus-management-system/
│
├── src/
│   │
│   ├── apps/
│   │   │
│   │   ├── account/
│   │   ├── academics/
│   │   ├── scheduling/
│   │   ├── rooms/
│   │   └── ...
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   ├── celery.py
│   │   └── __init__.py
│   │
│   └── manage.py
│
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# ⚙️ Local Development

## 1. Clone the repository

```bash
git clone <your-repository-url>

cd campus-management-system
```

---

## 2. Create the environment

This project uses `uv`.

```bash
uv sync
```

---

## 3. Start PostgreSQL and Redis

Example Docker services:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

---

## 4. Run migrations

```bash
uv run python src/manage.py migrate
```

---

## 5. Create a superuser

```bash
uv run python src/manage.py createsuperuser
```

---

## 6. Start Django

```bash
uv run python src/manage.py runserver
```

---

# ⚡ Start Celery

Start the worker:

```bash
uv run celery -A config worker --loglevel=info --pool=solo
```

> `--pool=solo` is useful for local development on macOS.

---

# 🔴 Redis

Redis is used for:

```text
Database 0 → Django Channels
Database 1 → Celery
```

Example:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

Celery:

```python
CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"
```

---

# 📖 API Documentation

OpenAPI schema:

```text
/schema/
```

Swagger UI:

```text
/docs/
```

Redoc:

```text
/redoc/
```

The API documentation is generated using `drf-spectacular`.

---

# 🔐 API Authorization

Protected endpoints require a JWT access token.

Example:

```http
Authorization: Bearer <access_token>
```

---

# 👥 Permission Model

| Operation | Student | Teacher | Admin/HOD |
|---|---:|---:|---:|
| View classes | ✅ | ✅ | ✅ |
| View timetable | ✅ | ✅ | ✅ |
| Create class | ❌ | ✅ | ✅ |
| Update class | ❌ | ✅ | ✅ |
| Cancel class | ❌ | ✅ | ✅ |
| Delete class | ❌ | ✅ | ✅ |
| Manage users | ❌ | ❌ | ✅ |
| View campus schedule | ❌ | Limited | ✅ |

---

# 🔮 Future Improvements

Planned improvements include:

- WhatsApp notification integration
- Push notifications
- Automated timetable generation
- Recurring classes
- Room capacity validation
- Lab requirement validation
- Class attendance
- Advanced analytics
- Better audit history
- Notification preferences
- Automatic timetable optimization
- Mobile application
- Production monitoring
- Rate limiting
- Advanced caching
- Horizontal scaling

---

# 🎯 Design Goals

The project focuses on:

```text
Consistency
Security
Scalability
Real-time communication
Background processing
Database integrity
Clean API design
Role-based access
```

A major design principle is:

> **Important scheduling rules should be enforced at the database level whenever possible.**

---

# 🧪 Testing

Before deploying, test:

```text
Authentication
Permissions
Class creation
Class update
Class cancellation
Class rescheduling
Teacher conflicts
Batch conflicts
Room conflicts
Concurrent scheduling
Timetable filtering
WebSocket authentication
WebSocket notifications
Celery tasks
Dashboard calculations
```

---

# 🚀 Production Architecture

A production deployment can be structured as:

```text
                    Load Balancer
                          │
             ┌────────────┴────────────┐
             │                         │
        Django API #1             Django API #2
             │                         │
             └────────────┬────────────┘
                          │
                    PostgreSQL
                          │
                        Redis
                       /     \
                      /       \
               Celery Worker   Channels
                      │
                      ▼
                Background Jobs
```

This allows the API layer to scale independently from background workers.

---

# 📌 Project Status

## Core Backend

- [x] Custom authentication
- [x] Role-based permissions
- [x] Student management
- [x] Teacher management
- [x] Academic management
- [x] Room management
- [x] Class scheduling
- [x] Conflict detection
- [x] PostgreSQL constraints
- [x] Class cancellation
- [x] Class rescheduling
- [x] Timetable API
- [x] Filtering
- [x] Redis
- [x] WebSockets
- [x] Real-time notifications
- [x] Celery
- [x] Scheduled background tasks
- [x] Dashboard
- [x] Activity tracking
- [x] API documentation

## Upcoming

- [ ] WhatsApp notification integration
- [ ] Push notifications
- [ ] Automated timetable generation
- [ ] Attendance
- [ ] Advanced analytics
- [ ] Production deployment optimization

---

# 👨‍💻 Author

**Anshu Saha**

Backend Developer

`Python` • `Django` • `DRF` • `PostgreSQL` • `Redis` • `Celery` • `WebSockets`

---

# ⭐ If You Find This Project Interesting

Give the repository a ⭐ and feel free to explore the architecture, APIs, and scheduling implementation.

---
