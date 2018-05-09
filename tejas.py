import cv2
import io
import picamera
import numpy as np
import picamera.array
import math
from actions import *
import time
def dummy(x):
     pass
cv2.namedWindow("alltime") # create a window to be displayed
cv2.createTrackbar("Mouse Sensitivity", "alltime", 1, 200, dummy)
cv2.setTrackbarPos("Mouse Sensitivity", "alltime", 100)

with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as frame:
                camera.brightness = 60
                camera.resolution = (432, 320)
                while True:
                        camera.capture(frame, 'bgr', use_video_port=True)

                        """buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

                        image = cv2.imdecode(buff, 1)"""
                        image = frame.array
                        act = action(image.shape)
                        cv2.imshow("img",frame.array)
                        ''''#create a box where image recognition takes place
                        img_x, img_y, _ = image.shape
                        cv2.rectangle(image, (img_x,img_y), (00,00), (0,255,0), 0)
                        crop_img = image'''
                        #cv2.imshow("crop",crop_img)

                        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                        ret, thresh1 = cv2.threshold(gray, 177, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
                        cnts = cv2.findContours(thresh1, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                        #cv2.imshow("thresh",thresh)
                        #cv2.imshow("gray",gray)
                        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                        # to find maximum area contour
                        max_area = -1
                        for i in range(len(contours)):
                             cnt=contours[i]
                             area = cv2.contourArea(cnt)
                             if(area>max_area):
                                  max_area=area
                                  c=i
                        cnt=contours[c]
                        #drawing rectangle on image
                        x,y,w,h = cv2.boundingRect(cnt)
                        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),0)
                        hull = cv2.convexHull(cnt)
                        drawing = np.zeros(image.shape,np.uint8)
                        cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
                        cv2.drawContours(drawing,[hull],0,(0,0,255),0)

                        #find out hull and defects
                        #hull stored in hull and defects stored in defects
                        hull = cv2.convexHull(cnt,returnPoints = False)
                        defects = cv2.convexityDefects(cnt,hull)
                        count_defects = 0
                        cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
                        for i in range(defects.shape[0]):
                             s,e,f,d = defects[i,0]
                             start = tuple(cnt[s][0])
                             end = tuple(cnt[e][0])
                             far = tuple(cnt[f][0])
                             a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                             b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                             c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                             angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                             if angle <= 90:
                                  count_defects += 1
                                  cv2.circle(image,far,1,[0,0,255],-1)
                             cv2.line(image,start,end,[0,255,0],2)
                        act.update_sensitivity(cv2.getTrackbarPos("Mouse Sensitivity", "alltime"))
                        if count_defects == 1:
                             act.one(far)
                        elif count_defects == 2:
                             act.two()
                        elif count_defects == 3:
                             act.three()
                        else:
                             act.zero()
                        all_img = np.hstack((drawing, image))
                        frame.seek(0)
                        frame.truncate()
                        key = cv2.waitKey(1) & 0xFF
                        
                        # if the 'q' key is pressed, stop the loop
                        if key == ord("q"):
                                break
cv2.destroyAllWindows()
