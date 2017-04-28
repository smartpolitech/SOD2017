#Generar el modulo con $slice2py GoogleCalendar.ice ->  pip install zeroc-ice

import sys, traceback, Ice
Ice.loadSlice('GoogleCalendar.ice')
import ModuleGoogleCalendar
import GoogleCalendar as gc
 

class GoogleCalendarImpl(ModuleGoogleCalendar.GoogleCalendarI):
    def checkEvent(self, s, current=None):
        print s
        gc.esEvento(s)
 
status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    adapter = ic.createObjectAdapterWithEndpoints("SimpleGoogleCalendarAdapter", "default -p 10003")
    object = GoogleCalendarImpl()
    adapter.add(object, ic.stringToIdentity("SimpleGoogleCalendar"))
    adapter.activate()
    print("Servidor arrancado")
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