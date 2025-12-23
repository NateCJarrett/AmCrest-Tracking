import requests
import keyboard
import credentials
from requests.auth import HTTPDigestAuth
from time import sleep

URL = f"http://{credentials.IP}/cgi-bin/ptz.cgi"
AUTH = HTTPDigestAuth(credentials.USERNAME, credentials.PASSWORD)
SPEED = 3

def ptz_move(direction, vertical=SPEED, horizontal=SPEED):
    params = {
        "action": "start",
        "channel": 0,
        "code": direction,
        "arg1": vertical,
        "arg2": horizontal,
        "arg3": 0
    }
    response = requests.get(URL, params=params, auth=AUTH, timeout=2)
    # print(response.status_code, response.text, response.headers)

def ptz_stop():
    params = {
        "action": "stop",
        "channel": 0,
        "code": "Up",
        "arg1": 0,
        "arg2": 0,
        "arg3": 0
    }
    response = requests.get(URL, params=params, auth=AUTH, timeout=2)
    # print(response.status_code, response.text, response.headers)

def move_up():
    ptz_move("Up")

def move_down():
    ptz_move("Down")

def move_left():
    ptz_move("Left")

def move_right():
    ptz_move("Right")

def face_forward(): # Non-functioning
    params = {
        "action": "goto",
        "channel": 0,
        "code": "Position",
        "arg1": 1,
        "arg2": 0,
        "arg3": 0
    }
    response = requests.get(URL, params=params, auth=AUTH, timeout=2)
    print(response.status_code, response.text, response.headers)

def controller(key):
    if keyboard.is_pressed(key):
        ptz_move(key)

def stopped():
    if not keyboard.is_pressed("Up") and not keyboard.is_pressed("Down") and not keyboard.is_pressed("Left") and not keyboard.is_pressed("Right"):
        ptz_stop()

def manual():
    face_forward()
    
    print("Listening for keyboard inputs. Press ESC to exit.")
    while not keyboard.is_pressed("esc"):
        controller("Up")
        controller("Down")
        controller("Left")
        controller("Right")
        stopped()

if __name__ == "__main__": # Manual Controls
    manual()

