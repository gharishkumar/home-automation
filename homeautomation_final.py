import numpy as np
import face_recognition as fr
import cv2
from multiprocessing import Process
from time import sleep
from mailsender import MailSender
from gpiozero import LED, MotionSensor
import logging

video_capture = cv2.VideoCapture(0)
image1 = fr.load_image_file("Person1_IMG.jpg")
face1_encoding = fr.face_encodings(image1)[0]
image2 = fr.load_image_file("Person2_IMG.jpg")
face2_encoding = fr.face_encodings(image2)[0]
image3 = fr.load_image_file("Person3_IMG.jpg")
face3_encoding = fr.face_encodings(image3)[0]
known_face_encondings = [face1_encoding, face2_encoding, face3_encoding]
known_face_names = ["Person1_NAME","Person2_NAME","Person3_NAME"]

led = LED(14)
led.on()
sleep(1)
led.off()
pir = MotionSensor(4)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

username = 'piharishkumar@gmail.com'
password = 'Sivahari9801@rit'
sender = username
mail_sender = MailSender(username, password)
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

    if pir.motion_detected:
        images = [{'id': 'Person', 'path': 'image.jpg'}]
        logger.info('Sending photo via email')
        mail_sender.send(sender, ['piharishkumar@gmail.com'], 'Person alert!', images=images)
        logger.info('Photo send to piharishkumar@gmail.com')
