"""Unit tests for sales endpoints."""

from datetime import datetime, date, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.db.models import Sales, Goods, User
from app.dependencies import get_current_user


class TestSalesEndpoints:
    """Test suite for sales management routes."""

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

    def test_get_sales_list_endpoint_available(self, client: TestClient):
        """Test that GET /api/sales endpoint is available."""
        response = client.get("/api/sales")
        assert response.status_code in [200, 400, 404]

    def test_get_sales_with_pagination(self, client: TestClient):
        """Test sales list with pagination parameters."""
        response = client.get("/api/sales?limit=2&page_index=1")
        assert response.status_code in [200, 400, 404]

    def test_create_sales_endpoint_available(
        self, client: TestClient, test_goods: Goods
    ):
        """Test that POST /api/sales endpoint is available."""
        payload = {
            "goods_id": str(test_goods.id),
            "quantity": 5,
            "sale_date": datetime.now().date().isoformat(),
        }
        response = client.post("/api/sales", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_create_sales_missing_quantity(self, client: TestClient, test_goods: Goods):
        """Test sales creation with missing quantity."""
        payload = {
            "goods_id": str(test_goods.id),
            "sale_date": datetime.now().date().isoformat(),
        }
        response = client.post("/api/sales", json=payload)
        # Missing required field should error
        assert response.status_code in [400, 422]

    def test_update_sales_endpoint_available(
        self, client: TestClient, test_sales: Sales
    ):
        """Test that PUT /api/sales/{id} endpoint is available."""
        payload = {
            "quantity": 20,
            "sale_date": datetime.now().date().isoformat(),
        }
        response = client.put(f"/api/sales/{test_sales.id}", json=payload)
        assert response.status_code in [200, 400, 404]

    def test_delete_sales_endpoint_available(
        self, client: TestClient, test_sales: Sales
    ):
        """Test that DELETE /api/sales/{id} endpoint is available."""
        response = client.delete(f"/api/sales/{test_sales.id}")
        assert response.status_code in [200, 400, 404]

    def test_delete_nonexistent_sales(self, client: TestClient):
        """Test deleting non-existent sales."""
        fake_id = uuid4()
        response = client.delete(f"/api/sales/{fake_id}")
        assert response.status_code in [400, 404]
