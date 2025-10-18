# Payment Fraud Detection System

## Overview
Real-time payment fraud detection system with machine learning - Analyzes transaction patterns to prevent fraudulent activities in payment processing.

## Project Structure
```
payment-fraud-detection-system/
├── docs/                        # Documentation
│   └── industry-analysis.md     # Payment industry analysis
├── analysis/                    # Data analysis
│   ├── transactional-analysis.ipynb
│   └── analyze_transactions.py
├── api/                         # Anti-fraud API
│   ├── app/
│   │   ├── models/
│   │   ├── rules/
│   │   └── database/
│   └── tests/
├── data/                        # Sample data
│   └── transactional-sample.csv
└── requirements.txt
```

## Key Findings
Based on analysis of 3,199 transactions from November-December 2019:

- **Alarming Chargeback Rate**: 12.22% (12x higher than industry standard)
- **Financial Impact**: R$ 568,346.62 in chargebacks
- **Critical Patterns**: Velocity attacks, high-value fraud, night transactions
- **High-Risk Entities**: 5 users, 14 devices, 114 merchants with extreme fraud rates

## Critical Anti-Fraud Rules (Immediate Implementation)
1. **Block transactions within 5 minutes** of previous (same user/card)
2. **Enhanced review for transactions >R$ 2,000**
3. **Immediate flags for night transactions** (00:00-06:00)
4. **Block users with >10 transactions** in 24 hours
5. **Block merchants with >50% chargeback rate**

## Expected Impact
- **Velocity attacks**: 49.23% → <5% chargeback rate
- **High-value fraud**: 38.75% → <10% chargeback rate  
- **Night transactions**: 17.53% → <8% chargeback rate
- **Overall target**: Reduce from 12.22% to <2% chargeback rate

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Data Analysis
```bash
jupyter notebook analysis/transactional-analysis.ipynb
```

### 3. Start Anti-Fraud API
```bash
cd api
python app/main.py
```

### 4. Test API
```bash
curl -X POST "http://localhost:8000/fraud-check" \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_id": 2342357,
       "merchant_id": 29744,
       "user_id": 97051,
       "card_number": "434505******9116",
       "transaction_date": "2019-11-31T23:16:32.812632",
       "transaction_amount": 373,
       "device_id": 285475
     }'
```

## API Documentation
The API provides a single endpoint `/fraud-check` that receives transaction data and returns fraud recommendations.

### Request Format
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

### Response Format
```json
{
  "transaction_id": 2342357,
  "recommendation": "approve",
  "risk_score": 0.3,
  "rules_triggered": ["high_value_check"],
  "processing_time_ms": 45
}
```

## Data Requirements
- **Missing**: 26% of transactions lack device_id (critical gap)
- **Needed**: Geolocation, biometric data, extended transaction history
- **Priority**: Implement device_id collection for all transactions

## Conclusion
The current system has critical vulnerabilities requiring immediate anti-fraud implementation. The identified patterns provide clear, actionable rules that can significantly reduce fraud risk and financial losses.

## Technology Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Analysis**: Pandas, NumPy, Matplotlib, Seaborn
- **Testing**: Pytest
- **Documentation**: Jupyter Notebooks, Markdown

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License
This project is part of the Cloudwalk Software Engineer assessment case.
