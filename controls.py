import requests
import keyboard
from requests.auth import HTTPDigestAuth
from time import sleep

URL = "http://192.168.1.108/cgi-bin/ptz.cgi"
AUTH = HTTPDigestAuth("admin", "admin123")
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

if __name__ == "__main__":
    def controller(key):
        if keyboard.is_pressed(key):
            ptz_move(key)

    def stopped():
        if not keyboard.is_pressed("Up") and not keyboard.is_pressed("Down") and not keyboard.is_pressed("Left") and not keyboard.is_pressed("Right"):
            ptz_stop()
    
    print("Listening for keyboard inputs. Press ESC to exit.")
    while not keyboard.is_pressed("esc"):
        controller("Up")
        controller("Down")
        controller("Left")
        controller("Right")
        stopped()

