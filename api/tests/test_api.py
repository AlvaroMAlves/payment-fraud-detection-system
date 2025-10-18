import pytest
import httpx
from fastapi.testclient import TestClient
from api.app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Payment Fraud Detection API" in response.json()["message"]

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_fraud_check_approve():
    """Test fraud check with low-risk transaction"""
    transaction_data = {
        "transaction_id": 123456,
        "merchant_id": 1001,
        "user_id": 2001,
        "card_number": "1234****5678",
        "transaction_date": "2019-12-01T14:30:00.000000",
        "transaction_amount": 100.50,
        "device_id": 3001
    }
    
    response = client.post("/fraud-check", json=transaction_data)
    assert response.status_code == 200
    
    result = response.json()
    assert result["transaction_id"] == 123456
    assert result["recommendation"] in ["approve", "deny"]
    assert "risk_score" in result
    assert "rules_triggered" in result
    assert "processing_time_ms" in result

def test_fraud_check_high_value():
    """Test fraud check with high-value transaction"""
    transaction_data = {
        "transaction_id": 123457,
        "merchant_id": 1002,
        "user_id": 2002,
        "card_number": "1234****5679",
        "transaction_date": "2019-12-01T15:30:00.000000",
        "transaction_amount": 3000.00,  # High value
        "device_id": 3002
    }
    
    response = client.post("/fraud-check", json=transaction_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "high_value_check" in result["rules_triggered"]
    assert result["risk_score"] >= 0.3

def test_fraud_check_night_transaction():
    """Test fraud check with night transaction"""
    transaction_data = {
        "transaction_id": 123458,
        "merchant_id": 1003,
        "user_id": 2003,
        "card_number": "1234****5680",
        "transaction_date": "2019-12-01T02:30:00.000000",  # Night time
        "transaction_amount": 150.00,
        "device_id": 3003
    }
    
    response = client.post("/fraud-check", json=transaction_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "night_transaction" in result["rules_triggered"]
    assert result["risk_score"] >= 0.2

def test_fraud_check_velocity():
    """Test fraud check with rapid successive transactions"""
    # First transaction
    transaction1 = {
        "transaction_id": 123459,
        "merchant_id": 1004,
        "user_id": 2004,
        "card_number": "1234****5681",
        "transaction_date": "2019-12-01T16:00:00.000000",
        "transaction_amount": 200.00,
        "device_id": 3004
    }
    
    response1 = client.post("/fraud-check", json=transaction1)
    assert response1.status_code == 200
    
    # Second transaction within 5 minutes (same user)
    transaction2 = {
        "transaction_id": 123460,
        "merchant_id": 1004,
        "user_id": 2004,  # Same user
        "card_number": "1234****5681",
        "transaction_date": "2019-12-01T16:03:00.000000",  # 3 minutes later
        "transaction_amount": 250.00,
        "device_id": 3004
    }
    
    response2 = client.post("/fraud-check", json=transaction2)
    assert response2.status_code == 200
    
    result = response2.json()
    assert "velocity_check" in result["rules_triggered"]
    assert result["risk_score"] >= 0.4

if __name__ == "__main__":
    pytest.main([__file__])
