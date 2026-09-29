# Campus Management System API Documentation

This project is a Django + DRF backend for a campus management system. It supports:
- Student, teacher, admin, and HOD authentication
- Academic management (departments, semesters, batches, subjects)
- Room management
- Class scheduling
- Scheduling conflict detection
- Real-time notifications via WebSockets
- Background jobs with Celery
- Admin dashboard and audit logs
- AI agent integration for campus-related questions

Base URL:
- Local dev: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs/
- OpenAPI schema: http://127.0.0.1:8000/schema/

Authentication:
- Use JWT bearer tokens.
- Header:
  Authorization: Bearer <access_token>

Important note:
- Most protected endpoints require a valid login.
- Admin-only routes require `is_staff == True`.
- Teacher-specific routes require `request.user.role == "teacher"`.

---

# API Endpoint Reference

This project exposes a Django REST Framework backend for campus management. All routes are grouped by app and mounted from the root URL configuration in `src/config/urls.py`.

Base URLs:
- Local backend: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/schema/`
- Admin site: `http://127.0.0.1:8000/admin/`

Authentication:
- Most endpoints require a logged-in user.
- Use JWT access token in the header:
  `Authorization: Bearer <access_token>`
- `login` returns both `access` and `refresh` tokens.

Important access rules:
- `POST /register/` and `POST /login/` are public.
- Student profile endpoints require `request.user.role == "student"`.
- Teacher profile endpoints require `request.user.role == "teacher"`.
- Admin routes require `is_staff == True`.
- Scheduling create/update operations are allowed for admin or teacher users.

---

## 1) Authentication and account endpoints

These are mounted directly at the project root.

### Public endpoints

1. `POST /register/`
   - Create a new user account.
   - Example body:
     ```json
     {
       "email": "student@example.com",
       "password": "StrongPassword123",
       "role": "student"
     }
     ```
   - Response: created user information and token handling from the serializer.

2. `POST /login/`
   - Authenticate a user and return JWT tokens.
   - Example body:
     ```json
     {
       "email": "student@example.com",
       "password": "StrongPassword123"
     }
     ```
   - Response:
     ```json
     {
       "access": "<jwt_access_token>",
       "refresh": "<jwt_refresh_token>",
       "role": "student"
     }
     ```

3. `POST /refresh/`
   - Refresh an expired access token using a valid refresh token.
   - Uses Django REST Framework Simple JWT `TokenRefreshView`.

4. `POST /logout/`
   - Blacklist a refresh token and log the user out.
   - Uses `TokenBlacklistView`.

### Authenticated user endpoints

5. `GET /student_profile/`
   - Returns the authenticated student’s profile.
   - Requires student role.

6. `PUT /student_profile/` or `PATCH /student_profile/`
   - Update the student profile.

7. `GET /teacher_profile/`
   - Returns the authenticated teacher profile.
   - Requires teacher role.

8. `PUT /teacher_profile/` or `PATCH /teacher_profile/`
   - Updates the teacher profile.

9. `GET /dashboard/`
   - Returns the admin dashboard summary.
   - Requires admin access.
   - Includes overview counts, today’s schedule metrics, weekly schedule stats, room status, and recent activity.

10. `GET /activitylogs/`
    - Lists recent activity records.
    - Requires admin access.

11. `GET /teacher_search/?q=<search_text>`
    - Search teachers by name or employee ID.
    - Example: `/teacher_search/?q=rahul`
    - Returns a list of matching teacher objects with `id`, `full_name`, and `employee_id`.

---

## 2) Academic endpoints

All academic endpoints are under the `/api/` prefix.

### 2.1 Department endpoints

Base route: `/api/departments/`

- `GET /api/departments/` — list all departments
- `POST /api/departments/` — create a department
- `GET /api/departments/<id>/` — retrieve one department
- `PUT /api/departments/<id>/` — update department
- `PATCH /api/departments/<id>/` — partial update
- `DELETE /api/departments/<id>/` — delete department

### 2.2 Semester endpoints

Base route: `/api/semesters/`

- `GET /api/semesters/` — list semesters
- `POST /api/semesters/` — create semester
- `GET /api/semesters/<id>/` — retrieve semester
- `PUT /api/semesters/<id>/` — update semester
- `PATCH /api/semesters/<id>/` — partial update
- `DELETE /api/semesters/<id>/` — delete semester

