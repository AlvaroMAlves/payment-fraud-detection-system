# Payment Fraud Detection System

**Author:** Alvaro Martins Alves  
**Date:** January 15, 2025  
**Case:** Cloudwalk Software Engineer Assessment

## Overview
Real-time payment fraud detection system - Analyzes transaction patterns to prevent fraudulent activities in payment processing.

## Project Structure
```
payment-fraud-detection-system/
├── PART1-INDUSTRY-ANALYSIS.md   # 📋 Part 1: Industry Understanding
├── PART2-DATA-ANALYSIS.md       # 📊 Part 2: Data Analysis
├── PART3-API-IMPLEMENTATION.md  # 🚀 Part 3: API Implementation
├── README.md                    # 📖 Project Overview
├── 
├── docs/
│   └── industry-analysis.md     # Detailed industry analysis
├── analysis/
│   └── transactional-analysis.ipynb  # Interactive data analysis
├── api/                         # Anti-fraud API
│   ├── app/
│   │   ├── main.py             # FastAPI implementation
│   │   ├── models/
│   │   ├── rules/
│   │   └── database/
│   ├── tests/
│   │   └── test_api.py         # Automated tests
│   └── requirements.txt        # API dependencies
├── data/
│   └── transactional-sample.csv # Sample transaction data
└── requirements.txt            # Analysis dependencies
```

## Case Solution Overview

This project implements the complete Cloudwalk Software Engineer case solution:

### 📋 [Part 1: Industry Analysis](PART1-INDUSTRY-ANALYSIS.md)
**Question**: "Understand the Industry"  
**Answer**: Complete analysis of payment ecosystem, money flow, and player roles with Brazilian examples.  
📄 **[Detailed Analysis](docs/industry-analysis.md)**

### 📊 [Part 2: Data Analysis](PART2-DATA-ANALYSIS.md)  
**Question**: "Get your hands dirty"  
**Answer**: Interactive analysis identifying suspicious patterns and fraud indicators from 3,199 transactions.

### 🚀 [Part 3: API Implementation](PART3-API-IMPLEMENTATION.md)
**Question**: "Solve the problem"  
**Answer**: Production-ready anti-fraud API with hybrid rule-based + score-based detection.

---

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
# Install Jupyter and dependencies
pip install -r requirements.txt

# Start Jupyter Notebook
jupyter notebook

# Then open: analysis/transactional-analysis.ipynb
# Or run directly:
jupyter notebook analysis/transactional-analysis.ipynb
```

**How to use the notebook:**
1. **Open**: Click on `transactional-analysis.ipynb` in Jupyter
2. **Run All**: Go to `Cell` → `Run All` to execute all analysis
3. **Interactive**: Each cell can be run individually with `Shift + Enter`
4. **Visualizations**: Charts and graphs will appear inline
5. **Results**: All findings and conclusions are in markdown cells

**Troubleshooting:**
- **Data not found**: Make sure `data/transactional-sample.csv` exists
- **Import errors**: Run `pip install pandas matplotlib seaborn jupyter`
- **Kernel issues**: Restart kernel in Jupyter (`Kernel` → `Restart`)

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
  "processing_time_ms": 45,
  "explanation": "High-value transaction: R$ 373.00"
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
- **Data Processing**: Pandas (in-memory analysis)
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
