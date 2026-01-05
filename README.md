# AmCrest Face Tracking


## Overview
This project implements real-time face detection and PTZ camera control using an Amcrest IP camera, OpenCV, and Python. The system actively tracks a detected face and dynamically adjusts camera pan/tilt to keep the subject centered in frame.


## Features
- Low-latency RTSP video ingestion
- Real-time face detection
- Closed-loop PTZ control
- Sub-200ms tracking response under load
- Network-aware control rate limiting


## Project Architecture
```
RTSP Substream (UDP)
        ↓
OpenCV Frame Grabber (grab/retrieve)
        ↓
Face Detection (Haar Cascade)
        ↓
Offset Calculation (from image center)
        ↓
State-Based PTZ Controller
        ↓
HTTP CGI Commands (Digest Auth)
```


## Camera Hardware
| Specification | Details | Reasoning |
| ----------- | ----------- | ----------- |
| Model | Amcrest IP4M-1041 | N/A |
| Category | Indoor PTZ IP Camera | N/A |
| Control Interface | HTTP CGI (/cgi-bin/ptz.cgi) | N/A |
| Authentication | HTTP Digest Authentication | N/A |
| Stream | Substream (1) | Lower quality -> faster processing |
| Video Encoding | MJPEG | Faster encoding than default |
| Substream Frame Rate | 15 FPS | Lower FPS -> faster transport |
| Substream Resolution | 640*480 (VGA) | Lower resolution -> faster transport |
| PTZ Speed | 1 | Slower speed, less overshooting |


## Installation
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows


pip install -r requirements.txt
```


## Configuration


Create a `credentials.py` file in the project root:


```python
IP = "192.168.1.100"
USERNAME = "admin"
PASSWORD = "password"
```


## Previous Latency Issue
### Problem/Debugging:
- The position of the camera that is being processed by the Haar cascade lags behind the true position of the camera. This prevents the camera from making accurate adjustments to the camera in real time, often overshooting then overcorrecting. This latency was often over a full second which is unusable.
- My first thought was that the stream was sending the processing script outdated data but testing that in isolation turned out not to be the issue.
- The second idea was that the Haar cascade that I was using was just not processing the stream quick enough. However, when displaying the live results post-recognition the latency there was negligible
- Once the PTZ code was reimplemented, the large spike in latency returned
- This implies that the issue comes down to the way that the control requests were being sent. Since each movement command requires a HTTP get request, redundant requests can increase the delay between the processing and the movement.


### Solution:
- Introducing states eliminates redundant requests by storing the current direction the camera is traveling and calculating the next direction the camera needs to travel in based on the deadzone specification.
- This is done by skipping over any movement logic if the next direction and the current direction are the same, effectively telling the camera to carry on.
- Another factor from this methodology is that the camera does not need to be repeatedly stopped when the camera needs to change directions. The logic ensures that the camera is only stopped once it is in the deadzone at which point it waits for any new commands to be given. This further reduces the amount of requests being sent and any degradation of the motor from the repetitive starting and stopping.


### Other Adjustments:
- **Sessions:** To further cut back on the time for each get request, we create a session with our username and password combination which eliminates the need to authenticate on every request. HTTP digest authentication is a more secure method of authenticating with the interface it takes longer than basic authentication. Not needing to have this delay on every movement request reduces the delay considerably.
- **Rate Limiting:** Since our program has the capability to run faster than the control interface can handle, adding a rate limit into our movement controls guarantees there are no issues there. The limit is set at a 5 Hz max, which could be fine tuned more in the future.


## Future Improvements
- [ ] Replace Haar cascade with OpenCV DNN or YuNet
- [ ] PID-based PTZ smoothing
- [ ] Face motion prediction (lead compensation)
- [ ] Reduce false positives to prevent unnecessary jittering
- [ ] Default position on startup/no targets after set period of time