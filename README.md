# Cristales SaaS

Backend API for Cristales SaaS - A comprehensive management system for glass/crystal businesses.

## Features

- **Multi-tenant Architecture**: Support for multiple business tenants
- **Inventory Management**: Complete CRUD operations for warehouses, stock configurations, inventory movements, and alerts
- **Business Modules**: Catalog, clients, commissions, companies, billing, orders, payments, profiles, reports, users, vehicles, and zones
- **Authentication & Authorization**: JWT-based auth with role-based access control (RBAC)
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Alembic**: Database migration tool
- **Pydantic**: Data validation
- **Docker**: Containerization

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (or use Docker container)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cristales-saas
```

2. Set up the database:
```bash
docker compose -f infra/docker-compose.dev.yml up -d
```

3. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
cd ..
pip install -r requirements.txt  # For root-level scripts
```

4. Set up environment variables:
Copy `.env.example` to `.env` and configure as needed.

5. Run database migrations:
```bash
cd backend
alembic upgrade head
```

### Running the Application

You can run the application from either the root directory or the backend directory:

#### From Root Directory (Recommended)
```bash
python run.py
```

#### From Backend Directory
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Project Structure

```
cristales-saas/
├── backend/                 # Main application code
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── core/           # Configuration and core functionality
│   │   ├── modules/        # Business modules
│   │   │   ├── inventario/ # Inventory management
│   │   │   ├── catalogo/   # Product catalog
│   │   │   └── ...         # Other modules
│   │   ├── rbac/           # Role-based access control
│   │   └── tenants/        # Multi-tenancy support
│   ├── alembic/            # Database migrations
│   └── requirements.txt    # Python dependencies
├── infra/                   # Infrastructure (Docker, nginx)
├── docs/                    # Documentation
├── frontend/                # Frontend application
├── run.py                   # Launcher script (root directory)
└── app/                     # Alternative app entry (root directory)
```

## Development

### Database Operations

- **Create migration**: `cd backend && alembic revision --autogenerate -m "message"`
- **Run migrations**: `cd backend && alembic upgrade head`
- **Rollback**: `cd backend && alembic downgrade -1`

### Testing

```bash
cd backend
pytest
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

[Add license information]
