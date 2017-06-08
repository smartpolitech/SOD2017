import telebot 
import datetime

TOKEN = '269503391:AAHcNYSvbBV3ndNu8FY9K9Dl6dTyTVChuf8' 
tb = telebot.TeleBot(TOKEN) 



def enviarMensaje(fecha):
	tb.send_message("@notificationsSP", "Se ha detectado una anomalia con fecha " +  fecha) 


if __name__ == "__main__":
	fecha = datetime.datetime.now()
 	enviarMensaje(str(fecha))
