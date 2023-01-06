# first stage
FROM python:3.10 AS builder
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.10-slim
WORKDIR /code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ethereum_client.py .
COPY log.py .
COPY config.py .
COPY secret.py .
COPY cursor.py .

# update PATH environment variable
ENV PATH=/root/.local:$PATH

CMD [ "python", "./ethereum_client.py" ] 
