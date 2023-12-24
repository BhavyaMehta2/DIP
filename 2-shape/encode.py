import cv2
import numpy as np
import json

def detect_dimens(gray):
    h, w= gray.shape

    return h,w

def detect_segments(gray):
    edges = cv2.Canny(gray,50,150,apertureSize=3)

    detected_segments = cv2.HoughLinesP(
                edges,
                1,
                np.pi/180,
                threshold=100,
                minLineLength=0,
                maxLineGap=20
                )

    print("Line Segments Extracted")
    
    return detected_segments

def detect_circles(gray):
    gray_blurred = cv2.blur(gray, (3, 3))

    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 135, param1 = 50,
                param2 = 30, minRadius = 1)
    
    print("Circles Extracted")
    
    return detected_circles

def encode(h ,w, segments, circles):
    if not segments is None and not circles is None:
        data = {
        "h": h,
        "w": w,
        "segments": segments.tolist(),
        "circles": circles.tolist()
        }

    else:
        if segments is None:
            data = {
            "h": h,
            "w": w,
            "segments": None,
            "circles": circles.tolist()
            }

        else:
            data = {
            "h": h,
            "w": w,
            "segments": segments.tolist(),
            "circles": None
            }

    with open("encoded.json", "w") as json_file:
        json.dump(data, json_file)
        print("Encoded")

image = cv2.imread("im1.png")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

h,w = detect_dimens(gray)
segments = detect_segments(gray)
circles = detect_circles(gray)

encode(h, w, segments, circles)