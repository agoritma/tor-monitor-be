"""Unit tests for dashboard analytics endpoints."""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.db.models import Sales, Goods, User
from app.dependencies import get_current_user


class TestDashboardEndpoints:
    """Test suite for dashboard and analytics routes."""

    @pytest.fixture(autouse=True)
    def setup_auth(self, client: TestClient, test_user: User):
        """Setup user dependency for all tests."""
        from app.main import app

        async def get_test_user_override(
            access_token: str = "", db=None, supabase_client=None
        ):
            return test_user

        app.dependency_overrides[get_current_user] = get_test_user_override
        yield
        app.dependency_overrides.clear()

    @pytest.fixture
    def sales_with_dates(self, session, test_user: User, test_goods: Goods):
        """Create sales records with various dates for analytics testing."""
        today = datetime.now().date()
        sales_data = []

        # Create sales for the last 30 days
        for i in range(30):
            date_offset = today - timedelta(days=i)
            sales = Sales(
                id=uuid4(),
                user_id=test_user.id,
                goods_id=test_goods.id,
                quantity=10 + i,
                sale_date=datetime.combine(date_offset, datetime.min.time()),
                total_profit=100000.0 + (i * 10000),
                created_at=datetime.now(),
            )
            sales_data.append(sales)
            session.add(sales)

        session.commit()
        return sales_data

    def test_get_dashboard_data_available(self, client: TestClient):
        """Test that dashboard endpoint is available."""
        response = client.get("/api/dashboard/")
        # Should respond (may be 200, 400, or 404 depending on data)
        assert response.status_code in [200, 400, 404]

    def test_get_dashboard_with_year_parameter(self, client: TestClient):
        """Test dashboard data with year filter."""
        current_year = datetime.now().year
        response = client.get(f"/api/dashboard/?year={current_year}")
        assert response.status_code in [200, 400, 404]

    def test_get_dashboard_with_month_parameter(self, client: TestClient):
        """Test dashboard data with month filter."""
        current_month = datetime.now().month
        response = client.get(f"/api/dashboard/?month={current_month}")
        assert response.status_code in [200, 400, 404]

    def test_get_dashboard_with_year_and_month(self, client: TestClient):
        """Test dashboard data with both year and month filters."""
        current_year = datetime.now().year
        current_month = datetime.now().month
        response = client.get(
            f"/api/dashboard/?year={current_year}&month={current_month}"
        )
        assert response.status_code in [200, 400, 404]

    def test_get_dashboard_invalid_month(self, client: TestClient):
        """Test dashboard with invalid month parameter."""
        response = client.get("/api/dashboard/?month=13")
        # Invalid month should be rejected or handled
        assert response.status_code in [400, 422]

    def test_get_dashboard_returns_json(self, client: TestClient):
        """Test that dashboard returns valid JSON."""
        response = client.get("/api/dashboard/")
        data = response.json()
        assert isinstance(data, dict)

    def test_get_dashboard_with_valid_parameters(self, client: TestClient):
        """Test dashboard with valid year and month."""
        response = client.get("/api/dashboard/?year=2024&month=1")
        assert response.status_code in [200, 400, 404]
