import cv2
import numpy as np
import time
import pyautogui       

cap = cv2.VideoCapture(0)
time.sleep(5)
up = False
down = False
center = True


while(1):
    ret, img = cap.read()
    height, width, _ = img.shape
    blur =  cv2.blur(img,(3,3))
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    lower = np.array([0,48,80])
    upper = np.array([20,255,255])
    mask = cv2.inRange(hsv,lower, upper)

    kernel_square = np.ones((11,11),np.uint8)
    kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        
    #Perform morphological transformations to filter out the background noise
    #Dilation increase skin color area
    #Erosion increase skin color area
    dilation = cv2.dilate(mask,kernel_ellipse,iterations = 1)
    erosion = cv2.erode(dilation,kernel_square,iterations = 1)    
    dilation2 = cv2.dilate(erosion,kernel_ellipse,iterations = 1)    
    filtered = cv2.medianBlur(dilation2,5)
    kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
    dilation2 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
    kernel_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilation3 = cv2.dilate(filtered,kernel_ellipse,iterations = 1)
    median = cv2.medianBlur(dilation2,5)
    ret,thresh = cv2.threshold(median,127,255,0)
    _,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (122,122,0), 3)
    new = contours
    max_area=100
    ci=0
    if(len(contours) > 0):
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i     
                #Largest area contour
        cnts = new[ci]
        moments = cv2.moments(cnts)
        
    #Central mass of first order moments
        if moments['m00']!=0:
            cx = int(moments['m10']/moments['m00']) # cx = M10/M00
            cy = int(moments['m01']/moments['m00']) # cy = M01/M00
        centerMass=(cx,cy)
        print(cx,cy)
        cv2.circle(img,centerMass,7,[100,0,255],2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Center',tuple(centerMass),font,2,(0,0,0),2)
        if(cy < (height/2)-70 and center == True ):
            center = False
            up = True
            print('up')
            pyautogui.press("up")
            
        if( cy > (height/2)-70 and cy < (height/2)+70 and (up == True or down == True)):
            center = True
            up = False
        if(cy > (height/2)+70 and center == True):
            center = False
            down = True
            print('up')
            pyautogui.press("down")
    cv2.line(img,(0,(height//2)-70),(width,(height//2)-70),(255,255,255),5)
    cv2.line(img,(0,(height//2)+70),(width,(height//2)+70),(255,255,255),5)
    cv2.imshow('frame',img)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()