#!/bin/env python
import os
import cv2
import pyautogui

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
CAMERA_INDEX = 0
DISTURBANCE_TOLERANCE = 20  #Sensitivity
CAMERA_FPS = 20

def detect_faces(image):
	faces = []
	detected = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

	if detected!=[]:
		for (x,y,w,h) in detected: #for (x,y,w,h),n in detected:
			faces.append((x,y,w,h))
	return faces

def get_motion(faceCenter, originCenter):
	#[0][0] - x, [0][1] - y, [0][2] - w, [0][3] - h
	horizontal_change = faceCenter[0] - originCenter[0]
	vertical_change = faceCenter[1] - originCenter[1]
	if abs(horizontal_change) < DISTURBANCE_TOLERANCE and abs(vertical_change) < DISTURBANCE_TOLERANCE:
		print 'ORIGIN'
		return 25, 0
	if abs(horizontal_change) > abs(vertical_change):
		if horizontal_change > 0:
			print 'LEFT'
			return 1, horizontal_change
		else:
			print 'RIGHT'
			return 0, -horizontal_change
	if abs(horizontal_change) < abs(vertical_change):
		if vertical_change > 0:
			print 'DOWN'
			return 2, vertical_change
		else:
			print 'UP'
			return 3, -vertical_change
	else:
#		print horizontal_change, vertical_change
		return 25, 0


def run():
    """ Create a pygame screen until it is closed. """
    running = True
    i = 0
    originCenter = None
    faceArray = [] 
    while running:
     	retval, image = capture.read()

       	# Only run the Detection algorithm every 3 frames to improve performance
      	if i%3==0:
       		faces = detect_faces(image)
		if faces:
			faceCenter = (faces[0][0]+faces[0][2]/2, faces[0][1]+faces[0][3]/2)
       		print 'current coords',faces

	if i<=10:
		faceArray.append(faceCenter)

       	for (x,y,w,h) in faces:
       		cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 255)
		cv2.cv.Rectangle(cv2.cv.fromarray(image), (faceCenter[0]-1, faceCenter[1]-1), (faceCenter[0]+1, faceCenter[1]+1), 255)
		if originCenter:
			cv2.cv.Rectangle(cv2.cv.fromarray(image), (originCenter[0]-1, originCenter[1]-1), (originCenter[0]+1, originCenter[1]+1), 0)

       	if originCenter and faceCenter and faceCenter != []:
      		direction, val = get_motion(faceCenter, originCenter)
      		if direction in key_to_function:
      			key_to_function[direction]()

       	if i==10 and faces:
       		#approx 3 secs of config time
		faceCenter_avg_y = sum([j[1] for j in faceArray])/len(faceArray)
		faceCenter_avg_x = sum([j[0] for j in faceArray])/len(faceArray)
		originCenter = [faceCenter_avg_x, faceCenter_avg_y]
		faceArray = None
      		print 'origin is ',originCenter
       	

	cv2.imshow("Video",image)
	if not faces:
		i -= 1
       	i += 1
       	c = cv2.waitKey(5)

       	if c==27:
       		break

def moveRight():
	pyautogui.press('right')
def moveLeft():
	pyautogui.press('left')
def moveUp():
	pyautogui.press('up')
def moveDown():
	pyautogui.press('down')


if __name__ == '__main__':
    key_to_function = {
        0:  moveRight,
        1:  moveLeft,
        2:  moveDown,
        3:  moveUp,
    }


    cv2.namedWindow("Video",600)

    capture = cv2.VideoCapture(CAMERA_INDEX)
    capture.set(cv2.cv.CV_CAP_PROP_FPS, 30)
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    faces = [] #var that stores face rect coords
    origin = [] #var that will store the origin coords
    #os.system("google-chrome --new-window index.html")
    run() 
