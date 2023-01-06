from config import client_url, client_port, number_of_blocks_in_batch, \
    data_dir
from cursor import latest_block
from secret import alchemy_api_key
from web3 import Web3
from datetime import datetime
import logging
from log import *
import traceback
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.dataset as ds

def get_ethereum_client_url():
    if "alchemy.com" in client_url:
        return(f'{client_url}{alchemy_api_key}')
    else:
        return(f'{client_url}:{client_port}/')


def retrieve_block_transactions(block_number):
    transac_list = []
    err_count = 0

    w3 = Web3(Web3.HTTPProvider(get_ethereum_client_url()))

    try:
        block = w3.eth.get_block(block_number)
    except:
        logging.error(f'retrieving block {block_number} : {traceback.print_exc()}')
        return(transac_list, 999) #TO CHECK
    #retrieve block date
    ts = block.timestamp
    dt = datetime.fromtimestamp(ts).date()
    transac_counter = 0
    for transac in block.transactions:
        transac_counter += 1
        try:
            transac_details = w3.eth.get_transaction(transac)
        except:
            err_count += 1
            if err_count < 2:
                logging.error(f'retrieving transaction {transac_counter} from block \
{block_number} : {traceback.print_exc()}')
            elif err_count == 2:
                logging.warning(f'too many errors when retrieving transactions for \
block {block_number}, exceptions logging stopped for this block') 

        dct = dict(transac_details)
        dct["blockTimestamp"] = ts
        dct["blockDate"] = dt
        keys_to_rm = [ "accessList" ]
        for k in keys_to_rm:
            dct.pop(k, None)
        #print(dct)
        transac_list.append(dct)

    logging.info(f'successfully retrieved {transac_counter} transactions from block \
{block_number}, block date {datetime.fromtimestamp(ts)}')
    if err_count > 0:
        logging.warning(f'but {err_count} transaction(s) out of {transac_counter} \
missed')


    return(transac_list, err_count)

        #print(Web3.toJSON(transac_details))
        #w3.eth.get_code(transac_details["to"])
        #print()

def build_pyarrow_table(lst, first_block_number, number_of_blocks_in_batch):
    # define pyarrow table schema
    transac_schema = pa.schema({
            "blockHash"  : pa.binary(),
            "blockNumber" : pa.uint64(),
            "hash"  : pa.binary(),
            "chainId"  : pa.binary(),
            "from"  : pa.string(),
            "gas" : pa.uint64(),
            "gasPrice" : pa.uint64(),
            "input"  : pa.string(),
            "maxFeePerGas" : pa.uint64(),
            "maxPriorityFeePerGas" : pa.uint64(),
            "nonce" : pa.uint64(),
            "r"  : pa.binary(),
            "s"  : pa.binary(),
            "to"  : pa.string(),
            "transactionIndex" : pa.uint32(),
            "type"  : pa.string(),
            "v" : pa.uint32(),
            "value" : pa.decimal128(38),
            "blockTimestamp" : pa.timestamp('s'),
            "blockDate" : pa.date32()
      })
    # convert dict to pyarrow table
    try:
        table = pa.Table.from_pylist(lst, schema=transac_schema)
    except:
        logging.error(f'convering list of dict to pyarrow table from {first_block_number}, \
batch of {number_of_blocks_in_batch} blocks : {traceback.print_exc()}')
    return(table)
    #print(table)

def write_parquet(table, directory, first_block_number, number_of_blocks_in_batch):
    # write to partitioned by date, snappy compressed parquet 
    try:
        ds.write_dataset(
            table,
            directory,
            format="parquet",
            # overwrites file with same name, ignore existing files with no conflicting name
            existing_data_behavior="overwrite_or_ignore",
            basename_template=f'collector-{first_block_number}-{number_of_blocks_in_batch}' \
                + '-{i}.snappy.parquet',
            file_options=ds.ParquetFileFormat().make_write_options(compression='snappy'),
            partitioning=ds.partitioning(
                pa.schema(
                    [
                        ("blockDate", pa.date32())
                    ]
                )
            )
        )
    except:
        logging.error(f'writing parquet file from {first_block_number}, \
batch of {number_of_blocks_in_batch} blocks : {traceback.print_exc()}')
        return(False)
    return(True)
    # TO ANALYZE LATER row groups after concatenation
    #print(parquet_file.num_row_groups)

# main
logging_config()
while True:

    transactions = []
    missed_transac_in_batch = 0
    first_block_in_batch = latest_block + 1
    logging.info(f'starting batch of {number_of_blocks_in_batch} blocks \
from {first_block_in_batch}')

    for i in range(number_of_blocks_in_batch):
        block_number = first_block_in_batch + i
        new_transactions, number_of_errors = retrieve_block_transactions(block_number)
        missed_transac_in_batch += number_of_errors
        transactions.extend(new_transactions)

    if missed_transac_in_batch > 20: # no writing, no cursor update
        logging.warning(f'{missed_transac_in_batch} missed transactions for \
batch of {number_of_blocks_in_batch} blocks starting at {first_block_in_batch}')
        continue

    transac_table = build_pyarrow_table(transactions, first_block_in_batch, number_of_blocks_in_batch)
    write_parquet(transac_table, data_dir, first_block_in_batch, number_of_blocks_in_batch)
    logging.info(f'wrrote parquet file from {first_block_in_batch}, \
batch of {number_of_blocks_in_batch} blocks')
    latest_block = block_number


    # update cursor.py
    try:
        with open('cursor.py','r') as file:
            filedata = file.read()
            filedata = filedata.replace(f'latest_block = {first_block_in_batch-1}',
            f'latest_block = {latest_block}')
        with open('cursor.py','w') as file:
            file.write(filedata)
    except:
        logging.critical(f'unable to update cursor.py file with {latest_block} \
: {traceback.print_exc()}')
        exit()
    logging.info(f'updated cursor.py to latest_block {latest_block}')
