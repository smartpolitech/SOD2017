# -*- coding: utf-8 -*-

import sys, json, pprint
import datetime as dt
from dateutil import parser
from subprocess import call, Popen, PIPE
import ConfigParser
import shlex
import pickle
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np


def gaussian(x):
    horaPico = 15
    mu = [horaPico*6+y for y in range(0, 1008, 144) ]
    sig = 10.0
    return      np.exp(-np.power(x - mu[0], 2.0) / (2 * np.power(sig, 2.0)))    \
            +   np.exp(-np.power(x - mu[1], 2.0) / (2 * np.power(sig, 2.0)))    \
            +   np.exp(-np.power(x - mu[2], 2.0) / (2 * np.power(sig, 2.0)))    \
            +   np.exp(-np.power(x - mu[3], 2.0) / (2 * np.power(sig, 2.0)))    \
            +   np.exp(-np.power(x - mu[4], 2.0) / (2 * np.power(sig, 2.0)))    \
            +   0.01 * np.exp(-np.power(x - mu[5], 2.0) / (2 * np.power(sig, 2.0)))    \
            +   0.01 * np.exp(-np.power(x - mu[6], 2.0) / (2 * np.power(sig, 2.0)))

def getMeasuresOfAWeek(w):
    fecha = dt.datetime.now()
    diasSemana = fecha.weekday()
    
    if w == 0:
        minuto2 = fecha.minute + fecha.hour*60 + diasSemana*60*24
        minuto1 = 0
    else:
        minuto2 = fecha.minute + fecha.hour*60 + w*diasSemana*60*24
        minuto1 = minuto2 + 24*7*60
    
    curlCommand = "curl -G 'http://10.253.247.18:8086/query?pretty=true' -u guest:smartpolitech --data-urlencode \"db=sensors\" --data-urlencode \"q=select * from " + param1 + " where time > now() - " + str(minuto1) + "m and time < now() - " + str(minuto2) + "m\""
    
    return curlCommand

argumentsParser = argparse.ArgumentParser()
argumentsParser.add_argument("--tabla", type=str, help='nombre de la tabla en la base de datos', default="UEXCC_TEL_P00_CUA027_SEN001_AGU", required=False)
argumentsParser.add_argument("--dias", type=str, help='se obtienen las medidas hoy-dias hasta hoy', default="900", required=False)
argumentsParser.add_argument("--periodo", type=int, help='periodo de medida', default=10, required=False)
args = argumentsParser.parse_args()

param1 = args.tabla
param2 = args.dias
param3 = args.periodo

pp = pprint.PrettyPrinter(indent=4)

for archivo in os.listdir("models"):
    (nombreFichero, extension) = os.path.splitext(archivo)
    if(extension == ".pickle") and (nombreFichero.startswith(param1)):
        modelo = pickle.load(open('models/'+archivo, 'r'))

#pendiente revisar curlcommand y lo que se pinta

args = shlex.split(getMeasuresOfAWeek(2))

process = Popen(args, stdout=PIPE, stderr=PIPE)
cadenaMedidas, err = process.communicate()

periodo = param3

medidas = json.loads(cadenaMedidas)
cursor = medidas['results'][0]['series'][0]['values']

medias = []
for medida in cursor:
    fecha = parser.parse(medida[0])
    dia = fecha.weekday()
    hora = fecha.hour
    minuto = fecha.minute
    minutoMasCercano = int((round(minuto/float(periodo))*periodo)%60)
    
    media = modelo[dia][hora][minutoMasCercano]['average']
    
    medias.append(media)

xList = range(len(medias))
gaussianFunction = [gaussian(x) for x in xList]

plt.plot(xList, gaussianFunction)
plt.plot(xList, medias)

plt.axis([0, 1008, 0, 2])
plt.show()