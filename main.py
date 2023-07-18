#for running the code
import cv2
import pickle
import numpy as np
import cvzone
width , height = 107,48
#video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPositions', 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgProcessed):

    spaceCounter= 0

    for pos in posList:
        x,y=pos
        imgCrop = imgProcessed[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop) #croping the images and showing them through their x and y values
        count = cv2.countNonZero(imgCrop)


        if count<900:
            color =(0,255,0)  #if space available
            thickness=5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness=2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)
    cvzone.putTextRect(img, f'Available: {spaceCounter}/{len(posList)}', (50,50), scale=3, thickness=5, offset=10, colorR=(0,200,0))

while True:

    #loop the video
    # cv2.CAP_PROP_POS_FRAMES ---> current frame in the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()

    #converting image to binary  image
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)
    checkParkingSpace(imgDilate)
    #for pos in posList:




    cv2.imshow("ParkingArea",img)
    # cv2.imshow("ImageBlur",imgBlur)
    # cv2.imshow("ImageBlur",imgThreshold)
    cv2.imshow("ImageBlur",imgMedian)

    cv2.waitKey(10)
