from os import system
import numpy as np
import face_recognition as fr
import cv2
import logging
from multiprocessing import Process
import keyboard
import sys
from time import sleep
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mailsender import MailSender
from gpiozero import LED, MotionSensor
print("All packages imported sucessful")
video_capture = cv2.VideoCapture(0)

image = fr.load_image_file("person.jpg")
face_encoding = fr.face_encodings(image)[0]

known_face_encondings = [face_encoding]
known_face_names = ["Harish"]

led = LED(14)
pir = MotionSensor(4)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def alert_bot(update, context):
    update.message.reply_text('Alert bot activated')
    logger.info('Alert bot activated send to %s',update.message.chat.username)
    while True:
        try:
            if pir.motion_detected:
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
                video_capture.release()
                sys.exit(0)
        except:
            break

def mail_server(username, password):
    sender = username
    mail_sender = MailSender(username, password)
    logger.info('Mail server initialized and running sucessful')
    
    while True:
        try:
            if pir.motion_detected:
                try:
                    images = [{'id': 'Person', 'path': 'image.jpg'}]
                    logger.info('Sending photo via email')
                    mail_sender.send(sender, ['piharishkumar@gmail.com'], 'Person alert!', images=images)
                    logger.info('Photo send to piharishkumar@gmail.com')
                except:
                    logger.error('Photo send via email failed')
            if keyboard.is_pressed('Ctrl + c'):
                logger.info('Ctrl + c pressed exiting program')
                video_capture.release()
                sys.exit(0)
        except:
            break
        
def face_auth():
    logger.info('Face auth initialized and running sucessful')
    state = 0
    process_this_frame = True
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_this_frame:
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = fr.compare_faces(known_face_encondings, face_encoding)
                name = "Unknown"
                face_distances = fr.face_distance(known_face_encondings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
        process_this_frame = not process_this_frame
        
        if face_names == []:
            if not state == 1:
                state =1
                logger.info('No face found')
                led.off()
        elif name == "Unknown":
            if not state == 2:
                state = 2
                logger.info('Unknown face found')
                led.off()
        elif not state == 3:
            state = 3
            logger.info('Matching face found')
            for face_name in face_names:
                logger.info('Welcome %s',face_name)
            led.on()
        cv2.imwrite('image.jpg', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def start(update, context):
    update.message.reply_text('Bot activated')
    logger.info('Bot activated send to %s',update.message.chat.username)
    Process(target=alert_bot, args=(update, context)).start()

def bop(update, context):
    logger.info('Photo Requested from telegram')
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
    Process(target=mail_server, args=(username, password)).start()
    Process(target=face_auth, args=('')).start()

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
    video_capture.release()
    cv2.destroyAllWindows()