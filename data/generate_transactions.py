import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

def generate_transactions(n=5000):
    start = datetime(2024, 1, 1)
    accounts = [f"ACC{i:04d}" for i in range(1, 201)]
    countries = ['KE','NG','ZA','GB','US','AE','IR','KP']  # IR/KP = FATF high-risk

    records = []
    for _ in range(n):
        acct = random.choice(accounts)
        # Inject structuring pattern for some accounts
        if acct in accounts[:10]:
            amount = round(random.uniform(8000, 9999), 2)  # just under 10k
        else:
            amount = round(np.random.lognormal(5, 1.5), 2)

        records.append({
            'txn_id': f"TXN{_:06d}",
            'account_id': acct,
            'amount': amount,
            'currency': 'USD',
            'country': random.choices(countries, weights=[30,20,15,10,10,10,3,2])[0],
            'txn_date': start + timedelta(days=random.randint(0,365),
                                            hours=random.randint(0,23)),
            'txn_type': random.choice(['WIRE','CASH_DEP','CASH_WD','TRANSFER']),
            'account_age_days': random.randint(1, 3650),
        })
    return pd.DataFrame(records)

if __name__ == '__main__':
    df = generate_transactions()
    df.to_csv('data/transactions.csv', index=False)
    print(f"Generated {len(df)} transactions")