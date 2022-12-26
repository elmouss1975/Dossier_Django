from django.db import models
from django.core.mail import send_mail
import datetime
from datetime import *
import requests
# Fonction d'envoi de  message Telegram
def telegram_bot_sendtext(bot_message):

   bot_token = '2104539218:AAEwJhKvPgOEguTX_3iXBSMqwCp4BYIS8kQ'
   bot_chatID = '1852446447'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
   response = requests.get(send_text)
   print(response)
   return response.json()
def send_telegram(msg):
    BOT_API_KEY = '5877107934:AAEdLO-UzbBcdLKYBoW5LAuR783oCfeptdI'
    CHAT_ID = '1242839034'
    url_bot = "https://api.telegram.org/bot" + BOT_API_KEY + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + msg
    response = requests.get(url_bot)
    print(response)
    return response.json()

class Ds18b20(models.Model):  # creation du modele gardant la temperature  et la date
    tmp = models.FloatField(null=True)
    vbat = models.FloatField(null=True)
    dt = models.DateTimeField(auto_now_add=True)  # la date s'enregistre automatiquement

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        # return '%s:  %s' % (self.temp,self.dt)
        return str(self.tmp)

    #  Envoyer Mail et telegram
    def save(self, *args, **kwargs):
        now = datetime.now()
        if self.tmp > 25.0:
            # send_whatsapp="https://api.callmebot.com/whatsapp.php?phone=+212653932383&text=temperature+hors+norme:" + str(self.tmp) + "&apikey=562529"
            # requests.get(send_whatsapp)
            telegram_bot_sendtext(str(self.tmp))
            send_telegram(str(self.tmp))
            send_mail(
                'Alert temperature',
                'Derniere valeur '+str(self.tmp) + ' enregistree le ' +str(now.strftime("%Y-%m-%d %H:%M")) +  ' est superieur a la valeur normal ',
                'a.elmoussati@ump.ac.ma',
                ['a.elmoussati@ump.ac.ma','elmouss@yahoo.com'],
                fail_silently=False,
                )
        if self.tmp <=-127:
            # send_whatsapp="https://api.callmebot.com/whatsapp.php?phone=+212653932383&text=Sonde+hors+service.+Merci+de+verifier"+ "&apikey=562529"
            # requests.get(send_whatsapp)
            telegram_bot_sendtext('erreur materiel:'+str(self.tmp))
            send_telegram('erreur materiel:'+str(self.tmp))
            send_mail(
                'Alert temperature',
                'Erreur materiel :'+ str(self.tmp) + ' enregistree le ' +str(now.strftime("%Y-%m-%d %H:%M")) +  ' ;Merci de verifier votre sonde ',
                'latifiotduess@gmail.com',
                ['latif.duess@gmail.com','aghzarmostafa@gmail.com'],
                fail_silently=False,
                )
        if self.vbat <3000:
            telegram_bot_sendtext('Pensez à changer votre batterie, valeur actuelle de la batterie est :'+str(self.vbat)+'mV')
            send_telegram('Pensez à changer votre batterie, valeur actuelle de la batterie est :'+str(self.vbat)+'mV')
            send_mail(
                'Alert Batterie',
                'Pensez à changer votre batterie, valeur actuelle de la batterie est :'+str(self.vbat)+'mV',
                'latifiotduess@gmail.com',
                ['latif.duess@gmail.com','aghzarmostafa@gmail.com'],
                fail_silently=False,
                )
        return super().save(*args, **kwargs)