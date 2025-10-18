# Part 2: Data Analysis
## Suspicious Behavior Detection

**This document answers Part 2 of the Cloudwalk case: "Get your hands dirty"**

### Key Questions Answered:
- What suspicious patterns can you identify in the transactional data?
- What additional data points would be useful for fraud detection?
- How can we detect fraudulent behavior from transaction patterns?

### Main Document:
📊 **[transactional-analysis.ipynb](analysis/transactional-analysis.ipynb)** - Interactive Jupyter notebook with complete analysis

### Key Findings:
- **Critical Chargeback Rate**: 12.22% (12x higher than industry standard)
- **Financial Impact**: R$ 568,346.62 in chargebacks
- **High-Risk Patterns**:
  - Velocity attacks: 49.23% chargeback rate
  - High-value fraud: 38.75% chargeback rate
  - Night transactions: 17.53% chargeback rate
- **Suspicious Entities**: 5 users, 14 devices, 114 merchants with extreme fraud rates

### Critical Anti-Fraud Rules Identified:
1. Block transactions within 5 minutes (same user)
2. Enhanced review for transactions >R$ 2,000
3. Flag night transactions (00:00-06:00)
4. Block users with high historical chargeback rates
5. Block merchants with >50% chargeback rates

### Additional Data Points Needed:
- Geolocation data
- Biometric authentication
- Extended transaction history
- Device fingerprinting improvements

---
*This analysis provides actionable insights for fraud prevention implementation.*
