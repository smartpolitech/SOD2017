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
from scipy.integrate import simps

compensacionGMT = 0

def savitzky_golay(y, window_size, order, deriv=0):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay
filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techhniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only
smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv]
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs(y[1:half_window+1][::-1] - y[0])
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m, y, mode='valid')

def checkZero(anclajesY):
    for i in anclajesY:
        if i == 0:
            return True
    return False

def fitnessSimpson(anclajesY, anclajesX, medidas):

    l1 = simps(anclajesY, x=anclajesX)
    l2 = simps(medidas, dx=1)
    le = abs(l1-l2)

    return le

def calculateBox(modelo, dia):

    anclajesX = [(8-compensacionGMT)*60/periodo, #(8-compensacionGMT)*60/periodo + 30/periodo,
                 #(9-compensacionGMT)*60/periodo, #(9-compensacionGMT)*60/periodo + 30/periodo,
                 (10-compensacionGMT)*60/periodo, #(10-compensacionGMT)*60/periodo + 30/periodo,
                 #(11-compensacionGMT)*60/periodo, #(11-compensacionGMT)*60/periodo + 30/periodo,
                 (12-compensacionGMT)*60/periodo, #(12-compensacionGMT)*60/periodo + 30/periodo,
                 #(13-compensacionGMT)*60/periodo, #(13-compensacionGMT)*60/periodo + 30/periodo,
                 (14-compensacionGMT)*60/periodo, #(14-compensacionGMT)*60/periodo + 30/periodo,
                 #(15-compensacionGMT)*60/periodo, #(15-compensacionGMT)*60/periodo + 30/periodo,
                 (16-compensacionGMT)*60/periodo, #(16-compensacionGMT)*60/periodo + 30/periodo,
                 #(17-compensacionGMT)*60/periodo, #(17-compensacionGMT)*60/periodo + 30/periodo,
                 (18-compensacionGMT)*60/periodo, #(18-compensacionGMT)*60/periodo + 30/periodo,
                 #(19-compensacionGMT)*60/periodo, #(19-compensacionGMT)*60/periodo + 30/periodo,
                 (20-compensacionGMT)*60/periodo, #(20-compensacionGMT)*60/periodo + 30/periodo,
                 #(21-compensacionGMT)*60/periodo, #(21-compensacionGMT)*60/periodo + 30/periodo,
                 (22-compensacionGMT)*60/periodo] #(22-compensacionGMT)*60/periodo + 30/periodo]
    medidas = []

    for d in range(0,7):
        for h in range(0,24):
            for m in range(0,60,periodo):
                medidas.append(modelo[d][h][m]['average'])

    for h in range(0,24):
        for m in range(0,60,periodo):
            medidas.append(modelo[dia][h][m]['average'])
        
    leAnt = 10000
    # solucion = []
    # for i in range(0,10000):
    #     anclajesY = np.random.uniform(0, 3, size=len(anclajesX))
        
    #     #metodo que calcule el fitness
    #     le = fitnessSimpson(anclajesY, anclajesX, medidas)
                
    #     if le < leAnt and not checkZero(anclajesY):
    #         leAnt = le
    #         solucion = anclajesY
    #         print le, solucion
    #     elif le < 1.0:
    #         break
    #     elif np.random.randint(0, 100, 1) < np.int(5):
    #         leAnt = le
        
    # SMOOTHING por le método de Savitzky-Golay
    med = np.array(medidas)
    smooth = savitzky_golay(med, 51, 3)

    print len(smooth), len(medidas), len(range(0, 24*60/periodo))

    plt.plot(range(0, 7*24*60/periodo), smooth)
    plt.plot(range(0, 7*24*60/periodo), medidas)

    med = np.array(medidas)
    smooth = savitzky_golay(med, 51, 3)
    plt.plot(range(0, 24*60/periodo),smooth)
    plt.plot(range(0, 24*60/periodo),medidas)

    plt.show()

  # SMOOTHING por le método de Ramer-Douglas-Peucker algorithm





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
argumentsParser.add_argument("--dia", type=int, help='dia de la semana', default=0, required=False)

args = argumentsParser.parse_args()

param1 = args.tabla
param2 = args.dias
param3 = args.periodo
param4 = args.semana
param5 = args.dia

pp = pprint.PrettyPrinter(indent=4)

for archivo in os.listdir("../../models"):
    (nombreFichero, extension) = os.path.splitext(archivo)
    if(extension == ".pickle") and (nombreFichero.startswith(param1)):
        modelo = pickle.load(open('../../models/'+archivo, 'r'))

args = shlex.split(getMeasuresOfAWeek(param4))

process = Popen(args, stdout=PIPE, stderr=PIPE)
cadenaMedidas, err = process.communicate()

periodo = param3

medidas = json.loads(cadenaMedidas)
cursor = medidas['results'][0]['series'][0]['values']

semana = dict()
for d in range(0,7):
    semana[d] = dict()
    for h in range(0,24):
        semana[d][h] = dict()
        for m in range(0,60,periodo):
            semana[d][h][m] = {"valor": 0.0}

for medida in cursor:
    fecha = parser.parse(medida[0])
    dia = fecha.weekday()
    hora = fecha.hour
    minuto = fecha.minute
    minutoMasCercano = int((round(minuto/float(periodo))*periodo)%60)
        
    semana[dia][hora][minutoMasCercano]['valor'] = medida[1]

for archivo in os.listdir("../../models"):
    (nombreFichero, extension) = os.path.splitext(archivo)
    if(extension == ".pickle") and (nombreFichero.startswith(param1)):
        modelo = pickle.load(open('../../models/'+archivo, 'r'))

valores = []
for d in range(0,7):
    for h in range(0,24):
        for m in range(0,60,periodo):
            valores.append(float(modelo[d][h][m]['average']))
print np.mean(valores[(8-compensacionGMT)*60/periodo:(22-compensacionGMT)*60/periodo])

xList = range(len(valores))

puntos = []
for d in range(0,5):
    puntos.append([calcX(d,8-compensacionGMT,0), 0])
    puntos.append([calcX(d,9-compensacionGMT,0), 1])
    puntos.append([calcX(d,13-compensacionGMT,0), 1])
    puntos.append([calcX(d,16-compensacionGMT,0), 0.7])
    puntos.append([calcX(d,21-compensacionGMT,0), 0.7])
    puntos.append([calcX(d,22-compensacionGMT,0), 0])

#for dia in range(0,7):
calculateBox(modelo, param5)

#boxFunction = [box(x, puntos) for x in xList]
#plt.plot(xList, boxFunction)
#plt.plot(xList, valores)
#plt.axis([0, len(valores), 0, max(valores)*1.5])
#plt.show()
#plt.show()
