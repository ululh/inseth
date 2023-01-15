# first stage
FROM python:3.10 AS builder
COPY inseth_viz/requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.10-slim
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY inseth_viz/eth_viz.py inseth_viz/eth_viz.py 
COPY utils/ ./utils/

# update PATH environment variable
ENV PATH=/root/.local:$PATH

ENV IN_CONTAINER True

WORKDIR /code/inseth_viz
CMD [ "python", "eth_viz.py" ] 
