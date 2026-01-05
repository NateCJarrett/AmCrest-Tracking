import cv2
import credentials
import controls
import time

stream = f"rtsp://{credentials.USERNAME}:{credentials.PASSWORD}@{credentials.IP}:554/cam/realmonitor?channel=1&subtype=1&rstp_transport=udp"
cap = cv2.VideoCapture(stream, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x = width // 2
center_y = height // 2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
horizontal_offset = 0
vertical_offset = 0

current_direction = None
last_command_time = 0
PTZ_INTERVAL = 0.2  # 5 Hz max

while True:
    cap.grab()
    ret, frame = cap.retrieve()

    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        horizontal_offset = (x + w // 2) - center_x
        vertical_offset = (y + h // 2) - center_y
    else:
        horizontal_offset = 0
        vertical_offset = 0

    now = time.time()
    new_direction = None

    if abs(horizontal_offset) > 40:
        new_direction = "Right" if horizontal_offset > 0 else "Left"
    elif abs(vertical_offset) > 40:
        new_direction = "Down" if vertical_offset > 0 else "Up"

    # Only send PTZ command if direction changes AND rate limit allows
    if new_direction != current_direction and now - last_command_time > PTZ_INTERVAL:
        if current_direction is not None:
            controls.ptz_stop()

        if new_direction is not None:
            if new_direction == "Right":
                controls.move_right()
            elif new_direction == "Left":
                controls.move_left()
            elif new_direction == "Up":
                controls.move_up()
            elif new_direction == "Down":
                controls.move_down()

        current_direction = new_direction
        last_command_time = now

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
#cv2.destroyAllWindows()
controls.manual()