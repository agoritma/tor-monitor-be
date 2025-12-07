"""Pytest configuration and fixtures for testing."""

from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.dependencies import get_db_session
from app.main import app
from app.db.models import User, Goods, Sales


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    # Create only app tables, skip auth schema (SQLite doesn't support schemas)
    for table in SQLModel.metadata.tables.values():
        if table.schema is None:  # Skip tables with schema (auth.users)
            table.create(engine, checkfirst=True)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create FastAPI test client with test database."""

    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Create a test user in the database."""
    user = User(id=uuid4())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_goods")
def test_goods_fixture(session: Session, test_user: User) -> Goods:
    """Create test goods in the database."""
    goods = Goods(
        id=uuid4(),
        user_id=test_user.id,
        name="Test Product",
        category="Electronics",
        price=50000.0,
        stock_quantity=100,
        created_at=datetime.now(),
    )
    session.add(goods)
    session.commit()
    session.refresh(goods)
    return goods


@pytest.fixture(name="test_goods_low_stock")
def test_goods_low_stock_fixture(session: Session, test_user: User) -> Goods:
    """Create test goods with low stock."""
    goods = Goods(
        id=uuid4(),
        user_id=test_user.id,
        name="Low Stock Product",
        category="Home",
        price=25000.0,
        stock_quantity=5,
        created_at=datetime.now(),
    )
    session.add(goods)
    session.commit()
    session.refresh(goods)
    return goods


@pytest.fixture(name="test_sales")
def test_sales_fixture(session: Session, test_user: User, test_goods: Goods) -> Sales:
    """Create test sales record."""
    sales = Sales(
        id=uuid4(),
        user_id=test_user.id,
        goods_id=test_goods.id,
        quantity=10,
        sale_date=datetime.now(),
        total_profit=500000.0,
        created_at=datetime.now(),
    )
    session.add(sales)
    session.commit()
    session.refresh(sales)
    return sales


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user: User) -> dict:
    """Create authorization headers with test user ID."""
    # Note: In production, this would be a JWT token
    # For testing, we mock the dependency
    return {"X-User-ID": str(test_user.id)}
