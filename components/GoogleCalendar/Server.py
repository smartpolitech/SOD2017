#Generar el modulo con $slice2py GoogleCalendar.ice ->  pip install zeroc-ice

import sys, traceback, Ice
sys.path.insert(0, 'Festivos')
sys.path.insert(0, 'GoogleCalendar')

Ice.loadSlice('../interfaces/Event.ice')
Ice.loadSlice('../interfaces/Notification.ice')

import ModuleEvent
import ModuleNotification
import GoogleCalendar as gc
import Festivos as f
import datetime

class GoogleCalendarImpl(ModuleEvent.GoogleCalendarI):
    def checkEvent(self, s, current=None):
        print s
        date = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
        return gc.esEvento(date)


class FestivosImpl(ModuleEvent.FestivosI):
    def checkHoliday(self, s, current=None):
        print s
        date = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
        return f.esFestivo(date)
 
status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints("EventAdapter", "default -p 10003")
    objectGc = GoogleCalendarImpl()
    objectF = FestivosImpl()

    adapter.add(objectGc, ic.stringToIdentity("GoogleCalendar"))
    adapter.add(objectF, ic.stringToIdentity("Festivos"))

    adapter.activate()
    print("Servidor arrancado...")
    ic.waitForShutdown()
except:
    traceback.print_exc()
    status = 1
 
if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1
 
sys.exit(status)
