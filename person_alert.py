#!/usr/bin/env python
# from picamera import PiCamera
# from gpiozero import MotionSensor
# pir = MotionSensor(4)
import logging
import threading
import keyboard
import sys
from time import sleep
from VideoCapture import Device
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mailsender import MailSender

cam = Device()

# camera = PiCamera()

# def capture():
#     timestamp = datetime.now().isoformat()
#     camera.capture('image.jpg')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def alert_bot(update, context):
    update.message.reply_text('Alert bot activated')
    logger.info('Alert bot activated send to %s',update.message.chat.username)
    while True:
        try:
            if keyboard.is_pressed('ENTER'):
            # if pir.motion_detected:
                try:
                    update.message.reply_text('Person alert!')
                    logger.info('Person alert! send to %s',update.message.chat.username)
                    logger.info('Sending photo via Telegram')
                    sleep(2)
                    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('image.jpg', 'rb'))
                    logger.info('Photo send to %s', update.message.chat.username)
                except:
                    logger.error('Photo via Telegram failed')
            if keyboard.is_pressed('Ctrl + c'):
                logger.info('Ctrl + c pressed exiting program')
                sys.exit(0)
        except:
            break

def mail_server(username, password):
    sender = username
    mail_sender = MailSender(username, password)
    logger.info('Mail server initialized and running sucessful')
    
    while True:
        try:
            if keyboard.is_pressed('ENTER'):
            # if pir.motion_detected:
                try:
                    cam.saveSnapshot('image.jpg',timestamp=1)
                    # capture()
                    images = [{'id': 'Person', 'path': 'image.jpg'}]
                    logger.info('Sending photo via email')
                    mail_sender.send(sender, ['piharishkumar@gmail.com'], 'Person alert!', images=images)
                    logger.info('Photo send to piharishkumar@gmail.com')
                except:
                    logger.error('Photo send via email failed')
            if keyboard.is_pressed('Ctrl + c'):
                logger.info('Ctrl + c pressed exiting program')
                sys.exit(0)
        except:
            break

def start(update, context):
    update.message.reply_text('Bot activated')
    logger.info('Bot activated send to %s',update.message.chat.username)
    threading.Thread(target=alert_bot, args=(update, context)).start()

def bop(update, context):
    logger.info('Photo Requested from telegram')
    logger.info('Capturing photo')
    cam.saveSnapshot('image.jpg',timestamp=1)
    logger.info('Sending photo')
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('image.jpg', 'rb'))
    logger.info('Photo send to %s', update.message.chat.username)

def echo(update, context):
    update.message.reply_text(update.message.text)
    logger.info('%s reply send to %s',update.message.text, update.message.chat.username)


def error(update, context):
    logger.warning('Update %s caused error %s', update, context.error)


def main():
    username = 'piharishkumar@gmail.com'
    password = 'Sivahari9801@rit'
    threading.Thread(target=mail_server, args=(username, password)).start()

    updater = Updater("1529116848:AAFaV6huMtiE1lfatvvIKZg_ZK_uIEZF8uY", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bop",bop))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info('Telegram bot initialized u need to send /start to activate')
    updater.idle()

if __name__ == '__main__':
    main()