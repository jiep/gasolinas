# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
import requests
import schedule
import time
import string
import datetime

def parseEstacion(estacion, precio_gasolina, nombre, fecha):
    return [
    {
        "measurement": nombre,
        "tags": {},
        "time": fecha,
        "fields" : {
            "cp": estacion["C.P."],
            "direccion": estacion["Dirección"],
            "horario": estacion["Horario"],
            "latitud": float(estacion["Latitud"].replace(",",".")) if estacion["Latitud"] else None,
            "longitud": float(estacion["Longitud (WGS84)"].replace(",",".")) if estacion["Longitud (WGS84)"] else None,
            "localidad": estacion["Localidad"],
            "margen": estacion["Margen"],
            "municipio": estacion["Municipio"],
            "precio": float(estacion[precio_gasolina].replace(",",".")),
            "rotulo": estacion["Rótulo"],
            "provincia": estacion["Provincia"]
        }
    }]


def getDataAndInsert(client):

    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-10]+"Z"

    tmpl = string.Template("Descargando datos $fecha...")
    print(tmpl.substitute(fecha=fecha))

    URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres"

    r = requests.get(URL)

    data = r.json()

    if(data["ListaEESSPrecio"]):
        for estacion in data["ListaEESSPrecio"]:
            print(fecha)
            if(estacion["Precio Biodiesel"]):
                client.write_points(parseEstacion(estacion, "Precio Biodiesel", "biodiesel", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Bioetanol"]):
                client.write_points(parseEstacion(estacion, "Precio Bioetanol", "bioetanol", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Gas Natural Comprimido"]):
                client.write_points(parseEstacion(estacion, "Precio Gas Natural Comprimido", "gasNaturalComprimido", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Gas Natural Licuado"]):
                client.write_points(parseEstacion(estacion, "Precio Gas Natural Licuado", "gasNaturalLicuado", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Gases licuados del petróleo"]):
                client.write_points(parseEstacion(estacion, "Precio Gases licuados del petróleo", "gasesLicuadosPetroleo", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Gasoleo A"]):
                client.write_points(parseEstacion(estacion, "Precio Gasoleo A", "gasoleoA", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Gasoleo B"]):
                client.write_points(parseEstacion(estacion, "Precio Gasoleo B", "gasoleoB", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Gasolina 95 Protección"]):
                client.write_points(parseEstacion(estacion, "Precio Gasolina 95 Protección", "gasolina95Proteccion", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Gasolina  98"]):
                client.write_points(parseEstacion(estacion, "Precio Gasolina  98", "gasolina98", fecha), database=DATABASE_NAME)
            elif(estacion["Precio Nuevo Gasoleo A"]):
                client.write_points(parseEstacion(estacion, "Precio Nuevo Gasoleo A", "gasoleoA", fecha), database=DATABASE_NAME)

if __name__ == '__main__':
    DATABASE_NAME = "gasolinas_precio"
    HOST = "influxdb"

    client = InfluxDBClient(HOST, 8086)

    databases = client.get_list_database()

    if DATABASE_NAME not in databases:
        client.create_database(DATABASE_NAME)

    schedule.every().hour.do(getDataAndInsert, client)

    while True:
        schedule.run_pending()
        time.sleep(1)

