"""
Payment Fraud Detection API
Author: Alvaro Martins Alves
Date: January 15, 2025
Case: Cloudwalk Software Engineer Assessment

Real-time payment fraud detection system based on historical data analysis.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import time
import pandas as pd
import os

app = FastAPI(
    title="Payment Fraud Detection API",
    description="Real-time payment fraud detection system based on historical data analysis",
    version="2.0.0"
)

# Data Models
class Transaction(BaseModel):
    transaction_id: int
    merchant_id: int
    user_id: int
    card_number: str
    transaction_date: str
    transaction_amount: float
    device_id: Optional[int] = None

class FraudResponse(BaseModel):
    transaction_id: int
    recommendation: str  # "approve" or "deny"
    risk_score: float
    rules_triggered: List[str]
    processing_time_ms: int
    explanation: str

# Enhanced Anti-Fraud Rules Engine
class FraudDetector:
    def __init__(self):
        self.transaction_history = {}
        self.user_transactions = {}
        self.merchant_blacklist = set()
        self.device_users = {}
        self.suspicious_users = set()
        self.suspicious_cards = set()
        self.suspicious_devices = set()
        self.suspicious_merchants = set()
        
        # Load historical data for better detection
        self._load_historical_data()
    
    def _load_historical_data(self):
        """Load historical transaction data to identify suspicious patterns"""
        try:
            # Try to load the CSV file
            csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'transactional-sample.csv')
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                
                # Identify suspicious entities based on chargeback rates
                # High-risk users (chargeback rate > 80%)
                user_cb_rates = df.groupby('user_id')['has_cbk'].agg(['count', 'sum']).reset_index()
                user_cb_rates['cb_rate'] = user_cb_rates['sum'] / user_cb_rates['count']
                self.suspicious_users = set(user_cb_rates[user_cb_rates['cb_rate'] > 0.8]['user_id'].tolist())
                
                # High-risk cards (chargeback rate > 50%)
                card_cb_rates = df.groupby('card_number')['has_cbk'].agg(['count', 'sum']).reset_index()
                card_cb_rates['cb_rate'] = card_cb_rates['sum'] / card_cb_rates['count']
                self.suspicious_cards = set(card_cb_rates[card_cb_rates['cb_rate'] > 0.5]['card_number'].tolist())
                
                # High-risk devices (chargeback rate > 75%)
                device_cb_rates = df.groupby('device_id')['has_cbk'].agg(['count', 'sum']).reset_index()
                device_cb_rates['cb_rate'] = device_cb_rates['sum'] / device_cb_rates['count']
                self.suspicious_devices = set(device_cb_rates[device_cb_rates['cb_rate'] > 0.75]['device_id'].tolist())
                
                # High-risk merchants (chargeback rate > 50%)
                merchant_cb_rates = df.groupby('merchant_id')['has_cbk'].agg(['count', 'sum']).reset_index()
                merchant_cb_rates['cb_rate'] = merchant_cb_rates['sum'] / merchant_cb_rates['count']
                self.suspicious_merchants = set(merchant_cb_rates[merchant_cb_rates['cb_rate'] > 0.5]['merchant_id'].tolist())
                
                print(f"Loaded historical data: {len(self.suspicious_users)} suspicious users, {len(self.suspicious_cards)} suspicious cards")
                
        except Exception as e:
            print(f"Could not load historical data: {e}")
    
    def check_fraud(self, transaction: Transaction) -> dict:
        start_time = time.time()
        rules_triggered = []
        risk_score = 0.0
        explanations = []
        
        # Rule 1: Historical Suspicious User (Critical)
        if transaction.user_id in self.suspicious_users:
            rules_triggered.append("suspicious_user")
            risk_score += 0.6
            explanations.append(f"User {transaction.user_id} has high historical chargeback rate")
        
        # Rule 2: Historical Suspicious Card
        if transaction.card_number in self.suspicious_cards:
            rules_triggered.append("suspicious_card")
            risk_score += 0.5
            explanations.append(f"Card {transaction.card_number} has high historical chargeback rate")
        
        # Rule 3: Historical Suspicious Device
        if transaction.device_id and transaction.device_id in self.suspicious_devices:
            rules_triggered.append("suspicious_device")
            risk_score += 0.5
            explanations.append(f"Device {transaction.device_id} has high historical chargeback rate")
        
        # Rule 4: Historical Suspicious Merchant
        if transaction.merchant_id in self.suspicious_merchants:
            rules_triggered.append("suspicious_merchant")
            risk_score += 0.4
            explanations.append(f"Merchant {transaction.merchant_id} has high historical chargeback rate")
        
        # Rule 5: Velocity Check (Critical)
        if self._check_velocity(transaction):
            rules_triggered.append("velocity_check")
            risk_score += 0.4
            explanations.append("Multiple transactions within 5 minutes")
        
        # Rule 6: High-Value Check
        if transaction.transaction_amount > 2000:
            rules_triggered.append("high_value_check")
            risk_score += 0.3
            explanations.append(f"High-value transaction: R$ {transaction.transaction_amount:,.2f}")
        
        # Rule 7: Night Transaction Check
        if self._check_night_transaction(transaction):
            rules_triggered.append("night_transaction")
            risk_score += 0.2
            explanations.append("Transaction during high-risk hours (00:00-06:00)")
        
        # Rule 8: Device Sharing Check
        if self._check_device_sharing(transaction):
            rules_triggered.append("device_sharing")
            risk_score += 0.2
            explanations.append("Device used by multiple users")
        
        # Determine recommendation
        recommendation = "deny" if risk_score >= 0.5 else "approve"
        
        # Update history
        self._update_history(transaction)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Create explanation
        if explanations:
            explanation = " | ".join(explanations)
        else:
            explanation = "No suspicious patterns detected"
        
        return {
            "transaction_id": transaction.transaction_id,
            "recommendation": recommendation,
            "risk_score": round(risk_score, 2),
            "rules_triggered": rules_triggered,
            "processing_time_ms": processing_time,
            "explanation": explanation
        }
    
    def _check_velocity(self, transaction: Transaction) -> bool:
        """Check if transaction is within 5 minutes of previous (same user)"""
        user_id = transaction.user_id
        current_time = datetime.fromisoformat(transaction.transaction_date.replace('Z', '+00:00'))
        
        if user_id in self.user_transactions:
            last_transaction_time = self.user_transactions[user_id]
            time_diff = (current_time - last_transaction_time).total_seconds() / 60
            
            if time_diff < 5:  # Less than 5 minutes
                return True
        
        return False
    
    def _check_night_transaction(self, transaction: Transaction) -> bool:
        """Check if transaction is between 00:00-06:00"""
        transaction_time = datetime.fromisoformat(transaction.transaction_date.replace('Z', '+00:00'))
        hour = transaction_time.hour
        
        return 0 <= hour <= 6
    
    def _check_device_sharing(self, transaction: Transaction) -> bool:
        """Check if device is used by multiple users"""
        if not transaction.device_id:
            return False
        
        device_id = transaction.device_id
        
        if device_id not in self.device_users:
            self.device_users[device_id] = set()
        
        self.device_users[device_id].add(transaction.user_id)
        
        # Flag if device used by >1 user
        return len(self.device_users[device_id]) > 1
    
    def _update_history(self, transaction: Transaction):
        """Update transaction history"""
        user_id = transaction.user_id
        transaction_time = datetime.fromisoformat(transaction.transaction_date.replace('Z', '+00:00'))
        
        self.user_transactions[user_id] = transaction_time

# Initialize fraud detector
fraud_detector = FraudDetector()

@app.get("/")
async def root():
    return {
        "message": "Payment Fraud Detection API",
        "version": "1.0.0",
        "endpoints": {
            "fraud-check": "POST /fraud-check",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/fraud-check", response_model=FraudResponse)
async def check_fraud(transaction: Transaction):
    """
    Check transaction for fraud patterns and return recommendation.
    
    This endpoint analyzes ONE transaction at a time and provides:
    - Historical pattern analysis based on real data
    - Real-time fraud detection rules
    - Clear explanation of why a transaction was flagged
    
    Based on analysis of 3,199 transactions, this endpoint implements:
    - Historical suspicious users (80%+ chargeback rate)
    - Historical suspicious cards (50%+ chargeback rate)  
    - Historical suspicious devices (75%+ chargeback rate)
    - Historical suspicious merchants (50%+ chargeback rate)
    - Velocity checks (49.23% chargeback rate for rapid transactions)
    - High-value monitoring (38.75% chargeback rate for >R$ 2,000)
    - Night transaction alerts (17.53% chargeback rate for 00:00-06:00)
    - Device sharing detection (75%+ chargeback rates for shared devices)
    
    Returns: approve/deny recommendation with detailed explanation
    """
    try:
        result = fraud_detector.check_fraud(transaction)
        return FraudResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fraud check failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
