import cv2
import credentials
import controls
from time import sleep

stream = f"rtsp://{credentials.USERNAME}:{credentials.PASSWORD}@{credentials.IP}:554/cam/realmonitor?channel=1&subtype=1&rstp_transport=udp"
cap = cv2.VideoCapture(stream, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x = width // 2
center_y = height // 2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
frame_count = 0
horizontal_offset = 0
vertical_offset = 0

controls.face_forward()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        horizontal_offset = center_x - (x + w // 2)
        vertical_offset = center_y - (y + h // 2)

    if(horizontal_offset > 15):
        controls.move_left()
    elif(horizontal_offset < -15):
        controls.move_right()
    elif(vertical_offset > 15):
        controls.move_down()
    elif(vertical_offset < -15):
        controls.move_up()
    else:
        controls.ptz_stop()

    print(f"Horizontal Offset: {horizontal_offset}, Vertical Offset: {vertical_offset}")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

controls.manual()