### 2.3 Batch endpoints

Base route: `/api/batches/`

- `GET /api/batches/` — list all batches
- `POST /api/batches/` — create a batch
- `GET /api/batches/<id>/` — retrieve a batch
- `PUT /api/batches/<id>/` — update a batch
- `PATCH /api/batches/<id>/` — partial update
- `DELETE /api/batches/<id>/` — delete a batch

### 2.4 Subject endpoints

Base route: `/api/subject/`

- `GET /api/subject/` — list subjects
- `POST /api/subject/` — create subject
- `GET /api/subject/<id>/` — retrieve subject
- `PUT /api/subject/<id>/` — update subject
- `PATCH /api/subject/<id>/`` — partial update
- `DELETE /api/subject/<id>/` — delete subject

### 2.5 Search endpoints

- `GET /api/batches/search/?q=<text>`
  - Search batches by name.
  - Example: `/api/batches/search/?q=3A`

- `GET /api/subject/search/?q=<text>`
  - Search subjects by name or subject code.
  - Example: `/api/subject/search/?q=dbms`

Notes:
- Academic management routes are admin-only in this project (`IsAdminUser`).
- These endpoints use `ModelViewSet`, so standard CRUD operations are available automatically.

---

## 3) Room endpoints

All room routes are mounted under `/rooms/`.

### Core room CRUD

Base route: `/rooms/`

- `GET /rooms/` — list rooms
- `POST /rooms/` — create a room
- `GET /rooms/<id>/` — fetch one room
- `PUT /rooms/<id>/` — update room
- `PATCH /rooms/<id>/` — partial update
- `DELETE /rooms/<id>/` — delete room

### Room search and availability

- `GET /rooms/search/?q=<text>`
  - Search room by room number or floor.
  - Example: `/rooms/search/?q=204`

- `GET /rooms/avalable/?date=YYYY-MM-DD&start_time=HH:MM:SS&end_time=HH:MM:SS`
  - Check room availability for a time range.
  - Example:
    ```http
    GET /rooms/avalable/?date=2026-09-29&start_time=09:00:00&end_time=10:00:00
    ```
  - Returns available rooms that do not conflict with the selected time slot.

Note:
- Room management is admin-only, but searching and availability checks require authentication.

---

## 4) Scheduling endpoints

All scheduling routes are under `/scheduling/`.

### Core class session CRUD

Base route: `/scheduling/`

- `GET /scheduling/` — list class sessions for the current user
  - Students see classes in their own batch.
  - Teachers see classes they teach.
  - Admins see all sessions.
- `POST /scheduling/` — create a class session
- `GET /scheduling/<id>/` — retrieve one class session
- `PUT /scheduling/<id>/` — update a session
- `PATCH /scheduling/<id>/` — partial update
- `DELETE /scheduling/<id>/` — delete a class session

### Scheduling custom actions

- `GET /scheduling/timetable/`
  - Returns the timetable for the current user or all classes depending on role.
  - Supports filtering via query parameters.

- `GET /scheduling/available-rooms/?date=YYYY-MM-DD&start_time=HH:MM:SS&end_time=HH:MM:SS`
  - Returns rooms that are free during a given time window.

- `GET /scheduling/teacher-schedule/?teacher_id=<id>&date=YYYY-MM-DD`
  - Returns a teacher’s schedule for a specific date.
  - If the logged-in user is a teacher, `teacher_id` can be omitted.

- `GET /scheduling/tools/`
  - Returns class session data for the AI agent and schedule tools.
  - Authenticated users only.

- `GET /scheduling/conflict/?date=YYYY-MM-DD&start_time=HH:MM:SS&end_time=HH:MM:SS&teacher_id=<id>&batch_id=<id>&room_id=<id>`
  - Checks whether a requested class schedule would conflict with existing schedule data.
  - Response is used as a pre-check before scheduling.

Schedule creation behavior:
- Admin and teacher users can create schedules.
- The system checks conflicts for teacher, batch, and room overlap.
- If a conflict exists, a `400 Bad Request` is returned with a descriptive error, for example:
  - teacher already has a class during this time
  - batch already has a class during this time
  - room is already booked during this time

---

## 5) AI agent endpoints

These are mounted under `/agent/`.

### 5.1 Campus AI chat

- `POST /agent/`
  - Sends a campus-related question to the AI assistant.
  - Request body:
    ```json
    {
      "message": "What classes does the BCA batch have tomorrow?"
    }
    ```
  - This endpoint streams a Server-Sent Events (SSE) response.
  - It uses the campus agent with access to schedule tools and knowledge-base tools.

### 5.2 Knowledge upload

- `POST /agent/knowledge/`
  - Uploads a document into the knowledge base.
  - Requires admin access.
  - Uses the `DocumentView` and `DocumentSerializer`.

Note:
- The AI assistant is designed to answer campus questions using both live schedule data and uploaded knowledge documents.

---

## 6) Documentation and schema endpoints

- `GET /schema/` — OpenAPI schema file
- `GET /docs/` — Swagger UI documentation page
- `GET /admin/` — Django admin UI

These are defined in `src/config/urls.py`.

---

## 7) WebSocket endpoint

The project also includes a WebSocket notification stream.

- `ws/notification/`
  - Real-time notification channel for scheduling updates.
  - Integrated through `apps.scheduling.webshocker_urls` and `NotificationConsumer`.

Example WebSocket URL:
```text
ws://127.0.0.1:8000/ws/notification/
```

---

## 8) Typical request examples

### Login
```http
POST /login/
Content-Type: application/json

