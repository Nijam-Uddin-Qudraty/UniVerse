# 🎓 University Information System — Project Plan

## 1. Project Overview
- **Purpose:** Build a scalable, modular web application for managing university-level operations.
- **Tech Stack:**  
  - Backend: Python, Django + Django REST Framework (DRF)  
  - Database: PostgreSQL (preferred), MySQL as alternative  
  - Frontend: React (with Tailwind or Next.js optional)  
  - Deployment: Docker, CI/CD pipelines, Nginx/Gunicorn, AWS/Azure/Local servers  
- **Core Modules:**  
  1. Academics (Departments, Programs, Courses, Faculty, Students, Enrollments)  
  2. Library (Books, Book Loans)  
  3. Scholarships & Admissions  
  4. Events & Notices  
  5. Research & Publications  
  6. Feedback & Helpdesk  

---

## 2. Stakeholders & Roles
- **Super Admin:** Full control (create departments, assign roles, system configuration).  
- **Faculty:** Create courses, manage sections, upload grades, publish research.  
- **Students:** Enroll in courses, apply for scholarships, borrow books.  
- **Staff:** Manage admissions, process library loans, handle notices/events.  
- **Librarian:** Dedicated staff managing book inventory and loans.  
- **Applicants (External Users):** Apply for admission/scholarship, limited access.  
- **IT / DevOps Team:** Maintain infrastructure, backups, and system monitoring.  

---

## 3. Functional Requirements

### 3.1 Academics
- CRUD operations for Departments, Programs, Courses, Course Sections.
- Student enrollments → auto-check prerequisites.
- Faculty assignment to sections.
- Grade submission with versioning (no overwrite, only update via “new row” or audit trail).

### 3.2 Library
- Manage Books with copies available.  
- BookLoans: borrowing, returning, overdue fine tracking.  
- Prevent multiple active loans for the same book copy.  

### 3.3 Scholarships & Admissions
- Students apply for scholarships (with eligibility checks).  
- Applications must be auditable (no hard delete, only status updates: pending → approved/denied).  
- Admission workflow: applicant → student creation upon approval.  

### 3.4 Events & Notices
- Faculty/Staff/Admin can post notices/events.  
- Visibility: public, department-only, or role-based.  
- Events should allow multi-organizer (User + Department).  

### 3.5 Research & Publications
- Faculty upload publications with metadata (year, journal/conference).  
- Support file uploads (PDFs).  
- Ensure DOIs or external identifiers are stored.  

### 3.6 Feedback & Helpdesk
- Students/Staff can submit feedback/complaints.  
- Assignable to staff/faculty for resolution.  
- Escalation rules for unresolved tickets.  

---

## 4. Non-Functional Requirements
- **Scalability:** Must handle 10k+ students & multiple campuses.  
- **Performance:** <200ms API response for common queries.  
- **Availability:** 99.9% uptime target.  
- **Data Integrity:** Enforce FK relationships, prevent orphan rows.  
- **Extensibility:** Allow easy addition of Hostel/Finance modules.  

---

## 5. Data Design & SQL Guidelines

### 5.1 General
- **Primary Keys:** Always use surrogate keys (`id SERIAL/BIGSERIAL`).  
- **Foreign Keys:** Enforce with `ON DELETE CASCADE` where logical (e.g., Enrollments).  
- **Soft Deletes:** Use `is_active` or `status` instead of deleting records.  
- **Timestamps:** Every table gets `created_at`, `updated_at`.

### 5.2 Row Update Rules
- **Grades:** Never overwrite; insert new record into `GradeHistory`.  
- **BookLoans:** `return_date` updated only once; new borrow → new row.  
- **ScholarshipApplications:** Status transitions only; don’t delete.  
- **Admissions:** Once approved, applicant data locked, and student profile created.  
- **Events/Notices:** Updates allowed, but old versions logged in `AuditLog`.

### 5.3 Exceptions & Special Cases
- **Faculty leaving university:** Keep profile but mark inactive (retain publications).  
- **Students suspended:** Keep record, mark `status = suspended`, no deletions.  
- **Books lost:** Mark loan `status = lost`, keep row for accountability.  

---

## 6. API & Integration
- REST APIs (JSON) with JWT authentication.  
- Rate limiting for public endpoints (admissions, scholarship applications).  
- Support for integration with external services:  
  - Payment Gateway (for fines, application fees).  
  - Email/SMS notifications.  

---

## 7. Security & Compliance
- Use role-based access control (RBAC).  
- Encrypt sensitive fields (passwords with Argon2/Bcrypt, PII if required).  
- Comply with GDPR-like rules (right to access/delete personal data).  
- Enforce HTTPS across all environments.  

---

## 8. Deployment & DevOps
- **Environments:** Dev → Staging → Production.  
- **Migrations:** Use Django `makemigrations`/`migrate` with versioning.  
- **Backups:** Daily full DB backup, 15-min incremental snapshots.  
- **Monitoring:** Prometheus + Grafana or Datadog.  
- **CI/CD:** GitHub Actions or GitLab CI for automated testing & deployment.  

---

## 9. Maintenance & Updates
- **Patch cycles:** Monthly security patches.  
- **Data archiving:** Graduated students archived after 5 years.  
- **Schema updates:** Version-controlled migrations; backward compatibility required.  
- **Audit logging:** All critical updates logged in `AuditLog` table (who, when, what changed).  

---

## 10. Risks & Mitigations
- **Data loss risk** → Frequent backups & test restores.  
- **Unauthorized access** → Strong RBAC & 2FA for admins.  
- **Scalability bottlenecks** → Database indexing & query optimization.  
- **Staff turnover** → Documentation & onboarding guides maintained.  

---

## 11. Deliverables
- ER Diagrams (Full + Per Module).  
- SQL Schema (DDL).  
- Django Models & DRF APIs.  
- Admin Panel for staff/faculty.  
- Documentation: User Manual + Developer Guide.  

---

## 12. Timeline (High-Level)
1. **Month 1–2:** Requirements gathering, ER design, project setup.  
2. **Month 3–4:** Implement Academics & User module.  
3. **Month 5:** Library + Scholarships.  
4. **Month 6:** Events/Notices + Research.  
5. **Month 7:** Security, performance tuning, final testing.  
6. **Month 8:** Deployment & Training.  

---
