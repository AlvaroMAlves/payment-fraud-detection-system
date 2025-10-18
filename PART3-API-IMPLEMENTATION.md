# Part 3: Anti-Fraud API Implementation
## Real-Time Fraud Detection System

**Author:** Alvaro Martins Alves  
**Date:** January 15, 2025  
**Case:** Cloudwalk Software Engineer Assessment

**This document answers Part 3 of the Cloudwalk case: "Solve the problem"**

### Key Requirements Met:
- ✅ Implement a simple anti-fraud system with an API
- ✅ Endpoint that receives transaction data and returns approve/deny recommendation
- ✅ Reject transactions based on predefined rules
- ✅ Hybrid approach (rule-based + score-based)

### Main Implementation:
🚀 **[API Documentation](api/app/main.py)** - Complete FastAPI implementation

### API Endpoint:
```
POST /fraud-check
```

### Request Format:
```json
{
  "transaction_id": 2342357,
  "merchant_id": 29744,
  "user_id": 97051,
  "card_number": "434505******9116",
  "transaction_date": "2019-11-31T23:16:32.812632",
  "transaction_amount": 373,
  "device_id": 285475
}
```

### Response Format:
```json
{
  "transaction_id": 2342357,
  "recommendation": "approve",
  "risk_score": 0.3,
  "rules_triggered": ["high_value_check"],
  "processing_time_ms": 45,
  "explanation": "High-value transaction: R$ 373.00"
}
```

### Anti-Fraud Rules Implemented:
1. **Historical Suspicious Users** (80%+ chargeback rate)
2. **Historical Suspicious Cards** (50%+ chargeback rate)
3. **Historical Suspicious Devices** (75%+ chargeback rate)
4. **Historical Suspicious Merchants** (50%+ chargeback rate)
5. **Velocity Check** (< 5 minutes between transactions)
6. **High-Value Check** (> R$ 2,000)
7. **Night Transaction Check** (00:00-06:00)
8. **Device Sharing Check** (multiple users per device)

### Technical Features:
- **Hybrid Approach**: Rule-based + Score-based detection
- **Real-time Processing**: <50ms response time
- **Historical Intelligence**: Uses past chargeback data
- **Clear Explanations**: Detailed reasoning for each decision
- **Professional API**: FastAPI with Swagger documentation
- **Automated Testing**: Complete test suite

### Expected Impact:
- **Velocity attacks**: 49.23% → <5% chargeback rate
- **High-value fraud**: 38.75% → <10% chargeback rate
- **Night transactions**: 17.53% → <8% chargeback rate
- **Overall target**: 12.22% → <2% chargeback rate

### How to Test:
```bash
# Start API
cd api
pip install -r requirements.txt
python app/main.py

# Test endpoint
curl -X POST "http://localhost:8000/fraud-check" \
     -H "Content-Type: application/json" \
     -d '{"transaction_id": 123, "merchant_id": 100, "user_id": 200, "card_number": "1234****5678", "transaction_date": "2019-12-01T14:30:00", "transaction_amount": 100.50, "device_id": 300}'
```

---
*This implementation provides a production-ready anti-fraud system with clear business impact.*
