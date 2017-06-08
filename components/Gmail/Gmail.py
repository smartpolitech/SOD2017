import datetime
from email.mime.text import MIMEText
from smtplib import SMTP


def enviarMensaje(fecha):
	from_address = "smartpolitech@gmail.com"
	to_address = "smartpolitech@gmail.com"
	message = "Estimado usuario, \n \n se ha detectado una nueva anomalia. \n \n Mensaje generado por el sistema de monitorizacion de SmartPolitech."
	mime_message = MIMEText(message)
	mime_message["From"] = from_address
	mime_message["To"] = to_address
	mime_message["Subject"] = "Nueva incidencia " + fecha
	smtp = SMTP("smtp.gmail.com", 587)
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	smtp.login(from_address, "opticalflow")
	smtp.sendmail(from_address, to_address, mime_message.as_string())
	smtp.quit()


if __name__ == "__main__":
	fecha = datetime.datetime.now()
 	enviarMensaje(str(fecha))


