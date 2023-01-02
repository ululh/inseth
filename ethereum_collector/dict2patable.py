%%timeit -r 10
import pyarrow as pa
import random
import string 
import time

large_dict = dict()

for i in range(int(1e6)):
    large_dict[i] = (random.randint(0, 5), random.choice(string.ascii_letters))



schema = pa.schema({
        "chainId"  : pa.binary(),
        "from"  : pa.binary(),
        "gas" : pa.uint32(),
        "gasPrice" : pa.uint32(),
        "input"  : pa.binary(),
        "maxFeePerGas" : pa.uint32(),
        "maxPriorityFeePerGas" : pa.uint32(),
        "nonce" : pa.uint32(),
        "r"  : pa.binary(),
        "s"  : pa.binary(),
        "to"  : pa.binary(),
        "transactionIndex" : pa.uint32(),
        "type"  : pa.binary(),
        "v" : pa.uint32(),
        "value" : pa.uint32(),
        "blockTimestamp" : pa.timestamp(),
        "blockDate", pa.date32([day]))
  })
keys = []
val1 = []
val2 = []
for k, (v1, v2) in large_dict.items():
  keys.append(k)
  val1.append(v1)
  val2.append(v2)

table = pa.Table.from_pydict(
    dict(
        zip(schema.names, (keys, val1, val2))
    ),
    schema=schema
)
