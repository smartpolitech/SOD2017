
#Instalar pip install --upgrade google-api-python-client
from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import json
import datetime

import dateutil.parser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: 
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def esEvento(fecha):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    fechaMedida = fecha

    fecha = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
    fechaIni = fecha.isoformat() + 'Z'
    fecha = fecha.replace(hour=23, minute=59, second=59, microsecond=0)
    fechaFin = fecha.isoformat() + 'Z'
    

    eventsResult = service.events().list(calendarId='escuelapolitecnicacc@gmail.com', timeZone='Europe/London', timeMin=fechaIni,timeMax=fechaFin, singleEvents=True, orderBy='startTime').execute()


    events = eventsResult.get('items', [])

    if not events:
        print('No hay eventos')
        return False
    else:
        for event in events:
            print("Inicio evento: ",fechaMedida.hour) 
            print("Inicio evento: ",fechaMedida.minute)
            if 'summary' in event:
                print("Nombre evento: ",event['summary'])

            if 'start' in event:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start)
                startFormat = dateutil.parser.parse(start)

                #startFormat = startFormat.isoformat() + 'Z'
                print("Inicio evento: ",startFormat.hour)
                print("Inicio evento: ",startFormat.minute)


            if 'end' in event:
                end = event['end'].get('dateTime', event['end'].get('date'))
                print(end)
                endFormat = dateutil.parser.parse(end)
                #endFormat = endFormat.isoformat() + 'Z'

                print("Inicio evento: ",endFormat.hour)
                print("Inicio evento: ",endFormat.minute)           
            
            if fechaMedida.hour > startFormat.hour and fechaMedida.hour < endFormat.hour:
                return True
            elif fechaMedida.hour == startFormat.hour and fechaMedida.minute >= startFormat.minute:
                return True 
            elif fechaMedida.hour == endFormat.hour and fechaMedida.minute <= endFormat.minute:
                return True 
                
        return False 



if __name__ == '__main__':
    fecha = datetime.datetime.now()
    fecha = fecha.replace(hour=12, minute=0)
    print(esEvento(fecha))



