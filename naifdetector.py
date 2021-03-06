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

argumentsParser = argparse.ArgumentParser()
argumentsParser.add_argument("--tabla", type=str, help='nombre de la tabla en la base de datos', default="UEXCC_TEL_P00_CUA027_SEN001_AGU", required=False)
argumentsParser.add_argument("--dias", type=str, help='se obtienen las medidas hoy-dias hasta hoy', default="90", required=False)
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

periodo = param3

medidas = json.loads(cadenaMedidas)
#pp.pprint(medidas)
cursor = medidas['results'][0]['series'][0]['values']

for medida in cursor:
    fecha = parser.parse(medida[0])
    dia = fecha.weekday()
    hora = fecha.hour
    minuto = fecha.minute
    #minutoMasCercano = int((round(minuto/float(periodo))*periodo)%60)

    if medida[2] > 2:
        print "ALARMA at ", fecha




    