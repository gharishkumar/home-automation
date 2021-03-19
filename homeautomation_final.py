#!/bin/python3
import cv2
import numpy as np
import face_recognition as fr
from gpiozero import LED, MotionSensor, Servo
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep

led = LED(14)
led.on()
sleep(1)
led.off()
servo = Servo(17)
servo.min()
pir = MotionSensor(4)

video_capture = cv2.VideoCapture(0)
image1 = fr.load_image_file("Person1_IMG.jpg")
face1_encoding = fr.face_encodings(image1)[0]
image2 = fr.load_image_file("Person2_IMG.jpg")
face2_encoding = fr.face_encodings(image2)[0]
image3 = fr.load_image_file("Person3_IMG.jpg")
face3_encoding = fr.face_encodings(image3)[0]
known_face_encondings = [face1_encoding, face2_encoding, face3_encoding]
#change thess with your details
known_face_names = ["Person1_NAME","Person2_NAME","Person3_NAME"]  

sender_email = "YOUR_EMAIL"
sender_name = "YOUR_NAME"
password = "YOUR_PASSWORD"

receiver_emails = ["RECEIVER_EMAIL_1", "RECEIVER_EMAIL_2", "RECEIVER_EMAIL_3"]
receiver_names = ["RECEIVER_NAME_1", "RECEIVER_NAME_2", "RECEIVER_NAME_3"]

state = 0
process_this_frame = True
while True:
    try:
        while True:
            ret, frame = video_capture.read()
            if ret:                             #to avoid void data
                break
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) #scale down image to reduce processing time
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
        
        if face_names == []:  #no face found
            if not state == 1:
                state =1
                servo.min()
                led.off()
        elif name == "Unknown": #Unknown face found
            if not state == 2:
                state = 2
                servo.min()
                led.off()
        elif not state == 3: #Matching face found
            state = 3
            servo.max()
            led.on()
        cv2.imwrite("image.jpg", frame)

        if pir.motion_detected: #On PIR trigger send e-mail
            filename = "image.jpg"
            for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
                msg = MIMEMultipart()
                msg["To"] = formataddr((receiver_name, receiver_email))
                msg["From"] = formataddr((sender_name, sender_email))
                msg["Subject"] = "Person at door!"
                with open(filename, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition",f"attachment; filename= {filename}",)
                msg.attach(part)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception:
        pass
