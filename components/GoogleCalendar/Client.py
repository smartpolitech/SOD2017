#Generar el modulo con $slice2py GoogleCalendar.ice  ->  pip install zeroc-ice

import sys, traceback, Ice
Ice.loadSlice('GoogleCalendar.ice')
import ModuleGoogleCalendar
import datetime
import dateutil.parser

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy("SimpleGoogleCalendar:default -p 10003")
    googleCalendar = ModuleGoogleCalendar.GoogleCalendarIPrx.checkedCast(base)
    if not googleCalendar:
        raise RuntimeError("Invalid proxy")
 


    #googleCalendar.checkEvent("Hola")


    fecha = datetime.datetime.now()
    fecha = fecha.replace(hour=12, minute=0)
    print(googleCalendar.checkEvent(str(fecha)))



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