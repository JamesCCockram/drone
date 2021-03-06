import logging
import threading
import time
import numpy as np
import argparse
import cv2
import imutils
import random
import commands as fly
import math
from multiprocessing.pool import ThreadPool
from multiprocessing import Process

pool = ThreadPool(processes=2)

# create camera window
def preview(camera):
    exitProgram = False
    (grabbed, frame) = camera.read()
    if not grabbed:
            return
    cv2.imshow("Preview", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        exitProgram = True
    return exitProgram

# fly to the target
def flyDrone(found, cX, cY):
    dist = calculateDistance(cX, cY)
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if dist[2] != 0 and found == False:
        fly.up()    
    elif dist[2] != 0 and found == True:
        #first quadrant   
        if cX < width/2 and cY < height/2:
            fly.right()
            fly.down()
        #second quadrant
        elif cX > width/2 and cY < height/2:
            fly.left()
            fly.down()
        #third quadrant
        elif cX < width/2 and cY > height/2:
            fly.right()
            fly.up()
        #fourth quadrant
        elif cX > width/2 and cY > height/2:
            fly.left()
            fly.up()

        elif cX <= width/2 and cY == height/2:
            fly.right()

        elif cX >= width/2 and cY == height/2:
            fly.left()

        elif cX == width/2 and cY <= height/2:
            fly.down()

        elif cX == width/2 and cY >= height/2:
            fly.up()
    else:
        print("Test")

# locate the target image
def detectImage(camera, found):
    (cX, cY) = (0,0)
    # grab the current frame and initialize the status text
    (grabbed, frame) = camera.read()
    found = False
    # check to see if we have reached the end of the video
    if not grabbed:
        return
    # convert the frame to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        # ensure that the approximated contour is "roughly" rectangular
        if len(approx) >= 4 and len(approx) <= 6:
            # compute the bounding box of the approximated contour and use the bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)
            # compute the solidity of the original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)
            # compute whether or not the width and height, solidity, and aspect ratio of the contour falls within appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2
            # ensure that the contour passes all our tests
            if keepDims and keepSolidity and keepAspectRatio:
                # draw an outline around the target and update the status text
                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                found = True
                # compute the center of the contour region and draw the crosshairs
                M = cv2.moments(approx)
                # center of object
                (cX, cY) = (int(M["m10"] // M["m00"]), int(M["m01"] // M["m00"]))
    return (found, cX, cY)

# calculate the coordinates of the target
def calculateDistance(cX, cY):
    # get width and height of camera
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # find center of camera
    width / 2, height / 2
    dX = cX - width / 2
    dY = cY - height / 2
    # find distance
    dist = math.sqrt((dX * dX) + (dY * dY))
    return (dX, dY, dist)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    found = False
    rv = False
    exitProgram = False
    camera = cv2.VideoCapture('tcp://192.168.1.1:5555')
    fly.takeoff()
    while exitProgram == False:
        print("Flying...")
        async_detect = pool.apply_async(detectImage,(camera,found))
        rv = async_detect.get()
        print("Found:", rv)
        dist = calculateDistance(rv[1], rv[2])
        async_fly = pool.apply_async(flyDrone,(rv[0], rv[1], rv[2]))
        found = async_fly.get()
        exitProgram = preview(camera)
    fly.land()    
    print("Stopped...")