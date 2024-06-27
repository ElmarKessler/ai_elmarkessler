import cv2
import numpy as np

document.getElementById("ai").addEventListener("change", toggleAi)
document.getElementById("fps").addEventListener("input", changeFps)

video = cv2.VideoCapture(0)
c1 = cv2.VideoWriter_fourcc(*'XVID')
ctx1 = cv2.VideoWriter('output.avi', c1, 16.0, (640,480))
cameraAvailable = False
aiEnabled = False
fps = 16

# Setting up the constraint
facingMode = "environment"
constraints = {
    "audio": False,
    "video": {
        "facingMode": facingMode
    }
}

# Stream it to video element
def camera():
    global cameraAvailable
    if not cameraAvailable:
        print("camera")
        try:
            video.open(0)
            cameraAvailable = True
        except:
            cameraAvailable = False
            if modelIsLoaded:
                if err.name == "NotAllowedError":
                    document.getElementById("loadingText").innerText = "Waiting for camera permission"
            cv2.waitKey(1000)
            camera()

def timerCallback():
    if isReady():
        setResolution()
        ret, frame = video.read()
        ctx1.write(frame)
        if aiEnabled:
            ai()
    cv2.waitKey(int(fps))
    cv2.destroyAllWindows()
    timerCallback()

def isReady():
    if modelIsLoaded and cameraAvailable:
        document.getElementById("loadingText").style.display = "none"
        document.getElementById("ai").disabled = False
        return True
    else:
        return False

def setResolution():
    if cv2.VideoCapture.get(cv2.CAP_PROP_FRAME_WIDTH) < video.get(cv2.CAP_PROP_FRAME_WIDTH):
        c1.set(cv2.CAP_PROP_FRAME_WIDTH, video.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.9)
        factor = c1.get(cv2.CAP_PROP_FRAME_WIDTH) / video.get(cv2.CAP_PROP_FRAME_WIDTH)
        c1.set(cv2.CAP_PROP_FRAME_HEIGHT, video.get(cv2.CAP_PROP_FRAME_HEIGHT) * factor)
    elif cv2.VideoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT) < video.get(cv2.CAP_PROP_FRAME_HEIGHT):
        c1.set(cv2.CAP_PROP_FRAME_HEIGHT, video.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.5)
        factor = c1.get(cv2.CAP_PROP_FRAME_HEIGHT) / video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        c1.set(cv2.CAP_PROP_FRAME_WIDTH, video.get(cv2.CAP_PROP_FRAME_WIDTH) * factor)
    else:
        c1.set(cv2.CAP_PROP_FRAME_WIDTH, video.get(cv2.CAP_PROP_FRAME_WIDTH))
        c1.set(cv2.CAP_PROP_FRAME_HEIGHT, video.get(cv2.CAP_PROP_FRAME_HEIGHT))

def toggleAi():
    global aiEnabled
    aiEnabled = document.getElementById("ai").checked

def changeFps():
    global fps
    fps = 1000 / document.getElementById("fps").value

def ai():
    # Detect objects in the image element
    objectDetector.detect(c1, (err, results) => {
        print(results) # Will output bounding boxes of detected objects
        for index, element in enumerate(results):
            ctx1.putText(element.label + " - " + str(round(element.confidence * 100, 2)) + "%", (element.x + 10, element.y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            ctx1.rectangle(element.x, element.y, element.width, element.height, (0, 0, 255), 2)
            print(element.label)
    })

