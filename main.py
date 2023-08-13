import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector
cap = cv2.VideoCapture("Resources/Videos/1.mp4")
detector = PoseDetector()
counterRight = 0
+3
counterLeft = 0
selectionSpeed = 10

shirtFolderPath = "Resources/T shirt Folder"
listShirts = os.listdir(shirtFolderPath)
#print(listShirts)
fixedRatio = 262/190 # widthOfShirt / widthOfPoint11to12
shirtRatioWidthHeight = 581/480
imageNumber = 0
imageButtonRight = cv2.imread("Resources/button.png",cv2.IMREAD_UNCHANGED)
imageButtonLeft = cv2.flip(imageButtonRight, 1)
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    # img = cv2.flip(img, 1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw = False)
    if lmList:
        # center = bboxInfo["center"]
        # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
        lml11 = lmList[11][1:3]
        lml12 = lmList[12][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        imgShirt = cv2.resize(imgShirt, (0, 0), None, 0.5, 0.5)

        widthOfShirt = int((lml11[0]-lml12[0])*fixedRatio)
        print(widthOfShirt)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shirtRatioWidthHeight)))
        currentscale = (lml11[0]-lml12[0])/190
        offset = int(44*currentscale), int(48*currentscale)
        try:
            img = cvzone.overlayPNG(img, imgShirt, (lml12[0]-offset[0], lml12[1]-offset[1]))
        except:
            pass
        # img = cvzone.overlayPNG(img, imgShirt, lml12)
        img = cvzone.overlayPNG(img, imageButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imageButtonLeft, (72, 293))

        if lmList[16][1]< 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66,66), 0, 0, counterRight*selectionSpeed, (0, 255, 0), 20)
            if counterRight* selectionSpeed > 360:
                counterRight=0
                if imageNumber< len(listShirts)-1:
                    imageNumber+=1
        elif lmList[15][1] > 900:
            counterLeft+=1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, counterLeft*selectionSpeed, (0, 255, 0), 20)
            if counterLeft* selectionSpeed > 360:
                counterLeft=0
                if imageNumber > 0:
                    imageNumber-=1
        else:
            counterRight=0
            counterLeft=0
    cv2.imshow("Image", img)
    cv2.waitKey(1)


