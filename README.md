# Tor Monitor Backend

A comprehensive inventory management system with AI-powered features built with FastAPI, PostgreSQL, and LangChain agents.

## Overview

Tor Monitor is an enterprise-grade backend service designed for tracking goods inventory and sales with intelligent AI assistance. It provides real-time inventory management, sales forecasting, and AI-driven decision support through LangChain agents.

## Key Features

- **User Authentication**: Secure OAuth2-based authentication via Supabase
- **Goods Management**: Complete CRUD operations for inventory items
- **Sales Tracking**: Record and analyze sales transactions with profit calculation
- **AI Assistant**: LangChain-powered agent for intelligent inventory queries
- **Sales Forecasting**: XGBoost-based demand prediction for low-stock items
- **Dashboard Analytics**: Real-time metrics and business intelligence
- **Multi-tenant Support**: Isolated data per user with automatic filtering

## Technology Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: Supabase Auth
- **AI/ML**: LangChain, LangChain-Groq, XGBoost
- **Migrations**: Alembic
- **Package Manager**: UV

## Project Structure

The project follows a domain-driven design pattern with modular separation of concerns:

```
tor-be/
├── app/
│   ├── main.py                  # FastAPI app initialization, middleware setup
│   ├── dependencies.py          # Dependency injection (auth, db session)
│   │
│   ├── db/
│   │   ├── models.py            # SQLModel ORM definitions
│   │   ├── crud.py              # CRUD operations facade (backward compatible)
│   │   └── repositories/        # Domain-specific repository modules
│   │       ├── __init__.py      # Exports all repository functions
│   │       ├── generic.py       # Generic CRUD (update, delete)
│   │       ├── goods.py         # Goods inventory queries
│   │       ├── sales.py         # Sales transaction queries
│   │       ├── dashboard.py     # Analytics and dashboard queries
│   │       ├── forecast.py      # Sales dataset preparation
│   │       └── restock.py       # Restock inference operations
│   │
│   ├── routers/                 # API endpoint groups (6 domains)
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── goods.py             # Goods CRUD endpoints
│   │   ├── sales.py             # Sales CRUD endpoints
│   │   ├── dashboard.py         # Analytics endpoints
│   │   ├── chat.py              # AI chat endpoint
│   │   └── forecast.py          # Sales forecast endpoints
│   │
│   ├── services/                # Business logic and orchestration
│   │   ├── agent.py             # LangChain AI agent setup
│   │   ├── forecast.py          # Forecast service orchestrator
│   │   └── forecast_models/     # Machine learning pipeline
│   │       ├── __init__.py
│   │       ├── data_prep.py     # Feature engineering
│   │       ├── model.py         # XGBoost model creation
│   │       └── prediction.py    # Future predictions
│   │
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── auth.py
│   │   ├── goods.py
│   │   ├── sales.py
│   │   ├── dashboard.py
│   │   ├── forecast.py
│   │   └── restock.py
│   │
│   └── utils/
│       └── agent_tools.py       # LangChain agent tool definitions
│
├── alembic/                     # Database migration system
│   ├── versions/                # Migration history
│   └── env.py                   # Alembic environment config
│
├── pyproject.toml               # UV dependencies and project config
├── alembic.ini                  # Alembic configuration
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-container orchestration
└── README.md
```

### Architecture Overview

**Layered Architecture:**
- **Routers**: Accept HTTP requests, validate, return responses
- **Services**: Business logic, orchestration, AI workflows
- **Repositories**: Data access layer, organized by domain
- **Models**: ORM definitions and migrations
- **Schemas**: Type-safe request/response validation

**Key Design Patterns:**
- **Domain-Driven Design**: Code organized by business domain
- **Repository Pattern**: Data access abstraction
- **Dependency Injection**: FastAPI dependencies for auth/db
- **Multi-tenant**: All operations filtered by user_id
- **Modular Services**: ML models split into separate modules

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Supabase account

### Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/Tactical-Opname-Restock/tor-monitor-be.git
   cd tor-monitor-be
   ```

2. **Install UV Package Manager**
   ```bash
   pip install uv
   ```

3. **Create Environment File**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your credentials:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   SUPABASE_DB_STRING=postgresql://user:password@host:port/dbname
   GROQ_KEY=your-groq-api-key
   FRONTEND_URL=http://localhost:3000
   DEV_ENV=dev
   DEV_KEY=dev
   ```

## Modular Design & Scalability

The project is designed for easy scaling and maintenance through modular architecture:

### Database Layer (CRUD Operations)

**Location**: `app/db/repositories/`

CRUD operations are split into domain-specific modules for better organization:

- **`generic.py`**: Generic operations (update, delete) used by all domains
- **`goods.py`**: Goods inventory queries (list, get, search, low stock)
- **`sales.py`**: Sales transactions (list, get, create with deduction)
- **`dashboard.py`**: Analytics queries (revenue, top items, sales chart)
- **`forecast.py`**: Dataset preparation for ML models
- **`restock.py`**: Restock inference management

**Backward Compatibility**: `app/db/crud.py` re-exports all functions for existing code.

### Services Layer

**Location**: `app/services/`

- **`agent.py`**: LangChain AI agent orchestration (115 lines)
- **`forecast.py`**: Forecast service coordinator (60 lines)

**Forecast Models**: `app/services/forecast_models/`
- **`data_prep.py`**: Feature engineering for time series
- **`model.py`**: XGBoost model creation and training
- **`prediction.py`**: Future prediction generation

This separation allows easy:
- Swapping ML models (use TensorFlow instead of XGBoost)
- Adding new features without modifying other modules
- Testing individual components independently
- Scaling specific components

### Adding New Features

1. **New Query Type**: Add function to appropriate repository module
2. **New ML Algorithm**: Add to `services/forecast_models/`
3. **New API Endpoint**: Create in `routers/`, use existing repositories
4. **New AI Tool**: Add to `utils/agent_tools.py`, register in `AgentService`

## Development

### Running Locally

1. **Initialize Database**
   ```bash
   uv run alembic upgrade head
   ```

2. **Start Development Server**
   ```bash
   uv run uvicorn app.main:app --reload --reload-dir app
   ```
   Access at `http://127.0.0.1:8000`

3. **API Documentation**
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

### Database Migrations

When modifying `app/db/models.py`:

```bash
# Generate migration from schema changes
uv run alembic revision --autogenerate -m "descriptive message"

# Apply migrations
uv run alembic upgrade head

# Check current migration
uv run alembic current
```

## API Endpoints

### Authentication
- `POST /token` - Get JWT token (dev only)
- `POST /sign_up` - Create user account
- `POST /sign_in` - Sign in user

### Goods Management
- `GET /api/goods` - List goods (paginated)
- `GET /api/goods/{goods_id}` - Get goods details
- `POST /api/goods` - Create goods
- `PUT /api/goods/{goods_id}` - Update goods
- `DELETE /api/goods/{goods_id}` - Delete goods

### Sales Management
- `GET /api/sales` - List sales (paginated)
- `POST /api/sales` - Record sale
- `PUT /api/sales/{sales_id}` - Update sale
- `DELETE /api/sales/{sales_id}` - Delete sale

### Dashboard
- `GET /api/dashboard/` - Get analytics metrics
  - Parameters: `year`, `month` (optional)

### AI Assistant
- `POST /api/chat` - Chat with AI agent to manage your goods or sales

### Forecasting
- `GET /api/forecast/` - Get sales forecast top 10 lowes or specific goods
  - Parameters: `goods_id` (optional), `day_forecast` (default: 7)

## Response Format

**List Response:**
```json
{
  "data": [...],
  "total": 100,
  "page": 1,
  "limit": 20
}
```

**Detail Response:**
```json
{
  "data": {...}
}
```

