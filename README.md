# Inseth
## collect Ethereum data to get blockchain insights

App overview :
- ethereum collector is permanently retrieving transaction data from ethereum node and write them to parquet files
- janitor (To be implemented) : 
  - checks that all blocks are present
  - asynchronously concatenate parquet files (daily, with Dask to avoid small row groups)
- For each graph
 - create aggregated dataset (aggregator)
 - plot with Dash (viz)


