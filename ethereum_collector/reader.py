import pandas as pd 
import sys

parquet_file = sys.argv[1]
content = pd.read_parquet(parquet_file, engine='pyarrow')
print(content[content.columns[2:4]])
