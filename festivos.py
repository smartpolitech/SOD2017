import lxml.html as lh
import urllib2
from datetime import datetime, date, timedelta
import os.path 
import pickle
import sys

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class Festivos_mes:
  festivos_nacionales = []
  festivos_autonomicos = []
  festivos_locales = []
  def __init__(self):
    self.festivos_nacionales = []
    self.festivos_autonomicos = []
    self.festivos_locales = []
  def __str__(self):
    return "FN:"+str(self.festivos_nacionales)+"|FA:"+str(self.festivos_autonomicos)+"|FL:"+str(self.festivos_locales)
  
diccionario_festivos = dict()
sys.setrecursionlimit(10000)
def obtenerFestivos():
  now = dt.datetime.now()
  url='http://www.calendarioslaborales.com/calendario-laboral-caceres-'+str(now.year)+'.htm'
  page = urllib2.urlopen(url).read()
  soup = BeautifulSoup(page, 'html.parser')

  #print(soup.prettify())

  print "Meses:"

  meses = soup.find_all('div', { 'class' : "mes"})
  conjunto_festivos=""
  num_mes = 1
  for mes in meses:
    festivos_mes = Festivos_mes()
    titulo  = mes.find('div', { 'class' : "tituloMes"})
    #print titulo.string + ":"
    festivos_nacionales = mes.find_all('td', {'class' : "cajaFestivoN"})
    festivos_autonomicos = mes.find_all('td', {'class' : "cajaFestivoR"})
    festivos_locales = mes.find_all('td', {'class' : "cajaFestivoP"})
    conjunto_festivos="FN:"
    for festn in festivos_nacionales:
      festivos_mes.festivos_nacionales.append(festn.string)
      conjunto_festivos+=festn.string+","
    conjunto_festivos+="FA:"
    for festa in festivos_autonomicos:
      festivos_mes.festivos_autonomicos.append(festa.string)
      conjunto_festivos+=festa.string+","
    conjunto_festivos+="FL:"
    for festl in festivos_locales:
      festivos_mes.festivos_locales.append(festl.string)
      conjunto_festivos+=festl.string+","  
    
    diccionario_festivos[num_mes] = festivos_mes
    #print conjunto_festivos
    num_mes+=1
  
  return conjunto_festivos
   
def crearArchivoFestivos ():
  if os.path.exists("ArchivosPickle/festivos"+str(datetime.now().year)+".pickle")==False: 
    conjunto_festivos=obtenerFestivos()
    print diccionario_festivos
    for festivo in diccionario_festivos:
      print festivo, diccionario_festivos[festivo]
    if os.path.exists("ArchivosPickle")==False: 
      os.makedirs('ArchivosPickle')
    pickle.dump(diccionario_festivos, open('ArchivosPickle/festivos'+str(datetime.now().year)+'.pickle', 'w'))
  
  else: 
    fichero_festivos = pickle.load(open('ArchivosPickle/festivos'+str(datetime.now().year)+'.pickle', 'r'))
    for festivo in fichero_festivos:
      print festivo, fichero_festivos[festivo]
    diccionario_festivos = fichero_festivos   
    
    return diccionario_festivos

def esFestivo(fecha):
  es_festivo=False
  diccionario_festivos=crearArchivoFestivos()
  festivos_mes = diccionario_festivos[fecha.month]
  if str(fecha.day) in festivos_mes.festivos_nacionales or str(fecha.day) in festivos_mes.festivos_autonomicos or str(fecha.day) in festivos_mes.festivos_locales:
    es_festivo=True
    
  return es_festivo  

def main():
  fecha=datetime.now()
  es_festivo= esFestivo(fecha)
  if es_festivo:
    print "Es festivo " + str(fecha)
  else:
    print "No es festivo " + str(fecha)
  

if __name__ == "__main__":
    main()
    