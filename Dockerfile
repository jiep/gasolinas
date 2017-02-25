FROM python:3.6.0-alpine

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
# RUN chmod +x wait-for-it.sh
# RUN ./wait-for-it.sh influxdb:8086 -- python3 cargarPrecioGasolina.py
ENTRYPOINT python3 cargarPrecioGasolina.py
