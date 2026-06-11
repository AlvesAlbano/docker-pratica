# FROM locustio/locust:latest

# COPY docker-pratica-invocacao-servicos/requirements.txt /tmp/requirements.txt

# RUN pip install --no-cache-dir -r /tmp/requirements.txt


FROM locustio/locust:latest

RUN pip install --no-cache-dir grpcio grpcio-tools protobuf