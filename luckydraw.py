import pandas as pd
import random

# Read both CSV files
df1 = pd.read_csv('data/raw/BI_results_Y6-8.csv')
df2 = pd.read_csv('data/raw/BI_results_Y9-12.csv')

# Extract email addresses from both dataframes
emails1 = set(df1['Email address'].dropna())
emails2 = set(df2['Email address'].dropna())

# Combine all unique email addresses
all_emails = list(emails1.union(emails2))

# Select 6 random winners
winners = random.sample(all_emails, 6)

print("\nLucky Draw Winners:")
print("-----------------")
for i, winner in enumerate(winners, 1):
    print(f"{i}. {winner}")