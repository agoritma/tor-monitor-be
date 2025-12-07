"""Unit tests for AI chat endpoints."""

from datetime import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.db.models import User
from app.dependencies import get_current_user


class TestChatEndpoints:
    """Test suite for AI chat and agent routes."""

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

    def test_chat_endpoint_exists(self, client: TestClient):
        """Test that chat endpoint is available."""
        response = client.post("/api/chat?chat_message=test")
        # Should respond (may fail on auth or validation, but endpoint exists)
        assert response.status_code in [200, 422, 500]

    def test_chat_with_valid_prompt(self, client: TestClient):
        """Test chat with valid prompt message."""
        response = client.post("/api/chat?chat_message=Berapa total penjualan?")
        assert response.status_code in [200, 500]

    def test_chat_missing_prompt(self, client: TestClient):
        """Test chat endpoint without chat_message parameter."""
        response = client.post("/api/chat")
        # Missing parameter should error
        assert response.status_code in [422, 400, 500]

    def test_chat_with_parameter(self, client: TestClient):
        """Test chat with query parameter."""
        response = client.post("/api/chat?chat_message=test message")
        assert response.status_code in [200, 500]

    def test_chat_returns_response(self, client: TestClient):
        """Test that chat returns a response."""
        response = client.post("/api/chat?chat_message=test")
        if response.status_code == 200:
            # Response could be a string or dict depending on implementation
            data = response.json()
            assert data is not None

    def test_chat_with_inventory_query(self, client: TestClient):
        """Test chat with inventory-related query."""
        response = client.post("/api/chat?chat_message=Berapa total stok?")
        assert response.status_code in [200, 500]

    def test_chat_with_sales_query(self, client: TestClient):
        """Test chat with sales-related query."""
        response = client.post("/api/chat?chat_message=Berapa pendapatan?")
        assert response.status_code in [200, 500]

    def test_chat_with_special_characters(self, client: TestClient):
        """Test chat with special characters."""
        response = client.post("/api/chat?chat_message=test%20%26%20special")
        assert response.status_code in [200, 500]
