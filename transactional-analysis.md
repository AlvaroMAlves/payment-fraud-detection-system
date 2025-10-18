# Transactional Data Analysis
## Suspicious Behavior Detection in Payment Transactions

### Executive Summary

This analysis examines 3,199 payment transactions from November-December 2019 to identify suspicious patterns and behaviors that could indicate fraudulent activity. The dataset shows a **12.22% chargeback rate**, significantly higher than industry standards (typically 0.5-1%), indicating substantial fraud risk.

### Dataset Overview

**Basic Statistics:**
- **Total Transactions**: 3,199
- **Unique Users**: 2,704 (1.18 transactions per user on average)
- **Unique Merchants**: 1,756
- **Unique Cards**: 2,925
- **Unique Devices**: 1,996
- **Date Range**: November 1 - December 1, 2019

**Transaction Values:**
- **Average Amount**: R$ 767.81
- **Median Amount**: R$ 415.94
- **Range**: R$ 1.22 - R$ 4,097.21
- **Standard Deviation**: R$ 889.10

### Key Findings

#### 1. High Chargeback Rate
- **Overall Rate**: 12.22% (vs. industry standard of 0.5-1%)
- **Total Chargeback Amount**: R$ 568,346.62
- **High-Value Transactions**: 38.75% chargeback rate for transactions >R$ 2,775

#### 2. Temporal Patterns
**Hourly Distribution:**
- **Peak Hours**: 16:00-20:00 (1,081 transactions, 33.8% of total)
- **Low Activity**: 04:00-08:00 (16 transactions, 0.5% of total)
- **Night Activity**: 00:00-03:00 (335 transactions, 10.5% of total)

**Weekly Distribution:**
- **Weekend Peak**: Friday (805) and Saturday (756) transactions
- **Weekday Decline**: Wednesday (157) and Tuesday (256) transactions

#### 3. Suspicious User Behavior

**High-Frequency Users:**
- **5 users** with >10 transactions each
- **Top offender**: User 11750 with 31 transactions
- **Pattern**: Multiple transactions suggest card testing or account takeover

**Velocity Attacks:**
- **65 transactions** occurring within 5 minutes of previous transaction (same user)
- **Pattern**: Rapid successive transactions indicate card testing or fraud attempts

#### 4. Card-Based Suspicious Activity

**High-Usage Cards:**
- **4 cards** with >5 transactions each
- **Top card**: 554482******7640 with 10 transactions
- **Pattern**: Multiple transactions per card suggest compromised card data

#### 5. Device-Based Patterns

**Shared Device Usage:**
- **14 devices** with >5 transactions each
- **Top device**: 563499.0 with 22 transactions
- **Pattern**: Multiple users on same device suggests device compromise or shared fraud

#### 6. Merchant Risk Analysis

**High-Risk Merchants:**
- **114 merchants** with >20% chargeback rate
- **15 merchants** with 100% chargeback rate
- **Pattern**: Merchant collusion or compromised merchant accounts

### Identified Fraud Patterns

#### 1. Card Testing
**Evidence**: Multiple small transactions from same card/user
- Card 554482******7640: 10 transactions
- User 11750: 31 transactions
- 65 rapid successive transactions

#### 2. Account Takeover
**Evidence**: Sudden increase in transaction frequency
- Users with >10 transactions in short period
- Unusual transaction amounts or timing

#### 3. Merchant Collusion
**Evidence**: Merchants with extremely high chargeback rates
- 15 merchants with 100% chargeback rate
- 114 merchants with >20% chargeback rate

#### 4. Device Compromise
**Evidence**: Multiple users on same device
- Device 563499.0: 22 transactions from multiple users
- 14 devices with >5 transactions each

#### 5. High-Value Fraud
**Evidence**: Large transactions with high chargeback rates
- 38.75% chargeback rate for transactions >R$ 2,775
- 160 high-value transactions (5% of total)

### Recommended Additional Data Points

#### 1. Behavioral Data
- **Biometric Authentication**: Fingerprint, facial recognition
- **Typing Patterns**: Keystroke dynamics, typing speed
- **Mouse Movement**: Cursor patterns and behavior

#### 2. Contextual Data
- **Geolocation**: GPS coordinates, IP geolocation
- **Device Fingerprinting**: Browser version, screen resolution, timezone
- **Network Information**: IP address, ISP, proxy detection

#### 3. Historical Data
- **Transaction History**: Previous transaction patterns
- **Credit Score**: Customer creditworthiness
- **Account Age**: Time since account creation
- **Login Patterns**: Usual login times and locations

#### 4. Real-Time Data
- **Velocity Checks**: Transactions per minute/hour/day
- **Amount Patterns**: Unusual spending patterns
- **Merchant Relationships**: Previous merchant interactions
- **Time-Based Anomalies**: Transactions outside normal hours

#### 5. External Data Sources
- **Blacklists**: Known fraudulent cards, devices, IPs
- **Whitelists**: Trusted customers and merchants
- **Risk Scores**: External fraud detection services
- **Social Media**: Account verification through social platforms

### Anti-Fraud Rules Recommendations

#### 1. Velocity Rules
- **Block**: >5 transactions in 5 minutes (same user/card)
- **Flag**: >10 transactions in 1 hour (same user/card)
- **Monitor**: >20 transactions in 1 day (same user/card)

#### 2. Amount Rules
- **Block**: Transactions >R$ 5,000 (new users)
- **Flag**: Transactions >R$ 2,000 (high-risk users)
- **Monitor**: Transactions >R$ 1,000 (new merchants)

#### 3. Device Rules
- **Block**: >10 users on same device (24 hours)
- **Flag**: >5 users on same device (24 hours)
- **Monitor**: New device for existing user

#### 4. Merchant Rules
- **Block**: Merchants with >50% chargeback rate
- **Flag**: Merchants with >20% chargeback rate
- **Monitor**: New merchants with high-value transactions

#### 5. Time-Based Rules
- **Flag**: Transactions between 02:00-06:00 (low activity hours)
- **Monitor**: Transactions outside user's normal hours
- **Block**: Multiple transactions in rapid succession

### Implementation Priority

#### High Priority (Immediate Implementation)
1. **Velocity checks** for rapid successive transactions
2. **High-value transaction** monitoring
3. **Device sharing** detection
4. **Merchant chargeback** rate monitoring

#### Medium Priority (Short-term Implementation)
1. **Geolocation** verification
2. **Device fingerprinting**
3. **Historical pattern** analysis
4. **Time-based** anomaly detection

#### Low Priority (Long-term Implementation)
1. **Biometric authentication**
2. **Machine learning** models
3. **External data** integration
4. **Social media** verification

### Conclusion

The transactional data reveals significant fraud indicators with a 12.22% chargeback rate. Key patterns include card testing, account takeover, merchant collusion, and device compromise. Implementing velocity checks, high-value monitoring, and device sharing detection would significantly reduce fraud risk.

The recommended additional data points would enhance fraud detection capabilities, particularly behavioral and contextual data that provide deeper insights into transaction legitimacy.
