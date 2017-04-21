import lxml.html as lh
import urllib2
import datetime as dt
import os.path 
import pickle
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

class Festivos_mes:
  festivos_nacionales = []
  festivos_autonomicos = []
  festivos_locales = []
  def __str__(self):
    return "FN:"+str(self.festivos_nacionales)+"|FA:"+str(self.festivos_autonomicos)+"|FL:"+str(self.festivos_locales)
  
diccionario_festivos = dict()

def obtenerFestivos():
  now = dt.datetime.now()
  url='http://www.calendarioslaborales.com/calendario-laboral-caceres-'+str(now.year)+'.htm'
  page = urllib2.urlopen(url).read()
  soup = BeautifulSoup(page, 'html.parser')

  #print(soup.prettify())

  print "Meses:"

  meses = soup.find_all('div', { 'class' : "mes"})
  conjunto_festivos=""
  for mes in meses:
    festivos_mes = Festivos_mes()
    titulo  = mes.find('div', { 'class' : "tituloMes"})
    print titulo.string + ":"
    diccionario_festivos[titulo.string] = dict() 
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
    
    diccionario_festivos[titulo.string] = festivos_mes
    print conjunto_festivos
    
  return conjunto_festivos
   
def crearArchivoFestivos ():
  if os.path.exists("ArchivosPickle/festivos"+str(dt.datetime.now().year)+".pickle")==False: 
    conjunto_festivos=obtenerFestivos()
    print diccionario_festivos
    os.makedirs('ArchivosPickle')
    pickle.dump(conjunto_festivos, open('ArchivosPickle/festivos'+str(dt.datetime.now().year)+'.pickle', 'w'))
  
  fichero_festivos = pickle.load(open('ArchivosPickle/festivos'+str(dt.datetime.now().year)+'.pickle', 'r'))
  return fichero_festivos

def main():
  crearArchivoFestivos()

if __name__ == "__main__":
    main()