from os import system
import numpy as np
import face_recognition as fr
import cv2
import logging
import threading
import keyboard
import sys
from time import sleep
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mailsender import MailSender
from gpiozero import LED, MotionSensor
#from gpiozero.pins.pigpio import PiGPIOFactory

video_capture = cv2.VideoCapture(0)

image = fr.load_image_file("harish.jpg")
face_encoding = fr.face_encodings(image)[0]

known_face_encondings = [face_encoding]
known_face_names = ["harish"]

#factory = PiGPIOFactory(host='192.168.225.135')
#led = LED(17, pin_factory=factory)
led = LED(17)
pir = MotionSensor(4)

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
                    ret, frame = video_capture.read()
                    cv2.imwrite('image.jpg', frame)
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
    ret, frame = video_capture.read()
    cv2.imwrite('image.jpg', frame)
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

    while True: 
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)
        
        authentication = False

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = fr.compare_faces(known_face_encondings, face_encoding)

            name = "Unknown"

            face_distances = fr.face_distance(known_face_encondings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                authentication = True
                name = known_face_names[best_match_index]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
        if authentication:
            #system('clear')
            logger.info('ok')
            led.on()
        else:
            #system('clear')
            logger.info('U cannot enter')
            led.off()

        cv2.imshow('Webcam_facerecognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if __name__ == '__main__':
    main()

video_capture.release()
cv2.destroyAllWindows()
