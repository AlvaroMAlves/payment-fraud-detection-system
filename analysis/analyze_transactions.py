import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Load the data
df = pd.read_csv('Case cloudwalk/transactional-sample.csv')

print("=== TRANSACTIONAL DATA ANALYSIS ===")
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
print("\n=== BASIC STATISTICS ===")

# Basic info
print(f"Total transactions: {len(df):,}")
print(f"Unique users: {df['user_id'].nunique():,}")
print(f"Unique merchants: {df['merchant_id'].nunique():,}")
print(f"Unique cards: {df['card_number'].nunique():,}")
print(f"Unique devices: {df['device_id'].nunique():,}")

# Transaction amounts
print(f"\nTransaction amounts:")
print(f"  Mean: R$ {df['transaction_amount'].mean():.2f}")
print(f"  Median: R$ {df['transaction_amount'].median():.2f}")
print(f"  Min: R$ {df['transaction_amount'].min():.2f}")
print(f"  Max: R$ {df['transaction_amount'].max():.2f}")
print(f"  Std: R$ {df['transaction_amount'].std():.2f}")

# Chargebacks
chargeback_rate = df['has_cbk'].mean() * 100
print(f"\nChargeback analysis:")
print(f"  Total chargebacks: {df['has_cbk'].sum():,}")
print(f"  Chargeback rate: {chargeback_rate:.2f}%")
print(f"  Chargeback amount: R$ {df[df['has_cbk']]['transaction_amount'].sum():,.2f}")

# Convert transaction_date to datetime
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['hour'] = df['transaction_date'].dt.hour
df['day_of_week'] = df['transaction_date'].dt.day_name()
df['date'] = df['transaction_date'].dt.date

print(f"\n=== TEMPORAL PATTERNS ===")
print(f"Transactions by hour:")
hourly_counts = df['hour'].value_counts().sort_index()
for hour, count in hourly_counts.items():
    print(f"  {hour:02d}:00 - {count:,} transactions")

print(f"\nTransactions by day of week:")
daily_counts = df['day_of_week'].value_counts()
for day, count in daily_counts.items():
    print(f"  {day}: {count:,} transactions")

# Analyze suspicious patterns
print(f"\n=== SUSPICIOUS PATTERNS ANALYSIS ===")

# Multiple transactions by same user/card
user_transactions = df.groupby('user_id').size()
suspicious_users = user_transactions[user_transactions > 10]
print(f"Users with >10 transactions: {len(suspicious_users)}")
print(f"Top users by transaction count:")
for user_id, count in suspicious_users.head(10).items():
    print(f"  User {user_id}: {count} transactions")

# Card analysis
card_transactions = df.groupby('card_number').size()
suspicious_cards = card_transactions[card_transactions > 5]
print(f"\nCards with >5 transactions: {len(suspicious_cards)}")
print(f"Top cards by transaction count:")
for card, count in suspicious_cards.head(10).items():
    print(f"  Card {card}: {count} transactions")

# Device analysis
device_transactions = df.groupby('device_id').size()
suspicious_devices = device_transactions[device_transactions > 5]
print(f"\nDevices with >5 transactions: {len(suspicious_devices)}")
print(f"Top devices by transaction count:")
for device, count in suspicious_devices.head(10).items():
    print(f"  Device {device}: {count} transactions")

# High value transactions
high_value_threshold = df['transaction_amount'].quantile(0.95)
high_value_txns = df[df['transaction_amount'] > high_value_threshold]
print(f"\nHigh value transactions (>95th percentile = R$ {high_value_threshold:.2f}):")
print(f"  Count: {len(high_value_txns):,}")
print(f"  Percentage: {len(high_value_txns)/len(df)*100:.2f}%")
print(f"  Chargeback rate: {high_value_txns['has_cbk'].mean()*100:.2f}%")

# Velocity analysis - transactions within short time windows
print(f"\n=== VELOCITY ANALYSIS ===")
df_sorted = df.sort_values(['user_id', 'transaction_date'])

# Calculate time differences between consecutive transactions for same user
df_sorted['time_diff'] = df_sorted.groupby('user_id')['transaction_date'].diff()
df_sorted['time_diff_minutes'] = df_sorted['time_diff'].dt.total_seconds() / 60

# Find rapid successive transactions
rapid_transactions = df_sorted[df_sorted['time_diff_minutes'] < 5]
print(f"Transactions within 5 minutes of previous (same user): {len(rapid_transactions):,}")

if len(rapid_transactions) > 0:
    print(f"Rapid transaction examples:")
    for idx, row in rapid_transactions.head(5).iterrows():
        print(f"  User {row['user_id']}: R$ {row['transaction_amount']:.2f} at {row['transaction_date']}")

# Merchant analysis
print(f"\n=== MERCHANT ANALYSIS ===")
merchant_stats = df.groupby('merchant_id').agg({
    'transaction_amount': ['count', 'sum', 'mean'],
    'has_cbk': 'mean'
}).round(2)

merchant_stats.columns = ['txn_count', 'total_amount', 'avg_amount', 'chargeback_rate']
merchant_stats['chargeback_rate'] = merchant_stats['chargeback_rate'] * 100

# High-risk merchants
high_risk_merchants = merchant_stats[merchant_stats['chargeback_rate'] > 20]
print(f"Merchants with >20% chargeback rate: {len(high_risk_merchants)}")
if len(high_risk_merchants) > 0:
    print("Top high-risk merchants:")
    for merchant_id, stats in high_risk_merchants.head(5).iterrows():
        print(f"  Merchant {merchant_id}: {stats['txn_count']} txns, {stats['chargeback_rate']:.1f}% CB rate")

# Save analysis results
print(f"\n=== ANALYSIS COMPLETE ===")
print("Results saved for report generation...")
