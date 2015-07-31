import cv2
import subprocess
import ghmm
import models
import numpy
import math
 
 
def current_image(cam):
    img = cam.read()[1]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Extract by color and make binary image (=black/white)
    img = cv2.inRange(img, (70, 50, 50), (130, 200, 200))
 
    # erode and dilate to reduce noise
    img = cv2.erode(img, numpy.array([[1] * ed_size] * ed_size), iterations=2)
    img = cv2.dilate(img, numpy.array([[1] * ed_size] * ed_size), iterations=2)
 
    return img
 
def pointer_pos(img):
    moments = cv2.moments(img)
    area = moments['m00']
 
    # Check if found object is large enough to be the target
    # otherwise probably some noise
    if area > 100000:
        x = moments['m10'] / area
        y = moments['m01'] / area
 
        return x, y
 
    return (None, None)
 
def movement_direction(x_delta, y_delta, threshold = 10):
    if abs(x_delta) > threshhold or abs(y_delta) > threshhold:
        degree = math.atan2(y_delta, x_delta)
 
        if -0.875 * math.pi <= degree < -0.625 * math.pi:
            direction = models.UP_RIGHT
        elif -0.625 * math.pi <= degree < -0.375 * math.pi:
            direction = models.UP
        elif -0.375 * math.pi <= degree < -0.125 * math.pi:
            direction = models.UP_LEFT
        elif -0.125 * math.pi <= degree < 0.125 * math.pi:
            direction = models.LEFT
        elif 0.125 * math.pi <= degree < 0.375 * math.pi:
            direction = models.DOWN_LEFT
        elif 0.375 * math.pi <= degree < 0.625 * math.pi:
            direction = models.DOWN
        elif 0.625 * math.pi <= degree < 0.875 * math.pi:
            direction = models.DOWN_RIGHT
        else:
            direction = models.RIGHT
 
        return direction
    else:
        return None
 
def execute(emission_seq, models):
    considered = []
    for model, command in models:
        res = model.forward(emission_seq)
        considered.append((res[1][-1], command))
 
    max_val, command = max(considered)
    if max_val >= 0.3:
        subprocess.call(command)
 
 
ed_size = 50
 
cam = cv2.VideoCapture(0)
 
winName = "Gestures Detection"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
 
img = current_image(cam)
x1, y1 = pointer_pos(img)
 
not_changed = 0
path = []
 
while True:
    x0 = x1
    y0 = y1
 
    img = current_image(cam)
    x1, y1 = pointer_pos(img)
 
    # only if there is no None position, we may calculate movement
    # None means the object is not visible to the webcam
    if x1 is not None and x0 is not None and y1 is not None and y0 is not None:
        x_delta = x1 - x0
        y_delta = y1 - y0
 
        direction = movement_direction(x_delta, y_delta)
        if direction is not None:
            path.append(direction)
        else:
            not_changed += 1
    else:
        not_changed += 1
 
    if not_changed > 5:
        if len(path) >= 2:
            execute(ghmm.EmissionSequence(models.sigma, path), models.models)
        path = []
        not_changed = 0
 
    cv2.imshow(winName, img)
 
    key = cv2.waitKey(50)
    if key == 27:
        cv2.destroyWindow(winName)
        break