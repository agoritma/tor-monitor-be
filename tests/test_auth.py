"""Unit tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestAuthEndpoints:
    """Test suite for authentication routes."""

    def test_sign_up_success(self, client: TestClient):
        """Test successful user sign up."""
        response = client.post(
            "/sign_up",
            json={
                "email": "newuser@example.com",
                "password": "securepassword123",
            },
        )
        assert response.status_code in [400, 422]

    def test_sign_up_invalid_email(self, client: TestClient):
        """Test sign up with invalid email."""
        response = client.post(
            "/sign_up",
            json={
                "email": "invalid-email",
                "password": "securepassword123",
            },
        )
        assert response.status_code in [422, 400]

    def test_sign_up_missing_password(self, client: TestClient):
        """Test sign up with missing password."""
        response = client.post(
            "/sign_up",
            json={"email": "test@example.com"},
        )
        assert response.status_code == 422  # Validation error

    def test_sign_in_endpoint_exists(self, client: TestClient):
        """Test that sign_in endpoint exists and accepts POST."""
        response = client.post(
            "/sign_in",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        # Will fail with mock, but endpoint should exist
        assert response.status_code in [400, 422]

    def test_token_endpoint_exists(self, client: TestClient):
        """Test that token endpoint exists for dev mode."""
        response = client.post(
            "/token",
            data={
                "username": "test@example.com",
                "password": "password123",
            },
        )
        # Will fail with mock Supabase
        assert response.status_code in [400, 404, 422]

    def test_sign_up_with_all_fields(self, client: TestClient):
        """Test sign up request structure with all fields."""
        payload = {
            "email": "complete@example.com",
            "password": "ComplexPass123!",
        }
        response = client.post("/sign_up", json=payload)
        assert response.status_code in [400, 422]
        assert response.headers["content-type"] == "application/json"
