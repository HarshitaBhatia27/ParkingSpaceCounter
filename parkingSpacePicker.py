#in this code we are going to see the spaces that are available for parking
import cv2
import pickle

# img = cv2.imread('carParkImg.png')
width , height = 107,48
posList= []
# here we will check if we have a pickle file, if yes it will be opened so that we can add or remove rectangles
try:
    with open('CarParkPositions', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []
def mouseClick(events,x,y,flags,params):
    if events== cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1= pos
            if  x1< x< x1 + width and y1 <y <y1+height:
                posList.pop(i)
    with open('CarParkPositions','wb') as f:
        pickle.dump(posList, f)

while True:

    # cv2.rectangle(img,(50,192),(157,240),(255,0,255),2) #size of 1 rectangle
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos,(pos[0] + width, pos[1]+height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image",mouseClick)
    cv2.waitKey(1)