# Leave Management System (Multi-Tenant SaaS)

This project is the backend implementation of a **Leave Management System** designed for a multi-tenant SaaS application. The system allows organizations to define leave policies, manage employee leave requests, and handle approval workflows efficiently.

## Features

- **Admins** can define leave policies for their organization.
- **Employees** can view their leave balance and submit leave requests.
- **Admins** can approve or reject leave requests.

## Assumptions & Open Questions

Before jumping into implementation, here are some key assumptions and questions that need clarification:

1. **Multi-Tenancy**  
   - How should we handle multi-tenancy?  
   - Will each organization have a separate database/schema, or should we use a single shared database with organization scoping?

2. **Leave Policies**  
   - Should leave policies be customizable per organization?  
   - How do we handle different types of leave (e.g., vacation, sick leave, parental leave)?  

3. **Approval Workflow**  
   - Can any admin approve a request, or should it be limited to a specific approver?  
   - Should approvals be single-step or multi-level (e.g., manager + HR approval)?

4. **Notifications**  
   - Should the system send email/Slack notifications for approvals and rejections?  

---

## 2. Data Model Design

The **Leave Management System** consists of three main tables:

### **User Table**
| Column       | Type         | Description                    |
|-------------|-------------|--------------------------------|
| id          | UUID        | Primary key                    |
| email       | String      | Unique email for authentication |
| name        | String      | Full name of the employee      |
| role        | Enum        | `employee` or `admin`         |
| organization_id | UUID    | Organization the user belongs to |
| days_remaining | Integer     | Number of days remaining for annual leave |
| created_at  | Timestamp   | Timestamp of user creation     |

### **LeaveRequest Table**
| Column       | Type         | Description                      |
|-------------|-------------|----------------------------------|
| id          | UUID        | Primary key                      |
| user_id     | UUID        | Foreign key → User               |
| start_date  | Date        | Start date of leave              |
| end_date    | Date        | End date of leave                |
| status      | Enum        | `pending`, `approved`, `rejected` |
| leave_type  | String      | Type of leave (e.g., vacation, sick) |
| approver_id | UUID        | Admin user approving the request |
| created_at  | Timestamp   | Timestamp of request submission  |

### **LeavePolicy Table**
| Column       | Type         | Description                      |
|-------------|-------------|----------------------------------|
| id          | UUID        | Primary key                      |
| organization_id | UUID    | Foreign key → Organization       |
| leave_type  | Enum        | `vacation`, `sick`, `other`      |
| max_days    | Integer     | Maximum leave days allowed       |

---

### **Relationships**
- **Users** belong to **Organizations**.
- **Users** submit **LeaveRequests**.
- **Admins** approve/reject **LeaveRequests**.
- **Organizations** define **LeavePolicies**.cuand

## 3. API Design

### **1. Submit Leave Request**
Employees can submit a leave request.

**Endpoint:**  
`POST /leave-requests/`

**Request Body:**
```json
{
  "user_id": 123,
  "start_date": "2025-04-01",
  "end_date": "2025-04-05", 
  "leave_type": "vacation"
}
```

#### **Response**
```json
{
  "id": "UUID",
  "status": "pending",
  "message": "Leave request submitted successfully."
}
```

---

### **2️. Endpoint: Approve/Reject Leave Request (Admin)**
**Method:** `PUT /leave-requests/{request_id}/status/'
**Description:** Admins can review leave requests.  

#### **Request Body**
```json
{
   "approver_id": 10,
   "status": "approved"
}
```

#### **Response**
```json
{
  "user_id":12345
  "message": "Leave request has been approved."
  "approver_id":10
}
```

---

### **3. Endpoint: Define Leave Policies (Admin)**
**Method:** `POST /leave-policies/'
**Description:** Admins can define lewve policies for their organization.  

#### **Request Body**
```json
{
   "organization_id": 1,
   "leave_type": "vacation",
   "max_days": 20
}
```

#### **Response**
```json
{
   "id": 1,
   "organization_id": 1,
   "leave_type": "vacation",
   "max_days": 20
}

```

## 4. High-Level Architecture

### Components:
- **FastAPI Backend** - Handles API requests, authentication, and business logic.
- **PostgreSQL Database (Supabase)** - Stores users, leave requests, and policies and organizations
- **Auth Service (JWT-based)** - Ensures secure access for employees and admins.
- **API Gateway** - Manages rate limiting and security for multi-tenant access.
- **Job Scheduler** - Handles leave balance updates and notifications.

### Scalability Considerations:
✅ **Load Balancing:** Use multiple API instances behind a load balancer.  
✅ **Caching:** Store frequently accessed data (e.g., leave balances) in Redis.  
✅ **Rate Limiting:** Prevent abuse of leave request submissions.  
✅ **Database Indexing:** Optimize queries on `user_id`, `organization_id`, and `status`.  

---

## 5. Implementation & Rollout Plan

### **Step 1: Database Setup & Models** 
- Set up the backend with FastAPI.
- Design database schema.

### **Step 2: API Development**
- Implement endpoints for leave requests and approvals.
- Deploy a basic Swagger UI for API testing.

### **Step 3: Authentication & Authorization** 
- Implement JWT authentication for employees and admins.
- Restrict leave approval to admin users.

### **Step 4: Testing & Deployment**
- Unit tests (pytest) for API endpoints.
- Dockerize the backend for easy deployment.
- Deploy to **AWS/GCP/Supabase** with auto-scaling.

### **Step 5 (optional): Enhancements** 
- Authentication & Authorization (JWT-based login).
- Organization-level multi-tenancy.
- Email/Slack notifications for leave approvals.


---

## 6. Workload Estimation  (Pro Solution)

| **Task**                                  | **Effort (Hours)** |
|-------------------------------------------|--------------------|
| **Database setup & migrations**           | 4h  |
| **API development (CRUD for Leave Requests & Policies)** | 6h  |
| **Authentication (JWT-based User Management)** | 6h  |
| **Unit & Integration Testing**            | 4h  |
| **Deployment & CI/CD Pipeline Setup**     | 4h  |
| **Multi-Tenancy Implementation** (via Docker – separate instances per client) | 10h  |
| **Alternative Multi-Tenancy Implementation** (Shared DB, tenant-based access) | 16h  |
| **Documentation & Final Review**          | 2h  |
| **Total Estimated Effort** *(without multi-tenancy)* | **26h** |
| **Total Estimated Effort** *(with multi-tenancy via Docker)* | **36h** |
| **Total Estimated Effort** *(with multi-tenancy via shared DB)* | **42h** |
| ** (extra)Frontend Implementation (React Native App)** | 8h  |

---

### ** Deployment Considerations**
- **For Single-Tenant Deployment:** Host backend as a single FastAPI instance with one PostgreSQL database.
- **For Multi-Tenancy via Docker:** Each organization gets a separate backend container with an independent database. 
- **For Multi-Tenancy via Shared DB:** Implement a **tenant_id** column in all tables, with row-level security (RLS).

---

🚀 ** Test frontend with react-native App using ExpoGo to make it easier :) 
