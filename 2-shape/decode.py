import cv2
import numpy as np
import json

def decode():
    with open("encoded.json", "r") as json_file:
        data = json.load(json_file)

    h = data["h"]
    w = data["w"]
    segments_list = data["segments"]
    circles_list = data["circles"]

    result = np.ones((h, w, 3), np.uint8) * 0xFF

    if not segments_list is None:
        segments = np.array(segments_list)

        for points in segments:
            x1,y1,x2,y2=points[0]
            cv2.line(result,(x1,y1),(x2,y2),(0,255,0),2)

    if not circles_list is None:
        circles = np.array(circles_list)

        if circles is not None:
            circles = np.uint16(np.around(circles))
        
            for pt in circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
        
                cv2.circle(result, (a, b), r, (0, 255, 0), 2)
        
    cv2.imwrite('decoded.png',result)

    print("Decoded")

decode()