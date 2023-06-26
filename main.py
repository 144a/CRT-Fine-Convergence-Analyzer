import cv2
import pygame
import numpy as np
import sys

#sys.path.append(r"C:\Users\andyg\OneDrive\Documents\CRT_Stuff")

import EmuBKM15r


# Green Mask
green_mask_range = [(30, 100, 100), (80, 255,255)]

# Blue Mask
blue_mask_range = [(90, 100, 100), (140, 255,255)]

# Red Mask
red_mask_range_low = [(0, 100, 100), (25, 255,255)]
red_mask_range_high = [(150, 100, 100), (240, 255,255)]

def calculateComponentImages(img):
    # Convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create masks for each color component
    green_mask = cv2.inRange(hsv, green_mask_range[0], green_mask_range[1])
    blue_mask = cv2.inRange(hsv, blue_mask_range[0], blue_mask_range[1])
    red_mask = cv2.bitwise_or(cv2.inRange(hsv, red_mask_range_low[0], red_mask_range_low[1]), 
                              cv2.inRange(hsv, red_mask_range_high[0], red_mask_range_high[1]))

    return green_mask, blue_mask, red_mask

def find_center_line(mask):
    # Dialate image to get rid of errors in thresholding
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Calculate contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ypos = []
    heights = []
    centers = []

    # Sort contours by x component
    boxes = []
    for contour in contours:
        boxes.append(cv2.boundingRect(contour))
    boxes = sorted(boxes, key=lambda x: x[0])

    # Create list of center points of the contours
    for contour in boxes:
        x, y, w, h = contour

        if len(heights) == 0 or (abs(np.mean(heights) - h) < np.mean(heights) * 0.15 
                                 and abs(np.mean(ypos) - y) < np.mean(ypos) * 0.15):
            ypos.append(y)
            centers.append([x, int(y+h/2)])
            heights.append(h)

    #print(centers)
    return centers

def calibrate_convergence(image_path, connection=None):
    # Open the webcam
    #cap = cv2.VideoCapture(image_path)
    cap = cv2.VideoCapture(2)

    if connection is not None:
        #EmuBKM15r.getCommand("PhaseInc -250", connection)
        EmuBKM15r.getCommand("ChromaInc -250", connection)

    # Check To make sure Webcam is good
    if not cap.isOpened():
        print("Error: Unable to open the webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Unable to read the frame.")
            break

        half = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)

        cv2.imshow("Get In Position", half)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

    isGreenGood = False
    isRedBlueGood = False

    while not(isGreenGood) or not(isRedBlueGood):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Unable to read the frame.")
            break

        half = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)

        output_green, output_blue, output_red = calculateComponentImages(half)
        #cv2.imshow("output_blue", output_blue)
        #cv2.imshow("output_red", output_red)

        #ret = cv2.normalize((output_red + output_blue) - output_green, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)

        red_blue_output = cv2.bitwise_or(output_red, output_blue)

        ret = cv2.bitwise_or(output_green, red_blue_output)

        #cv2.imshow("output", ret)

        blue_line = find_center_line(output_red)
        red_line = find_center_line(output_blue)
        green_line = find_center_line(output_green)

        # Take the averages of each line and calculate differences
        blue_diff = np.mean(blue_line, axis=0) - np.mean(green_line, axis=0)
        red_diff = np.mean(green_line, axis=0) - np.mean(red_line, axis=0)

        green_diff = blue_diff - red_diff
        red_blue_diff = np.mean(blue_line, axis=0) - np.mean(red_line, axis=0)


        # Draw Center lines
        cv2.polylines(half, 
                [np.array(blue_line, dtype=np.int32)], 
                isClosed = False,
                color = (0,255,255),
                thickness = 3)

        cv2.polylines(half, 
                [np.array(red_line, dtype=np.int32)], 
                isClosed = False,
                color = (255,255,0),
                thickness = 3)

        cv2.polylines(half, 
                [np.array(green_line, dtype=np.int32)], 
                isClosed = False,
                color = (0,128,0),
                thickness = 3)

        cv2.putText(
                img = half,
                text = "Green Diff: " + str(int(green_diff[1] * 5))+ "                  " + "Red-Blue Diff: " + str(int(red_blue_diff[1] * 5)),
                org = (50, 50),
                fontFace = cv2.FONT_HERSHEY_DUPLEX,
                fontScale = 1.0,
                color = (125, 246, 55),
                thickness = 1)

        cv2.imshow("Analysis Output", half)

        # Send Adjustment if possible
        if connection is not None:
            print(green_diff[1]*5)
            print(str(int(green_diff[1]*0.25)))
            print(red_blue_diff[1]*5)
            print(str(int(red_blue_diff[1]*0.35)))
            if green_diff[1]*5 < -50:
                isGreenGood = False
                EmuBKM15r.getCommand("PhaseInc 15", connection)
                #EmuBKM15r.getCommand("PhaseInc "+str(int(green_diff[1]*0.25)), connection)
            elif green_diff[1]*5 > 50:
                isGreenGood = False
                EmuBKM15r.getCommand("PhaseDec 15", connection)
                #EmuBKM15r.getCommand("PhaseDec "+str(int(green_diff[1]*0.25)), connection)
            else:
                isGreenGood = True
            
            if red_blue_diff[1]*5 > 50:
                isRedBlueGood = False
                EmuBKM15r.getCommand("ChromaInc "+str(int(red_blue_diff[1]*0.35)), connection)
            elif red_blue_diff[1]*5 < -50:
                isRedBlueGood = False
                EmuBKM15r.getCommand("ChromaDec "+str(int(red_blue_diff[1]*0.35)), connection)
            else:
                isRedBlueGood = True

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(200) & 0xFF == ord("q"):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    sock = EmuBKM15r.connect_to_monitor()
    #sock = None
    calibrate_convergence(r"C:\Users\andyg\OneDrive\Documents\CRT_Stuff\Horizontal-Convergence-Test.mp4", sock)
