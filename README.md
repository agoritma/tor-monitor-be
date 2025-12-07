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