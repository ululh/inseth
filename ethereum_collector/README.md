## ethereum collector

This module connects to an ethereum client (currently alchemy) to retrieve transaction data, remove unused fields and write them in parquet files, partitionned by date
Data is processed in batches of configurable length, one batch = one write

There is no caching of raw data since target architecture is to use a local ethereum node which will be a de facto raw data cache


collector algorithm :
- get latest block from cursor.py config file
- loop forever :
  - Work in batch : retrieve n blocks from ethereum client. For each block :
    - loop to retrieve transactions
      - create a dict for each transaction
      - add block timestamp and date as field for each transaction
      - add transaction dict to transaction list
    - add transaction list to batch transaction list
  - write transactions in parquet files, partitionned (Hive style) by date
  - update latest block in cursor.py

