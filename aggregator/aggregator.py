import sys
sys.path.append("../utils/")
import pandas as pd
from log import * # from utils
from container import * # from utils
import traceback

logging_config()
data_prefix = storage_prefix()

col_to_use = ["from", "to", "value", "type", "blockTimestamp"]
all_transactions = pd.read_parquet(f'{data_prefix}/ethereum_transactions/', engine='pyarrow', columns=col_to_use)

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

def agg_resample(df, grouping_field):
    agg_df = all_transactions.groupby(grouping_field) \
            .resample("1H", on="blockTimestamp") \
            .agg({'value':['sum'],'from':['count', 'nunique']})
    return(agg_df)

def agg(df, grouping_field):
    agg_df = all_transactions.groupby(grouping_field) \
            .agg({'value':['sum'],'from':['count', 'nunique']})
    return(agg_df)

def write_to_file(agg_df, df_name):
    agg_df.reset_index(inplace=True) # all columns names at same level
    agg_df.columns = [' '.join(col).strip() for col in agg_df.columns.values]
    #print(agg_df)
    try:
        agg_df.to_parquet(f'{data_prefix}/agg/{df_name}.parquet', index=False)
    except:
        logging.error(f'writing file {df_name}.parquet : {traceback.print_exc()}')
    logging.info(f'wrote file {df_name}.parquet')

by_type = agg_resample(all_transactions, 'type')
write_to_file(by_type, 'by_type_hour')
by_from = agg(all_transactions, 'from')
write_to_file(by_from, 'by_from')

# number of transactions
#print(len(all_transactions.index))
# sum of values
#print(all_transactions['value'].sum())
