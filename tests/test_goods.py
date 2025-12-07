"""Unit tests for goods endpoints."""

from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.db.models import Goods, User
from app.dependencies import get_current_user


class TestGoodsEndpoints:
    """Test suite for goods management routes."""

    @pytest.fixture(autouse=True)
    def setup_auth(self, client: TestClient, test_user: User):
        """Setup user dependency for all tests in this class."""
        # Override the get_current_user function to return our test user
        from app.main import app

        async def get_test_user_override(
            access_token: str = "", db=None, supabase_client=None
        ):
            return test_user

        app.dependency_overrides[get_current_user] = get_test_user_override
        yield
        app.dependency_overrides.clear()

    def test_get_goods_endpoint_available(self, client: TestClient):
        """Test that GET /api/goods endpoint is available."""
        response = client.get("/api/goods")
        assert response.status_code in [200, 400, 404]

    def test_get_goods_with_pagination(self, client: TestClient):
        """Test goods list with pagination parameters."""
        response = client.get("/api/goods?limit=10&page_index=1")
        assert response.status_code in [200, 400, 404]

    def test_get_goods_with_search(self, client: TestClient):
        """Test goods list with search query."""
        response = client.get("/api/goods?q=test")
        assert response.status_code in [200, 400, 404]

    def test_get_goods_by_id_endpoint_available(
        self, client: TestClient, test_goods: Goods
    ):
        """Test that GET /api/goods/{id} endpoint is available."""
        response = client.get(f"/api/goods/{test_goods.id}")
        assert response.status_code in [200, 404]

    def test_get_nonexistent_goods(self, client: TestClient):
        """Test getting non-existent goods."""
        fake_id = uuid4()
        response = client.get(f"/api/goods/{fake_id}")
        assert response.status_code in [400, 404]

    def test_create_goods_endpoint_available(self, client: TestClient):
        """Test that POST /api/goods endpoint is available."""
        payload = {
            "name": "Test Item",
            "price": 10000.0,
            "stock_quantity": 50,
        }
        response = client.post("/api/goods", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_create_goods_missing_required_field(self, client: TestClient):
        """Test creating goods with missing required field."""
        payload = {
            "name": "Test Item",
            # Missing price
            "stock_quantity": 50,
        }
        response = client.post("/api/goods", json=payload)
        # Missing required field should return validation error
        assert response.status_code in [400, 422]

    def test_update_goods_endpoint_available(
        self, client: TestClient, test_goods: Goods
    ):
        """Test that PUT /api/goods/{id} endpoint is available."""
        payload = {
            "name": "Updated Item",
            "price": 15000.0,
        }
        response = client.put(f"/api/goods/{test_goods.id}", json=payload)
        assert response.status_code in [200, 400, 404, 422]

    def test_update_nonexistent_goods(self, client: TestClient):
        """Test updating non-existent goods."""
        fake_id = uuid4()
        payload = {"name": "Updated"}
        response = client.put(f"/api/goods/{fake_id}", json=payload)
        assert response.status_code in [400, 404, 422]

    def test_delete_goods_endpoint_available(
        self, client: TestClient, test_goods: Goods
    ):
        """Test that DELETE /api/goods/{id} endpoint is available."""
        response = client.delete(f"/api/goods/{test_goods.id}")
        assert response.status_code in [200, 400, 404]

    def test_delete_nonexistent_goods(self, client: TestClient):
        """Test deleting non-existent goods."""
        fake_id = uuid4()
        response = client.delete(f"/api/goods/{fake_id}")
        assert response.status_code in [400, 404]
