#!/bin/env python
import cv2
import pyautogui

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
CAMERA_INDEX = 0
DISTURBANCE_TOLERANCE = 50   # High for less sensitivity towards Zoom IN/OUT
DISTURBANCE_TOLERANCE_ZOOM = 100 # More for less sensitivity towards ZOOM IN/OUT. More the difference, more will be stable time.

key_to_function = {
    0:   (lambda x: moveRight(x)),
    1:  (lambda x: moveLeft(x)),
    2:   (lambda x: moveUp(x)),
    3:     (lambda x: moveDown(x)),
}


def detect_faces(image):
	faces = []
	detected = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

	if detected!=[]:
		for (x,y,w,h) in detected: #for (x,y,w,h),n in detected:
			faces.append((x,y,w,h))
	return faces

def get_motion(face):
	#yaw is x-axis - horizontal axis
	#pitch is y-axis - depth axis
	#roll is z-axis - vertical axis

	#[0][0] - x, [0][1] - y, [0][2] - w, [0][3] - h

	#w,h are approx constant for U,D,L,R events
	#checking if w,h in range of origin(w,h)+/-DISTURBANCE_TOLERANCE
	if (face[0][2]>(origin[0][2]-DISTURBANCE_TOLERANCE)) and (face[0][2]<(origin[0][2]+DISTURBANCE_TOLERANCE)) and (face[0][3]>(origin[0][3]-DISTURBANCE_TOLERANCE)) and (face[0][3]<(origin[0][3]+DISTURBANCE_TOLERANCE)):
		#check x while y is same
		if face[0][1]>(origin[0][1]-DISTURBANCE_TOLERANCE) and face[0][1]<(origin[0][1]+DISTURBANCE_TOLERANCE):
			if face[0][0]>(origin[0][0]-DISTURBANCE_TOLERANCE) and face[0][0]<(origin[0][0]+DISTURBANCE_TOLERANCE):
				#user is in origin location
				print 'origin'
				return 25,0 #no motion
			else:
				if (face[0][0]-origin[0][0])>0:
					#LEFT motion event - S button
					print 'LEFT'
					return 1, face[0][0]-origin[0][0]
				elif (face[0][0]-origin[0][0])<0:
					#RIGHT motion event - A button
					print 'RIGHT'
					return 0, origin[0][0]-face[0][0]
		else:
			#check y while x is same
			if (face[0][1]-origin[0][1])>0:
				#DOWN motion event - Q button
				print 'DOWN'
				return 2, face[0][1]-origin[0][1]
			elif (face[0][1]-origin[0][1])<0:
				#UP motion event - W button
				print 'UP'
				return 3, origin[0][1]-face[0][1]
	else:
		pass	
#		#possible events: Zoom in, Zoom out
#		if (face[0][2]-origin[0][2])>DISTURBANCE_TOLERANCE_ZOOM:
#			#ZOOM IN motion event - = button
#			print 'ZOOM IN'
#			return 4
#	 	elif (face[0][2]-origin[0][2])<DISTURBANCE_TOLERANCE_ZOOM:
#			#ZOOM OUT motion event - -button
#			print 'ZOOM OUT'
#			return 5


def run():
    """ Create a pygame screen until it is closed. """
    running = True
    while running:
     	retval, image = capture.read()

       	global i, ctr, origin, faces

       	# Only run the Detection algorithm every 3 frames to improve performance
      	if i%3==0:
       		faces = detect_faces(image)
       		print 'current coords',faces
       		ctr += 1

       	for (x,y,w,h) in faces:
       		cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 255)

       	if ctr==20:
       		#approx 3 secs of config time
       		origin = faces
       		print 'origin is ',origin

       	if origin!=[] and faces!=[]:
#      		direction, val = get_motion(faces)
#		print 'direction vector',dir
#      		if direction in key_to_function:
#      			key_to_function[direction](val)
		move(faces)	
       	cv2.imshow("Video",image)
       	i += 1
       	c = cv2.waitKey(5)

       	if c==27:
       		break
def move(face):
	pyautogui.moveTo((face[0][0]+face[0][2]/2)*1366/600, (face[0][1]+face[0][3]/2)*768/600)        	
def moveRight(value):
	pyautogui.moveRel(value, None)
def moveLeft(value):
	pyautogui.moveRel(-value, None)
def moveUp(value):
	pyautogui.moveRel(None, -value)
def moveDown(value):
	pyautogui.moveRel(None, value)



if __name__ == '__main__':

    cv2.namedWindow("Video",600)

    capture = cv2.VideoCapture(CAMERA_INDEX)
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    faces = [] #var that stores face rect coords
    origin = [] #var that will store the origin coords

    i = 0
    c = -1
    ctr = 0 #for counting the no. of detections
    run() 
