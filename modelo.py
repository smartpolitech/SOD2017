# -*- coding: utf-8 -*-

import sys, json, pprint
import datetime as dt
from dateutil import parser
from subprocess import call, Popen, PIPE
import ConfigParser
import shlex
import pickle
import argparse
import matplotlib.pyplot as plt

compensacionGMT = 0

argumentsParser = argparse.ArgumentParser()
argumentsParser.add_argument("--tabla", type=str, help='nombre de la tabla en la base de datos', default="UEXCC_TEL_P00_CUA027_SEN001_AGU", required=False)
argumentsParser.add_argument("--dias", type=str, help='se obtienen las medidas hoy-dias hasta hoy', default="900", required=False)
argumentsParser.add_argument("--periodo", type=int, help='periodo de medida', default=10, required=False)
args = argumentsParser.parse_args()

param1 = args.tabla
param2 = args.dias
param3 = args.periodo

pp = pprint.PrettyPrinter(indent=4)

curlCommand = "curl -G 'http://10.253.247.18:8086/query?pretty=true' -u guest:smartpolitech --data-urlencode \"db=sensors\" --data-urlencode \"q=select * from " + param1 + " where time > now() - " + param2 + "d\""
args = shlex.split(curlCommand)

process = Popen(args, stdout=PIPE, stderr=PIPE)
cadenaMedidas, err = process.communicate()

semana = dict()
periodo = param3  #se divide la semana en periodo minutos
for d in range(0,7):
    semana[d] = dict()
    for h in range(0,24):
        semana[d][h] = dict()
        for m in range(0,60,periodo):
            semana[d][h][m] = {"total": 0.0, "count": 0, "average": 0.0, "variance": 0.0}


medidas = json.loads(cadenaMedidas)
cursor = medidas['results'][0]['series'][0]['values']
for medida in cursor:
    fecha = parser.parse(medida[0])
    dia = fecha.weekday()
    hora = fecha.hour
    minuto = fecha.minute
    minutoMasCercano = int((round(minuto/float(periodo))*periodo)%60)

    if (hora-compensacionGMT >= 8 and hora-compensacionGMT <= 21) and (dia <= 4):
        #print dia, hora, minuto, minutoMasCercano
        
        semana[dia][hora][minutoMasCercano]['total'] += medida[1]
        
        semana[dia][hora][minutoMasCercano]['count'] += 1
        
        contador = semana[dia][hora][minutoMasCercano]['count']
        mediaAnterior = semana[dia][hora][minutoMasCercano]['average']
        semana[dia][hora][minutoMasCercano]['average'] += (medida[1] - mediaAnterior)/contador
        
        semana[dia][hora][minutoMasCercano]['variance'] += (medida[1] - mediaAnterior) * (medida[1] - semana[dia][hora][minutoMasCercano]['average'])
    
pp.pprint(semana)

pickle.dump(semana, open("models/"+param1+"_"+str(dt.datetime.today().strftime("%Y-%m-%d"))+".pickle", 'w'))

medidas = []
for d in range(0,7):
    for h in range(0,24):
        for m in range(0,60,periodo):
            medidas.append(semana[d][h][m]['average'])


plt.plot(medidas)
plt.axis([0, len(medidas), 0, 4])
plt.show()