{
  "email": "student@example.com",
  "password": "StrongPassword123"
}
```

### Get timetable
```http
GET /scheduling/timetable/
Authorization: Bearer <access_token>
```

### Search room
```http
GET /rooms/search/?q=301
Authorization: Bearer <access_token>
```

### Create class session
```http
POST /scheduling/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "date": "2026-09-30",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "teacher": 1,
  "batch": 2,
  "room": 3,
  "subject": 4,
  "status": "scheduled"
}
```

---

## 9) Endpoint summary table

| Module | Route prefix | Purpose |
|---|---|---|
| Account | `/` | auth, profile, dashboard, search |
| Academics | `/api/` | departments, semesters, batches, subjects |
| Rooms | `/rooms/` | room CRUD, search, availability |
| Scheduling | `/scheduling/` | class session CRUD and conflict checks |
| Agent | `/agent/` | AI chat and knowledge upload |
| Docs | `/docs/`, `/schema/` | API docs |
| WebSocket | `/ws/notification/` | live notifications |

---

The endpoint list above reflects the actual code in the project and is meant to be a practical reference for developers and API consumers working with this campus management backend.

---

# 1. Project Structure

```text
src/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── celery.py
│   └── wsgi.py
├── compus_management_system/
│   └── __init__.py
├── apps/
│   ├── account/
│   │   ├── models.py        # User, Student, Teacher
│   │   ├── serializer.py     # Auth + profile serializers
│   │   ├── views.py         # Login/register/profile/dashboard endpoints
│   │   ├── urls.py          # Auth routes
│   │   ├── signals.py       # Creates Student/Teacher profile on user creation
│   │   └── custom_manager.py
│   ├── academics/
│   │   ├── models.py        # Department, Semester, Batch, Subject
│   │   ├── serializer.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── rooms/
│   │   ├── models.py        # Room model
│   │   ├── serializer.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── scheduling/
│   │   ├── models.py        # ClassSession + Activity
│   │   ├── serializer.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── signal.py        # Notifications & activity tracking
│   │   ├── consumers.py     # WebSocket notification consumer
│   │   ├── aut_middlewere.py # JWT for WebSockets
│   │   ├── notification_clint.py
│   │   └── filter.py
│   ├── agent/
│   │   ├── agent.py
│   │   ├── tools.py
│   │   ├── llm.py
│   │   ├── services.py
│   │   ├── views.py
│   │   └── urls.py
│   └── __init__.py
└── manage.py
```

---

# 2. Roles and Permissions

Supported roles:

- student
- teacher
- admin
- hod

Role behavior:
- Student:
  - Can view own classes and timetable
  - Can view own profile
  - Cannot create/update schedules
- Teacher:
  - Can view own schedule
  - Can create or update class schedules
  - Can cancel classes
- Admin / HOD:
  - Can manage academic data, rooms, and schedules
  - Can view dashboard and activity logs

---

# 3. Core Data Models

## 3.1 User

Model: `apps.account.models.User`

Fields:
- id: UUID
- email: string, unique
- role: student | teacher | admin | hod
- is_active: boolean
- is_staff: boolean
- created_at
- updated_at

Create payload:
```json
{
  "email": "student@example.com",
  "role": "student",
  "password": "StrongPassword123"
}
```

---

## 3.2 Student

Model: `apps.account.models.Student`

Fields:
- id
- user
- student_id
- batch
- full_name
- phone
- profile_picture
- enrollment_date
- created_at
- updated_at

Example:
```json
{
  "student_id": "STU-2025-001",
  "batch": 3,
  "full_name": "Amit Verma",
  "phone": "9876543210",
  "enrollment_date": "2025-08-01"
}
```

---

## 3.3 Teacher

Model: `apps.account.models.Teacher`

Fields:
- id
- user
- employee_id
- full_name
- department
- designation
- phone
- profile_picture
- created_at
- updated_at

Example:
```json
{
  "employee_id": "EMP-1001",
  "full_name": "Bikash Roy",
  "department": 1,
  "designation": "Assistant Professor",
  "phone": "9876543211"
}
```

---

## 3.4 Department

Model: `apps.academics.models.Department`

Fields:
- id
- name
- code
- created_at
- updated_at

Example:
```json
{
  "name": "Computer Science",
  "code": "CS"
}
```

---

## 3.5 Semester

Model: `apps.academics.models.Semester`

Fields:
- id
- department
- number
- name
- start_date
- end_date
- created_at

Example:
```json
{
  "department": 1,
  "number": 3,
  "name": "Semester 3",
  "start_date": "2025-07-01",
  "end_date": "2025-12-15"
}
```

---

## 3.6 Batch

Model: `apps.academics.models.Batch`

Fields:
- id
- department
- semester
- name
- section
- academic_year
- capacity
- is_active
- created_at
- updated_at

Example:
```json
{
  "department": 1,
  "semester": 3,
  "name": "BCA",
  "section": "A",
  "academic_year": "2025-2026",
  "capacity": 60,
  "is_active": true
}
```

---

## 3.7 Subject

Model: `apps.academics.models.Subject`

Fields:
- id
- department
- semester
- teachers
- name
- code
- is_active
- created_at
- updated_at

Example:
```json
{
  "department": 1,
  "semester": 3,
  "name": "Data Structures",
  "code": "CS301",
  "is_active": true,
  "teachers": [1, 2]
}
```

---

## 3.8 Room

Model: `apps.rooms.models.Room`

Fields:
- id
- department
- room_number
- building
- floor
- capacity
- room_type
- is_active
- created_at
- updated_at

Valid room types:
- CLASSROOM
- COMPUTER_LAB
- LAB
- SEMINAR_HALL

Example:
```json
{
  "department": 1,
  "room_number": "301",
  "building": "Main Block",
  "floor": 3,
  "capacity": 60,
  "room_type": "CLASSROOM",
  "is_active": true
}
```

---

## 3.9 ClassSession

Model: `apps.scheduling.models.ClassSession`

Fields:
- id
- subject
- teacher
- batch
- room
- date
- start_time
- end_time
- time_range
- status
- cancellation_reason
- created_by
- created_at
- updated_at

Valid status:
- SCHEDULED
- CANCELLED
- COMPLETED

Example create payload:
```json
{
  "subject": 5,
  "teacher": 2,
  "batch": 3,
  "room": 4,
  "date": "2026-09-28",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "status": "SCHEDULED"
}
```

Important rules:
- Teacher cannot have overlapping class
- Batch cannot have overlapping class
- Room cannot be double-booked
- Subject, batch, and room must belong to same department as teacher
- `cancellation_reason` is required if status is CANCELLED

---

## 3.10 Activity

Model: `apps.scheduling.models.Activity`

Fields:
- id
- type
- message
- created_at

Valid types:
- CLASS_CREATED
- CLASS_RESCHEDULED
- CLASS_CANCELLED

---

# 4. API Endpoints

## 4.1 Account / Auth APIs

### 1) Register User
Route:
- POST /register/

Description:
- Create a new user account.
- Automatically creates matching `Student` or `Teacher` profile based on role.

Required payload:
```json
{
  "email": "student@example.com",
  "role": "student",
  "password": "Pass1234!"
}
```

Status codes:
- 201 Created
- 400 Bad Request
- 500 Server Error

Response example:
```json
{
  "email": "student@example.com",
  "role": "student"
}
```

---

### 2) Login
Route:
- POST /login/

Required payload:
```json
{
  "email": "student@example.com",
  "password": "Pass1234!"
}
```

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized

Response example:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 3) Refresh Token
Route:
- POST /refresh/

Description:
- Refresh JWT access token using refresh token.

Required payload:
```json
{
  "refresh": "<refresh_token>"
}
```

Status codes:
- 200 OK
- 401 Unauthorized
- 400 Bad Request

Response example:
```json
{
  "access": "new_access_token"
}
```

---

### 4) Logout
Route:
- POST /logout/

Description:
- Blacklist refresh token.

Required payload:
```json
{
  "refresh": "<refresh_token>"
}
```

Status codes:
- 205 Reset Content
- 400 Bad Request
- 401 Unauthorized

---

### 5) Student Profile
Route:
- GET /student_profile/
- PATCH /student_profile/

Description:
- Fetch or update logged-in student's profile.

Authentication:
- Required
- Role must be `student`

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

Response example:
```json
{
  "student_id": "STU-2025-001",
  "batch": 3,
  "phone": "9876543210",
  "full_name": "Amit Verma",
  "enrollment_date": "2025-08-01",
  "profile_picture": "https://..."
}
```

Update payload example:
```json
{
  "phone": "9876543210",
  "full_name": "Amit Verma"
}
```

---

### 6) Teacher Profile
Route:
- GET /teacher_profile/
- PATCH /teacher_profile/

Description:
- Fetch or update logged-in teacher profile.

Authentication:
- Required
- Role must be `teacher`

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

Example payload:
```json
{
  "employee_id": "EMP-1001",
  "department": 1,
  "designation": "Assistant Professor",
  "phone": "9876543211"
}
```

---

### 7) Admin Dashboard
Route:
- GET /dashboard/

Description:
- Returns overview metrics for admin/HOD.
- Includes counts for students, teachers, subjects, batches, rooms, classes, room utilization, etc.

Authentication:
- Required
- Admin only

Status codes:
- 200 OK
- 401 Unauthorized
- 403 Forbidden

Example response:
```json
{
  "overview": {
    "total_students": 245,
    "total_teachers": 35,
    "total_subjects": 72,
    "total_batches": 12,
    "total_rooms": 30
  },
  "today": {
    "total_classes": 18,
    "ongoing_classes": 3,
    "scheduled_classes": 15,
    "completed_classes": 0
  },
  "schedule": {
    "classes_this_week": 60,
    "classes_next_week": 58,
    "cancelled_this_week": 2,
    "rescheduled_this_week": 4
  },
  "rooms": {
    "total_rooms": 30,
    "rooms_in_use": 8,
    "available_rooms": 22,
    "utilization_percentage": 27
  }
}
```

---

### 8) Audit Logs
Route:
- GET /activitylogs/

Description:
- Returns recent scheduling activity logs.

Authentication:
- Required
- Admin only

Status codes:
- 200 OK
- 401 Unauthorized
- 403 Forbidden

Example:
```json
[
  {
    "id": 4,
    "type": "CLASS_CREATED",
    "message": "New class: CS301 on 2026-09-28 at 10:00:00 in Room 301.",
    "created_at": "2026-09-24T09:30:00Z"
  }
]
```

---

### 9) Teacher Search
Route:
- GET /teacher_search/?q=<query>

Description:
- Search teachers by name or employee ID.

Authentication:
- Required

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized

Example:
```json
[
  {
    "id": 2,
    "full_name": "Bikash Roy",
    "employee_id": "EMP-1001"
  }
]
```

---

## 4.2 Academics APIs

Base prefix:
- /api/

### 10) Department list/create
Route:
- GET /api/departments/
- POST /api/departments/

Authentication:
- Admin only

Status codes:
- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

Create payload:
```json
{
  "name": "Computer Science",
  "code": "CS"
}
```

---

### 11) Department detail/update/delete
Routes:
- GET /api/departments/<id>/
- PUT /api/departments/<id>/
- PATCH /api/departments/<id>/
- DELETE /api/departments/<id>/

---

### 12) Semester list/create
Route:
- GET /api/semesters/
- POST /api/semesters/

Create payload:
```json
{
  "department": 1,
  "number": 3,
  "name": "Semester 3",
  "start_date": "2025-07-01",
  "end_date": "2025-12-15"
}
```

---

### 13) Batch list/create
Route:
- GET /api/batches/
- POST /api/batches/

Create payload:
```json
{
  "department": 1,
  "semester": 3,
  "name": "BCA",
  "section": "A",
  "academic_year": "2025-2026",
  "capacity": 60,
  "is_active": true
}
```

---

### 14) Subject list/create
Route:
- GET /api/subject/
- POST /api/subject/

Create payload:
```json
{
  "department": 1,
  "semester": 3,
  "teachers": [1, 2],
  "name": "Data Structures",
  "code": "CS301",
  "is_active": true
}
```

---

### 15) Search batches
Route:
- GET /api/batches/search/?q=<query>

Example:
```http
GET /api/batches/search/?q=BCA
```

Response:
```json
[
  { "id": 3, "name": "BCA" }
]
```

---

### 16) Search subjects
Route:
- GET /api/subject/search/?q=<query>

Example:
```http
GET /api/subject/search/?q=Data
```

Response:
```json
[
  [5, "Data Structures", "CS301"]
]
```

---

## 4.3 Room APIs

Base prefix:
- /rooms/

### 17) Room list/create
Routes:
- GET /rooms/
- POST /rooms/

Authentication:
- Admin only

Create payload:
```json
{
  "department": 1,
  "room_number": "301",
  "building": "Main Block",
  "floor": 3,
  "capacity": 60,
  "room_type": "CLASSROOM",
  "is_active": true
}
```

Status codes:
- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

---

### 18) Search rooms
Route:
- GET /rooms/search/?q=<query>

Description:
- Search room by room number or floor

Example:
```http
GET /rooms/search/?q=301
```

Response:
```json
[
  {
    "id": 4,
    "room_number": "301",
    "floor": 3
  }
]
```

---

### 19) Available rooms
Route:
- GET /rooms/avalable/?date=YYYY-MM-DD&start_time=HH:MM:SS&end_time=HH:MM:SS

Description:
- Returns rooms that are active and not assigned to overlapping scheduled classes.

Required query parameters:
- date
- start_time
- end_time

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized

Response example:
```json
[
  {
    "id": 7,
    "room_number": "305",
    "capacity": 50
  }
]
```

---

## 4.4 Scheduling APIs

Base prefix:
- /scheduling/

### 20) Class Session list/create
Routes:
- GET /scheduling/
- POST /scheduling/

Description:
- List all class sessions visible to the current user.
- Students only get their own batch classes.
- Teachers only get their own classes.
- Admin gets all.

Authentication:
- Required

Required payload for create:
```json
{
  "subject": 5,
  "teacher": 2,
  "batch": 3,
  "room": 4,
  "date": "2026-09-28",
  "start_time": "10:00:00",
  "end_time": "11:00:00"
}
```

Status codes:
- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

---

### 21) Class Session detail/update/delete
Routes:
- GET /scheduling/<id>/
- PUT /scheduling/<id>/
- PATCH /scheduling/<id>/
- DELETE /scheduling/<id>/

Description:
- Update or delete class sessions.

For cancellation:
```json
{
  "status": "CANCELLED",
  "cancellation_reason": "Teacher unavailable"
}
```

Status codes:
- 200 OK
- 204 No Content
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found

---

### 22) Timetable
Route:
- GET /scheduling/?format=... OR use list route with filter
- GET /scheduling/timetable/

Description:
- Returns timetable for current user or all classes depending on role.

Status codes:
- 200 OK
- 401 Unauthorized

Response example:
```json
[
  {
    "id": 16,
    "date": "2026-10-10",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "subject_name": "Data Structures",
    "teacher_name": "Bikash Roy",
    "batch_name": "BCA-3B",
    "room_name": "Room 301",
    "status": "SCHEDULED"
  }
]
```

---

### 23) Available rooms for schedule
Route:
- GET /scheduling/available-rooms/?date=...&start_time=...&end_time=...

Description:
- Returns rooms free during the selected time and date.

Required query params:
- date
- start_time
- end_time

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized

Example:
```http
GET /scheduling/available-rooms/?date=2026-09-28&start_time=10:00:00&end_time=11:00:00
```

Response:
```json
[
  {
    "department": 1,
    "room_number": "305",
    "floor": 3,
    "capacity": 50
  }
]
```

---

### 24) Teacher Schedule
Route:
- GET /scheduling/teacher-schedule/?teacher_id=<id>&date=YYYY-MM-DD

Description:
- Returns teacher's schedule for a given date.

If the caller is a teacher:
- teacher_id can be omitted, and backend uses the logged-in teacher.

Required query params:
- date
- teacher_id (optional for teacher requests)

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

Example response:
```json
{
  "teacher_id": 2,
  "date": "2026-09-28",
  "classes": [
    {
      "id": 9,
      "date": "2026-09-28",
      "start_time": "10:00:00",
      "end_time": "11:00:00",
      "subject_name": "Data Structures",
      "batch_name": "BCA-3B",
      "room_num": "301",
      "status": "SCHEDULED"
    }
  ]
}
```

---

### 25) Conflict checker
Route:
- GET /scheduling/conflict/?date=...&start_time=...&end_time=...&teacher_id=...&batch_id=...&room_id=...

Description:
- Checks whether the proposed class conflicts with teacher, batch, or room.

Required query params:
- date
- start_time
- end_time
- teacher_id
- batch_id
- room_id

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized

Response:
```json
{
  "has_conflict": true,
  "conflicts": [
    {
      "type": "teacher",
      "class_id": 12,
      "subject": "Data Structures",
      "teacher": "Bikash Roy",
      "batch": "BCA-3B",
      "room": "301",
      "start_time": "10:00:00",
      "end_time": "11:00:00"
    }
  ]
}
```

No conflict:
```json
{
  "has_conflict": false,
  "conflicts": []
}
```

---

### 26) Schedule tools
Route:
- GET /scheduling/tools/

Description:
- Returns class schedules based on filters for authenticated user.
- Used by the AI agent service.

Optional query params:
- date
- date_from
- date_to

Status codes:
- 200 OK
- 401 Unauthorized

Example:
```http
GET /scheduling/tools/?date=2026-09-28
```

---

## 4.5 Agent API

Base prefix:
- /agent/

### 27) Campus Agent Chat
Route:
- POST /agent/

Description:
- AI-powered assistant for campus-related questions.
- Accepts a natural language message and responds with streaming text events.

Required payload:
```json
{
  "message": "Show me today's schedule"
}
```

Authorization:
- Required

Status codes:
- 200 OK
- 400 Bad Request
- 401 Unauthorized

Streaming event format:
```text
event: tool_start
data: {"tool":"search_teachers"}

