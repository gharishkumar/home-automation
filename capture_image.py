import cv2
video_capture = cv2.VideoCapture(0)
input('Ready press enter to capture image of 1st person')
while True:
    ret, frame = video_capture.read()
    if ret:
        break
cv2.imwrite('Person1_IMG.jpg', frame)
video_capture.release()
video_capture = cv2.VideoCapture(0)
input('Ready press enter to capture image of 2nd person')
while True:
    ret, frame = video_capture.read()
    if ret:
        break
cv2.imwrite('Person2_IMG.jpg', frame)
video_capture.release()
video_capture = cv2.VideoCapture(0)
input('Ready press enter to capture image of 3rd person')
while True:
    ret, frame = video_capture.read()
    if ret:
        break
cv2.imwrite('Person3_IMG.jpg', frame)
video_capture.release()
