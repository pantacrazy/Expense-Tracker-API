# Expense Tracker API
https://roadmap.sh/projects/expense-tracker-api
A RESTful API for personal expense management built with Django REST Framework, featuring JWT authentication, advanced filtering, and comprehensive test coverage.

## Key Features

- ✅ **Secure JWT authentication** (registration, login, token refresh)
- 🔍 **Full CRUD operations** for expense types and expenses
- 📅 **Advanced date filtering** (ranges, recent weeks/months)
- 🧪 **Comprehensive test coverage** with Django TestCase
- 🔒 **Authentication-based permissions** for all operations
- 📊 **Robust data serialization** with DRF
- ⚙️ **Custom filters** for complex queries

## Technical Requirements

- Python 3.9+
- Django 4.1+
- Django REST Framework
- Simple JWT
- django-filter
- python-dateutil

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/expense-tracker-api.git
cd expense-tracker-api
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Run development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
| Method | Endpoint          | Description                |
|--------|-------------------|----------------------------|
| POST   | `/api/register/user/` | Register new user          |
| POST   | `/api/login/`    | Login (obtain tokens)      |
| POST   | `/api/token/refresh/` | Refresh access token     |

### Expense Types
| Method | Endpoint                 | Description                     |
|--------|--------------------------|---------------------------------|
| GET    | `/api/expense-types/`        | List all expense types          |
| POST   | `/api/expense-types/`        | Create new expense type         |
| GET    | `/api/expense-types/{id}/`   | Get expense type details        |
| PUT    | `/api/expense-types/{id}/`   | Update expense type             |
| DELETE | `/api/expense-types/{id}/`   | Delete expense type             |

### Expenses
| Method | Endpoint          | Description                     |
|--------|-------------------|---------------------------------|
| GET    | `/api/expenses/`      | List all expenses (with filters)|
| POST   | `/api/expenses/`      | Create new expense              |
| GET    | `/api/expenses/{id}/` | Get expense details             |
| PUT    | `/api/expenses/{id}/` | Update expense                  |
| DELETE | `/api/expenses/{id}/` | Delete expense                  |

## Available Expense Filters

| Parameter     | Example                      | Description                                  |
|---------------|------------------------------|----------------------------------------------|
| `start_date`  | `?start_date=2023-08-01`     | Expenses from this date (inclusive)          |
| `end_date`    | `?end_date=2023-08-31`       | Expenses up to this date (inclusive)         |
| `week`        | `?week=2`                    | Expenses from last 2 weeks                  |
| `last_months` | `?last_months=3`             | Expenses from last 3 months                 |

**Combined example:**  
`GET /expenses/?start_date=2023-08-01&end_date=2023-08-15&type=2`

## Usage Examples

### User Registration
```http
POST /api/expense-types/
Content-Type: application/json

{
  "username": "new_user",
  "password": "secure_password",
  "email": "user@example.com"
}
```

### Creating an Expense
```http
POST /api/expenses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Groceries",
  "amount": 85.50,
  "type": 1,
  "date": "2023-08-04"
}
```

### Filtering Expenses
```http
GET /api/expenses/?week=2
Authorization: Bearer <access_token>
```

## Running Tests

To execute the full test suite:

```bash
python manage.py expense.tests
```

Test coverage includes:
- User registration and authentication
- CRUD operations for expense types
- CRUD operations for expenses
- Advanced date filtering
- Error handling and edge cases
- Data validation and permissions

## Project Structure

```
expense-tracker-api/
├── api/    
    ├── expense/               # Main application
        ├── migrations/        # Database migrations
        ├── tests.py             # Automated tests
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── filterset.py         # Custom filters
        ├── models.py          # Data models
        ├── serializers.py     # Serializers
        ├── urls.py            # API routes
        ├── permissions.py      # Permissions
        └── views.py           # Views

├── manage.py
├── README.md
├── requirements.txt       # Dependencies
└── api/          # Project configuration
    ├── __init__.py
    ├── asgi.py
    ├── settings.py        # Configuration
    ├── urls.py            # Main routes
    └── wsgi.py
```