event: token
data: {"content":"Here are your classes..."}

event: done
data: {"status":"completed"}
```

The agent can answer questions like:
- Show my schedule
- Show teacher schedule
- Check room availability
- Search teachers, rooms, batches, subjects
- Check scheduling conflicts

---

# 5. WebSocket Notifications

WebSocket endpoint:
- ws/notification/?token=<JWT_ACCESS_TOKEN>

Description:
- Students join a batch group and receive notifications when their batch has a class created, cancelled, or rescheduled.

Authentication:
- JWT token passed in query string as `token`

Important:
- If the user is not authenticated, the connection is closed.
- Students are added to `batch_<batch_id>` group.

Example:
```text
ws://127.0.0.1:8000/ws/notification/?token=<jwt_token>
```

Notification payload:
```json
{
  "type": "notification",
  "message": "New class: CS301 on 2026-09-28 at 10:00:00 in Room 301."
}
```

---

# 6. Celery + Background Jobs

Celery is configured in:
- src/config/celery.py

Redis:
- Broker: redis://127.0.0.1:6379/1
- Result backend: redis://127.0.0.1:6379/1

Current tasks:
- `apps.scheduling.notification_clint.beforeclass`
  - Runs 15 minutes before a class start time
- `apps.scheduling.notification_clint.wanotification`
  - Placeholder async task

Run worker:
```bash
uv run celery -A config worker --loglevel=info --pool=solo
```

Start beat if required:
```bash
uv run celery -A config beat --loglevel=info
```

---

# 7. Frontend Developer Notes

## 7.1 Login Flow
1. Call `POST /login/`
2. Save returned `access` and `refresh`
3. Use access token in every protected request:
   ```http
   Authorization: Bearer <access>
   ```

## 7.2 Role-aware UI
- If role == student:
  - Show student profile
  - Show own timetable
  - Hide class creation forms
- If role == teacher:
  - Show teacher profile
  - Show teacher schedule
  - Allow create/update/cancel class
- If role == admin/hod:
  - Show dashboard
  - Show rooms management
  - Show academic management
  - Show activity logs

## 7.3 Scheduling Form
Required values:
```json
{
  "subject": 5,
  "teacher": 2,
  "batch": 3,
  "room": 4,
  "date": "2026-09-28",
  "start_time": "10:00:00",
  "end_time": "11:00:00"
}
```

Before sending:
- Validate teacher not busy
- Validate batch not busy
- Validate room free
- Ensure subject/batch/room belong to same department

## 7.4 Best practice for conflict validation
Call:
```http
GET /scheduling/conflict/?date=...&start_time=...&end_time=...&teacher_id=...&batch_id=...&room_id=...
```

If `has_conflict == true`, show returned list to user.

## 7.5 Room availability
Call:
```http
GET /rooms/avalable/?date=2026-09-28&start_time=10:00:00&end_time=11:00:00
```

## 7.6 Fetching own timetable
For student:
```http
GET /scheduling/?status=SCHEDULED
```

For teacher:
```http
GET /scheduling/teacher-schedule/?date=2026-09-28
```

## 7.7 Search helpers
Use:
- `/teacher_search/?q=...`
- `/api/batches/search/?q=...`
- `/api/subject/search/?q=...`
- `/rooms/search/?q=...`

---

# 8. Common HTTP Status Codes

- 200 OK: successful GET/PATCH/PUT
- 201 Created: successful POST
- 204 No Content: successful DELETE
- 400 Bad Request: invalid body / validation failed / missing params
- 401 Unauthorized: token missing or invalid
- 403 Forbidden: user does not have permission
- 404 Not Found: resource not found
- 405 Method Not Allowed: unsupported method
- 500 Internal Server Error: server error

---

# 9. Backend Notes and Important Implementation Details

## 9.1 Conflict enforcement
Conflicts are enforced at database level using PostgreSQL exclusion constraints on:
- teacher
- batch
- room
- time_range

This prevents overlapping scheduled classes even when app-level checks are bypassed.

## 9.2 Automatic notifications
When a `ClassSession` is saved:
- `signal.py` listens for create/update
- Creates `Activity` entries
- Sends WebSocket notification to the batch group

## 9.3 Student notifications
The WebSocket consumer adds the student to:
- `batch_<batch_id>`

So students receive class updates of their own batch.

## 9.4 Authentication
This project uses JWT via `djangorestframework-simplejwt`.

---

# 10. Setup Guide

## Install dependencies
```bash
cd /Users/anshusaha/Documents/Compus\ management\ system
uv sync
```

## Run migrations
```bash
uv run python src/manage.py migrate
```

## Run server
```bash
uv run python src/manage.py runserver
```

## Optional: create superuser
```bash
uv run python src/manage.py createsuperuser
```

## Start Celery worker
```bash
uv run celery -A config worker --loglevel=info --pool=solo
```

---

# 11. API Docs

Swagger:
- /docs/

OpenAPI schema:
- /schema/

---

# 12. Summary

This system is built for:
- scheduling academic classes
- preventing conflicts automatically
- managing academic master data
- supporting role-based access
- real-time updates for students
- admin insights and audit tracking

For frontend and developer implementation, the most important endpoints are:
- /login/
- /register/
- /student_profile/
- /teacher_profile/
- /dashboard/
- /api/batches/search/
- /api/subject/search/
- /rooms/search/
- /rooms/avalable/
- /scheduling/
- /scheduling/available-rooms/
- /scheduling/teacher-schedule/
- /scheduling/conflict/
- /agent/

---

If you are building the frontend, start with these flows:
1. Login
2. Get user profile
3. Fetch timetable
4. Search teachers / batches / rooms / subjects
5. Create class
6. Validate conflict
7. Show dashboard data
8. Subscribe to WebSocket notifications

This is the complete API contract required for frontend integration and backend development.