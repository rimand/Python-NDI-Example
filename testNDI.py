import cv2 as cv
import numpy as np
import sys
import imutils

sys.path.insert(0, './pyNDI/ndi')

#pyNDI Import
import finder
import receiver
import lib

find = finder.create_ndi_finder()
NDIsources = find.get_sources()
recieveSource = NDIsources[0]
reciever = receiver.create_receiver(recieveSource)

def empty(a):
    pass

cv.namedWindow("Parameters")
cv.resizeWindow("Parameters",640,240)
cv.createTrackbar("Threshold1","Parameters",120,255,empty)
cv.createTrackbar("Threshold2","Parameters",50,255,empty)
cv.createTrackbar("SizeArea","Parameters",5000,30000,empty)

def getContours(img,imgContour):
    img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    contours,hierarchy = cv.findContours(img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    # cv.drawContours(imgContour,contours,-1,(255,0,255),7)
    
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > SizeArea:
            cv.drawContours(imgContour,contours,-1,(255,0,255),7)
            peri = cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,0.02 * peri,True)
            print(len(approx))
            x,y,w,h = cv.boundingRect(approx)
            cv.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),5)
            cv.putText(imgContour,"Points:" + str(len(approx)),(x+w+20,y+20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
            cv.putText(imgContour,"Area:" + str(int(area)),(x+w+20,y+45),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)

while True:
    img = reciever.read()
    img = cv.cvtColor(img, cv.COLOR_RGBA2BGR)
    imgContour = img.copy()
    
    imgBlur = cv.GaussianBlur(img,(7,7),1)
    
    imgGray = cv.cvtColor(imgBlur,cv.COLOR_BGR2GRAY)
    imgGray = cv.cvtColor(imgGray, cv.COLOR_GRAY2BGR)
    
    threshold1 = cv.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv.getTrackbarPos("Threshold2","Parameters")
    SizeArea = cv.getTrackbarPos("SizeArea","Parameters")
    
    imgCanny = cv.Canny(imgGray,threshold1,threshold2)
    imgCanny = cv.cvtColor(imgCanny, cv.COLOR_GRAY2BGR)
    
    kernel = np.ones((5,5))
    imgDil = cv.dilate(imgCanny,kernel,iterations=1)
    
    getContours(imgDil,imgContour)
    
    
    frameh = np.hstack((img,imgGray, imgCanny))
    frameh = imutils.resize(frameh, width=1000)
    framev = np.hstack((imgDil,imgContour, imgContour))
    framev = imutils.resize(framev, width=1000)
    
    frame = np.vstack((frameh,framev))
    frame = imutils.resize(frame, width=1000)
    
    cv.imshow("window",frame)
    if cv.waitKey(1) & 0xff == ord('q'):
        break
    
print(imgBlur.shape)
print(imgCanny.shape)

cv.destroyAllWindows()