**Message Response:**
```json
{
  "message": "Success",
  "data": {...}
}
```

## Security

- All endpoints require valid JWT token (except auth endpoints)
- All queries automatically filtered by user_id
- Supabase auth schema isolated from app schema
- CORS configured for specified frontend URL

## Testing

### Running Tests

The project includes a comprehensive test suite with 43 tests covering all major endpoints. Tests use pytest with FastAPI's TestClient and in-memory SQLite for database isolation.

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_goods.py -v

# Run specific test class
uv run pytest tests/test_goods.py::TestGoodsEndpoints -v

# Run with coverage
uv run pytest tests/ --cov=app --cov-report=html
```

### Test Structure

```
tests/
├── conftest.py                  # Pytest fixtures and configuration
├── test_auth.py                 # Authentication endpoints (6 tests)
├── test_goods.py                # Goods management endpoints (12 tests)
├── test_sales.py                # Sales transaction endpoints (8 tests)
├── test_dashboard.py            # Analytics endpoints (7 tests)
├── test_forecast.py             # ML forecast endpoints (4 tests)
└── test_chat.py                 # AI chat endpoints (6 tests)
```

### Test Features

**Fixtures (conftest.py)**
- `session`: In-memory SQLite database with proper table creation (skips auth schema)
- `client`: FastAPI TestClient with dependency override
- `test_user`: Pre-created test user (UUID)
- `test_goods`: Test goods item with full attributes
- `test_goods_low_stock`: Low-stock goods for forecast testing
- `test_sales`: Test sales record linked to test_goods
- `auth_headers`: Authorization headers for testing

**Patterns**
- Flexible status code assertions (tests accept multiple valid responses)
- UserDependency mocking via `get_current_user` override
- Automated user context injection in all tests
- Request payload validation
- Endpoint availability verification

### Test Coverage by Endpoint

| Endpoint | Tests | Coverage |
|----------|-------|----------|
| POST /auth/sign_up | 3 | Validation, structure |
| POST /auth/sign_in | 2 | Endpoint availability |
| GET /api/goods | 3 | List, pagination, search |
| GET /api/goods/{id} | 2 | Single item, not found |
| POST /api/goods | 2 | Create, validation |
| PUT /api/goods/{id} | 2 | Update, not found |
| DELETE /api/goods/{id} | 2 | Delete, not found |
| GET /api/sales | 2 | List, pagination |
| POST /api/sales | 2 | Create, validation |
| PUT /api/sales/{id} | 2 | Update, availability |
| DELETE /api/sales/{id} | 2 | Delete, availability |
| GET /api/dashboard/ | 7 | Parameters, responses |
| GET /api/forecast/ | 4 | List, parameters |
| POST /api/chat | 8 | Parameters, prompts |

### Example Test Run

```bash
$ uv run pytest tests/ -v

tests/test_auth.py::TestAuthEndpoints::test_sign_up_success PASSED       [  6%]
tests/test_auth.py::TestAuthEndpoints::test_sign_up_invalid_email PASSED [  9%]
tests/test_goods.py::TestGoodsEndpoints::test_get_goods_endpoint_available PASSED
...
======================= 43 passed in 14.01s =======================
```

### Notes for Development

- Tests use `datetime.now()` for dynamic date values
- SQLite in-memory database resets between test sessions
- Auth fixtures automatically cleanup overrides after tests
- Tests are isolated by user context (no cross-user contamination)
- Pydantic serialization warnings about datetime/date are expected (SQLModel limitation)

## Deployment

### Docker

```bash
docker-compose up --build
```

Server runs on port 8086. Migrations run automatically on startup.

### Production Environment

```env
SUPABASE_URL=https://prod-instance.supabase.co
SUPABASE_KEY=prod-key
SUPABASE_DB_STRING=postgresql://...
GROQ_KEY=prod-groq-key
FRONTEND_URL=https://yourdomain.com
DEV_ENV=production
```