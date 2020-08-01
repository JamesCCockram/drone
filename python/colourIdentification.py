import numpy as np
import argparse
import cv2

#USED FOR IMAGES:
#construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", help = "path to the image")
#args = vars(ap.parse_args())
#load the image
#image = cv2.imread(args["image"])
cap = cv2.VideoCapture('../node/vid.h264')

#loop over the boundaries
while True:
    _, frame = cap.read()  
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower = np.array([20, 20, 160])
    upper = np.array([100, 100, 255])
    
    mask = cv2.inRange(hsv, lower, upper)

    imgray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if(area > 800):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),10)
    
    cv2.imshow("mask", mask)
    k = cv2.waitKey(5) & 0XFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()

#for static image, run in powershell with:
#python colourIdentification.py --image red_table.jpg
