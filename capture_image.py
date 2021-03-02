import cv2
video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()
cv2.imwrite('person.jpg', frame)
