# first stage
FROM python:3.10 AS builder
COPY ethereum_collector/requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.10-slim
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ethereum_collector/ethereum_client.py ethereum_collector/ethereum_client.py 
COPY utils/ ./utils/
COPY ethereum_collector/config.py ethereum_collector/config.py
COPY ethereum_collector/secret.py ethereum_collector/secret.py
COPY ethereum_collector/collector_cursor.py ethereum_collector/collector_cursor.py

# update PATH environment variable
ENV PATH=/root/.local:$PATH

ENV IN_CONTAINER True

WORKDIR /code/ethereum_collector
CMD [ "python", "ethereum_client.py" ] 
