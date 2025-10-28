# Employee Management System

A complete full-stack web application for managing employees, built with Django REST Framework (backend) and React with TypeScript (frontend).

## Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (HR and Employee roles)
- Secure login/logout functionality

### Employee Management
- Add, edit, and delete employees (HR only)
- Employee profiles with comprehensive information
- Department and designation management

### Leave Management
- Employee leave applications
- HR approval/rejection workflow
- Leave type categorization (Sick, Casual, Annual, etc.)
- Leave history tracking

### Attendance Management
- Daily attendance marking
- Attendance status tracking (Present, Absent, Late, Half Day)
- Monthly attendance reports
- Attendance summary statistics

### Payroll Management
- Salary slip generation
- Bulk payroll processing (HR only)
- Salary components (basic, allowances, deductions)
- Tax and PF calculations

### Performance Management
- Performance review system
- Multi-criteria rating system
- Performance history tracking
- Goal setting and feedback

## Technology Stack

### Backend
- **Django 5.2.5**: Web framework
- **Django REST Framework**: API development
- **JWT Authentication**: Secure token-based auth
- **SQLite**: Database (development)
- **PostgreSQL**: Database (production ready)
- **Python 3.13**: Programming language

### Frontend
- **React 19**: Frontend framework
- **TypeScript**: Type-safe JavaScript
- **Material-UI (MUI)**: UI component library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls

## Project Structure

```
Employee Management System/
├── backend/                    # Django backend
│   ├── employee_management/    # Main Django project
│   ├── employees/             # Employee app
│   ├── leaves/                # Leave management app
│   ├── attendance/            # Attendance tracking app
│   ├── payroll/               # Payroll management app
│   ├── performance/           # Performance review app
│   ├── venv/                  # Virtual environment
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
└── frontend/                  # React frontend
    ├── src/
    │   ├── components/        # Reusable components
    │   ├── contexts/          # React contexts
    │   ├── pages/             # Page components
    │   └── App.tsx            # Main app component
    ├── public/                # Static files
    └── package.json           # Node.js dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.13+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (already created):**
   - Email: admin@example.com
   - Password: admin123

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```
   Backend will be available at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   Frontend will be available at: http://localhost:3000

## Default Login Credentials

### HR Admin
- **Email:** admin@example.com
- **Password:** admin123
- **Role:** HR (Full access to all features)

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Employees
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee (HR only)
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee (HR only)
- `DELETE /api/employees/{id}/` - Delete employee (HR only)

### Leaves
- `GET /api/leaves/` - List leaves
- `POST /api/leaves/` - Apply for leave
- `GET /api/leaves/{id}/` - Get leave details
- `PATCH /api/leaves/{id}/approve-reject/` - Approve/reject leave (HR only)

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/mark/` - Mark attendance
- `GET /api/attendance/monthly/` - Monthly attendance report

### Payroll
- `GET /api/payroll/` - List payroll records
- `POST /api/payroll/` - Create payroll (HR only)
- `POST /api/payroll/generate-bulk/` - Bulk payroll generation (HR only)

### Performance
- `GET /api/performance/` - List performance reviews
- `POST /api/performance/` - Create performance review (HR only)
- `GET /api/performance/my-reviews/` - Get user's reviews

## Features by Role

### HR Features
- ✅ Dashboard with employee statistics
- ✅ Employee management (CRUD operations)
- ✅ Leave approval/rejection
- ✅ Attendance management
- ✅ Payroll generation
- ✅ Performance review creation
- ✅ Bulk operations

### Employee Features
- ✅ Personal dashboard
- ✅ Profile management
- ✅ Leave applications
- ✅ Attendance marking
- ✅ Payslip viewing
- ✅ Performance review viewing

## Development Status

### Completed
- ✅ Backend API development
- ✅ Database models and migrations
- ✅ Authentication system
- ✅ Basic frontend structure
- ✅ Login functionality
- ✅ Dashboard layouts
- ✅ Routing setup

### In Progress
- 🔄 Frontend forms and data management
- 🔄 API integration
- 🔄 Complete CRUD operations

### Future Enhancements
- 📝 Email notifications
- 📝 File upload for documents
- 📝 Advanced reporting
- 📝 Mobile responsiveness
- 📝 Dark mode support
- 📝 Export functionality (PDF, Excel)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and demonstration purposes.

## Support

For any questions or issues, please refer to the documentation or create an issue in the repository.
