# Inseth
## collect Ethereum data to get blockchain insights

App overview :
- ethereum collector is permanently retrieving transaction data from ethereum node and write them to parquet files, partitioned by date
- janitor (To be implemented) : 
  - checks that all blocks are present
  - asynchronously concatenate parquet files (for complete days, with Dask to avoid small row groups)
- For each graph
  - create aggregated dataset 
  - plot with Dash (viz)

![Inseth overview](https://github.com/ululh/inseth/blob/main/inseth.excalidraw.png?raw=true)
