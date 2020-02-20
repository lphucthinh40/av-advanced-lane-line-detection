# import the necessary packages
import argparse
import cv2
import numpy as np
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
count = 0
ref_pts = np.zeros((4, 2), np.int32)
out_pts = np.zeros((4, 2), np.int32)
pressed = False

def click(event, x, y, flags, param):
	global ref_pts, out_pts, count, pressed, image, clone
	h, w, _ = image.shape
	if event == cv2.EVENT_LBUTTONDOWN:
		pressed = True
	elif (event == cv2.EVENT_LBUTTONUP) and (pressed == True):
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		pressed = False
		if (count < 4):
			image = cv2.circle(image, (x,y), 4, (0, 0, 255), -1) 
			image = cv2.line(image, (0, y), (w, y), (0, 0, 255), 1) 
			ref_pts[count] = [x, y]
			count += 1
			if count == 4:
				cv2.polylines(image, np.int32([ref_pts]), True,(0, 0, 255))
				print(ref_pts)
		elif (count < 8):
			image = cv2.circle(image, (x,y), 4, (0, 255, 0), -1) 
			image = cv2.line(image, (0, y), (w, y), (0, 255, 0), 1) 
			image = cv2.line(image, (x, 0), (x, h), (0, 255, 0), 1) 
			out_pts[count-4] = [x, y]
			count += 1
			if count == 8:
				cv2.polylines(image, np.int32([out_pts]), True,(0, 255, 0))
				print(out_pts)
				M = cv2.getPerspectiveTransform(np.float32(ref_pts), np.float32(out_pts))
				warped = cv2.warpPerspective(clone, M, image.shape[1::-1], flags=cv2.INTER_LINEAR)
				cv2.imshow("warp", warped)

		# draw a rectangle around the region of interest
		cv2.imshow("image", image)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click)
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
		count = 0
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

# close all open windows
cv2.destroyAllWindows()