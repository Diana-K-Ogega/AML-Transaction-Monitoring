import pandas as pd

# RULE 1: Structuring / Smurfing
# FATF Recommendation 20 — splitting to avoid reporting thresholds
def rule_structuring(df, threshold=10000, window_days=3):
    alerts = []
    df['txn_date'] = pd.to_datetime(df['txn_date'])
    for acct, grp in df.groupby('account_id'):
        grp = grp.sort_values('txn_date')
        for i, row in grp.iterrows():
            window = grp[(grp['txn_date'] >= row['txn_date'] - pd.Timedelta(days=window_days)) &
                         (grp['txn_date'] <= row['txn_date'])]
            if (window['amount'].sum() >= threshold * 0.8 and
                (window['amount'] < threshold).all() and
                len(window) >= 3):
                alerts.append({'txn_id': row['txn_id'], 'account_id': acct,
                                'rule': 'STRUCTURING', 'risk': 'HIGH',
                                'amount': row['amount'],
                                'detail': f"{len(window)} txns totalling ${window['amount'].sum():.0f} in {window_days} days"})
    return pd.DataFrame(alerts).drop_duplicates()

# RULE 2: High-Risk Country Transaction
def rule_high_risk_country(df):
    fatf_high_risk = ['IR', 'KP', 'MM', 'SY']  # FATF blacklist
    flagged = df[df['country'].isin(fatf_high_risk)].copy()
    flagged['rule'] = 'HIGH_RISK_COUNTRY'
    flagged['risk'] = 'HIGH'
    flagged['detail'] = 'Transaction with FATF-listed jurisdiction'
    return flagged[['txn_id','account_id','rule','risk','amount','detail']]

# RULE 3: Large Cash Transaction (CTR threshold)
def rule_large_cash(df, threshold=10000):
    flagged = df[(df['txn_type'].isin(['CASH_DEP','CASH_WD'])) &
                 (df['amount'] >= threshold)].copy()
    flagged['rule'] = 'LARGE_CASH'
    flagged['risk'] = 'MEDIUM'
    flagged['detail'] = flagged['amount'].apply(lambda x: f"Cash transaction of ${x:,.0f}")
    return flagged[['txn_id','account_id','rule','risk','amount','detail']]

# RULE 4: New Account High Value
def rule_new_account_high_value(df, days=30, amount=5000):
    flagged = df[(df['account_age_days'] <= days) &
                 (df['amount'] >= amount)].copy()
    flagged['rule'] = 'NEW_ACCT_HIGH_VALUE'
    flagged['risk'] = 'MEDIUM'
    flagged['detail'] = f"Account <{days}d old with ${amount:,}+ transaction"
    return flagged[['txn_id','account_id','rule','risk','amount','detail']]