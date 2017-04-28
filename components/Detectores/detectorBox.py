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

def calcX(dia, hora, minuto):
    return dia*24*60/param3 + hora*60/param3 + minuto/param3

def interpolate(p1, p2, p):
    a = p2[0] - p1[0]
    b = p2[1] - p1[1]
    
    if a != 0:
        return (b/a)*p - (b*p1[0]/a) + p1[1]
    else:
        return 0

def box(x, puntos):
    for k in range(0, len(puntos)-1):
        if x >= puntos[k][0] and x <= puntos[k+1][0]:
            return interpolate(puntos[k], puntos[k+1], x)
    return 0

def getMeasuresOfAWeek(w):
    fecha = dt.datetime.now()
    diasSemana = fecha.weekday()
        
    if w == 0:
        minutosDesde = fecha.minute + fecha.hour*60 + diasSemana*24*60
        curlCommand = "curl -G 'http://10.253.247.18:8086/query?pretty=true' -u guest:smartpolitech --data-urlencode \"db=sensors\" --data-urlencode \"q=select * from " + param1 + " where time > now() - " + str(minutosDesde) + "m\""
    else:
        minutosDesde = fecha.minute + fecha.hour*60 + diasSemana*24*60 + (w-1)*7*24*60
        minutosHasta = minutosDesde + 60*24*7
        curlCommand = "curl -G 'http://10.253.247.18:8086/query?pretty=true' -u guest:smartpolitech --data-urlencode \"db=sensors\" --data-urlencode \"q=select * from " + param1 + " where time < now() - " + str(minutosDesde) + "m and time > now() - " + str(minutosHasta) + "m\""    
        
    return curlCommand

argumentsParser = argparse.ArgumentParser()
argumentsParser.add_argument("--tabla", type=str, help='nombre de la tabla en la base de datos', default="UEXCC_TEL_P00_CUA027_SEN001_AGU", required=False)
argumentsParser.add_argument("--dias", type=str, help='se obtienen las medidas hoy-dias hasta hoy', default="900", required=False)
argumentsParser.add_argument("--periodo", type=int, help='periodo de medida', default=10, required=False)
argumentsParser.add_argument("--semana", type=int, help='semana actual = 0, semana pasada = 1...', default=0, required=False)
args = argumentsParser.parse_args()

param1 = args.tabla
param2 = args.dias
param3 = args.periodo
param4 = args.semana

pp = pprint.PrettyPrinter(indent=4)

for archivo in os.listdir("models"):
    (nombreFichero, extension) = os.path.splitext(archivo)
    if(extension == ".pickle") and (nombreFichero.startswith(param1)):
        modelo = pickle.load(open('models/'+archivo, 'r'))

args = shlex.split(getMeasuresOfAWeek(param4))

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

puntos = []
for d in range(0,5):
    puntos.append([calcX(d,8,0), 0])
    puntos.append([calcX(d,9,0), 1])
    puntos.append([calcX(d,13,0), 1])
    puntos.append([calcX(d,16,0), 0.7])
    puntos.append([calcX(d,21,0), 0.7])
    puntos.append([calcX(d,22,0), 0])

boxFunction = [box(x, puntos) for x in xList]

plt.plot(xList, boxFunction)
plt.plot(xList, medias)
plt.axis([0, 1008, 0, max(medias)*1.5])
plt.show()