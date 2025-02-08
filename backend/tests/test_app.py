import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app import app
import os

client = TestClient(app)

# Authentication Tests
def test_login_success():
    response = client.post(
        "/auth/login",
        json={"username": os.getenv("APP_USERNAME"), "password": os.getenv("APP_PASSWORD")}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()

def test_login_failed():
    response = client.post(
        "/auth/login",
        json={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Protected Endpoints Tests
def test_protected_endpoint_without_token():
    response = client.post("/api/chunk", json={"content": "test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_protected_endpoint_with_invalid_token():
    response = client.post(
        "/api/chunk",
        headers={"Authorization": "Bearer invalid_token"},
        json={"content": "test"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Markdown Processing Tests
@pytest.mark.asyncio
async def test_chunk_markdown():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        json={"username": os.getenv("APP_USERNAME"), "password": os.getenv("APP_PASSWORD")}
    )
    token = login_response.json()["token"]
    
    # Test markdown chunking
    markdown_content = "# Test\nThis is a test content"
    response = client.post(
        "/api/chunk",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": markdown_content}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "chunks" in response.json()

# Error Handling Tests
def test_invalid_markdown():
    login_response = client.post(
        "/auth/login",
        json={"username": os.getenv("APP_USERNAME"), "password": os.getenv("APP_PASSWORD")}
    )
    token = login_response.json()["token"]
    
    response = client.post(
        "/api/chunk",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": None}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_server_error_handling():
    login_response = client.post(
        "/auth/login",
        json={"username": os.getenv("APP_USERNAME"), "password": os.getenv("APP_PASSWORD")}
    )
    token = login_response.json()["token"]
    
    # Testing with invalid file path
    response = client.post(
        "/api/upload",
        headers={"Authorization": f"Bearer {token}"},
        json={"file_path": "/nonexistent/path"}
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "error" in response.json()