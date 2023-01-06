import pandas as pd
import logging
from log import *

col_to_use = ["from", "to", "value", "type", "blockTimestamp"]
all_transactions = pd.read_parquet('../ethereum_collector/ethereum_transactions/2022-07-04', engine='pyarrow', columns=col_to_use)

"""
all_transactions = pd.DataFrame({
    "from": ["toto", "ulul", "ulul", "titi", "toto", "toto"],
    "value": [4, 1, 2, 2, 4, 5],
    #"value2": [2, 2, 4, 4, 2, 10],
    "type": ["0x1", "0x1", "0x0", "0x0", "0x2", "0x2"],
    "blockTimestamp": ["2022-11-28 08:05:00", "2022-11-28 09:15:00", "2022-11-28 10:46:09", "2022-11-28 12:55:20", "2022-11-28 09:35:43", "2022-11-28 08:05:00"]
})
"""
#print(all_transactions)
# force proper types
#typed = all_transactions.convert_dtypes() #does not work, converts everything to string, infer_objects does not work
all_transactions['blockTimestamp'] = all_transactions['blockTimestamp'].apply(pd.to_datetime)
all_transactions['from'] = all_transactions['from'].astype('string')
all_transactions['type'] = all_transactions['type'].astype('string')
#print(all_transactions.info())

# https://stackoverflow.com/questions/14529838/apply-multiple-functions-to-multiple-groupby-columns
#agg = all_transactions.groupby(['blockTimestamp']).sum()
# group by must be done before resampling

def aggregator(df, grouping_field):
    agg_df = all_transactions.groupby(grouping_field) \
            .resample("1H", on="blockTimestamp") \
            .agg({'value':['sum'],'from':['count', 'nunique']})
    return(agg_df)

def write_to_csv(agg_df, df_name):
    agg_df.reset_index(inplace=True) # all columns names at same level

    agg_df.columns = [' '.join(col).strip() for col in agg_df.columns.values]
    #print(agg_df)
    try:
        agg_df.to_csv(f'{df_name}.csv', index=False)
    except:
        logging.error(f'writing CSV file {df_name}.csv : {traceback.print_exc()}')

by_from = aggregator(all_transactions, 'from')
write_to_csv(by_from, 'by_from')
by_type = aggregator(all_transactions, 'type')
write_to_csv(by_type, 'by_type')

# number of transactions
#print(len(all_transactions.index))
# sum of values
#print(all_transactions['value'].sum())
