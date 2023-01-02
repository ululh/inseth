import pandas as pd

col_to_use = ["from", "to", "value", "type", "blockTimestamp"]
all_transactions = pd.read_parquet('../ethereum_collector/ethereum_transactions/', engine='pyarrow', columns=col_to_use)

print(all_transactions.shape)

# number of transactions
print(len(all_transactions.index))

# sum of values
print(all_transactions['value'].sum())
