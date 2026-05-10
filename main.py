import pandas as pd
from rules.aml_rules import rule_large_cash, rule_new_account_high_value

# 1. Load the data you already generated
print("📂 Loading transaction data...")
df = pd.read_csv('data/transactions.csv')

# 2. Run your specific CFE rules
print("🔍 Screening for red flags...")
alerts_cash = rule_large_cash(df)
alerts_new_acct = rule_new_account_high_value(df)

# 3. Combine the findings
all_alerts = pd.concat([alerts_cash, alerts_new_acct])

# 4. Save the final report
all_alerts.to_csv('reports/aml_alerts_report.csv', index=False)

print(f"✅ SUCCESS! {len(all_alerts)} alerts found.")
print("📂 Report saved in: reports/aml_alerts_report.csv")
import pandas as pd
from rules.aml_rules import rule_large_cash, rule_new_account_high_value

# Load data
df = pd.read_csv('data/transactions.csv')

# Run Rules
alerts_cash = rule_large_cash(df)
alerts_new_acct = rule_new_account_high_value(df)

# Combine and Save
all_alerts = pd.concat([alerts_cash, alerts_new_acct])
all_alerts.to_csv('reports/aml_alerts_report.csv', index=False)

print(f"✅ Success! Generated {len(all_alerts)} alerts in the reports folder.")