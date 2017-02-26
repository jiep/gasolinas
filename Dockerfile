FROM python:3.6.0-alpine

ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 cargarPrecioGasolina.py
