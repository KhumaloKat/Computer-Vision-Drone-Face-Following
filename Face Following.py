from djitellopy import tello
import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.PoseModule import PoseDetector
import time

detector = FaceDetector(minDetectionCon=0.8)
detectorBody = PoseDetector()

cap = cv2.VideoCapture(0)
h1, w1, _ = 480, 640, True

following = False
gesture = ''
colourG = (0, 0, 255)
snapTime = 0

xVal = 0
yVal = 0
zVal = 0

xPID = cvzone.PID([0.22, 0, 0.1], w1//2)
yPID = cvzone.PID([0.27, 0, 0.1], h1//2, axis=1)
zPID = cvzone.PID([0.005, 0, 0.003], 10000, limit=[-20, 15])

myPlotx = cvzone.LivePlot(yLimit=[-100, 100], char='x')
myPloty = cvzone.LivePlot(yLimit=[-100, 100], char='Y')
myPlotz = cvzone.LivePlot(yLimit=[-100, 100], char='Z')

# me = tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamoff()
# me.streamon()
# me.takeoff()
# me.move_up(80)

while True:

    _, img = cap.read()
    #img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    img, bboxs = detector.findFaces(img, draw=True)

    img = detectorBody.findPose(img, draw=False)
    lmList, bboxInfo = detectorBody.findPosition(img, draw=False)

    if bboxs:
        cx, cy = bboxs[0]['center']
        x, y, w, h = bboxs[0]['bbox']
        area = w * h

        xVal = int(xPID.update(cx))
        yVal = int(yPID.update(cy))
        zVal = int(zPID.update(area))
        #print(zVal)

        imgPlotx = myPlotx.update(xVal)
        imgPloty = myPloty.update(yVal)
        imgPlotz = myPlotz.update(zVal)

        angArmL = detectorBody.findAngle(img, 13, 11, 23, draw=False)
        angArmR = detectorBody.findAngle(img, 14, 12, 24, draw=False)
        CrossL, img, _ = detectorBody.findDistance(15, 12, img, draw=False)
        CrossR, img, _ = detectorBody.findDistance(16, 11, img, draw=False)
        CrossP, img, _ = detectorBody.findDistance(16, 8, img, draw=False)
        print(CrossR)

        if detectorBody.angleCheck(angArmL, 98) and detectorBody.angleCheck(angArmR, 278):
            gesture = 'Tracking mode: OFF'
            following = False
            colourG = (0, 0, 255)

        elif CrossL < 70 and CrossR < 70:
            gesture = 'Tracking mode: ON'
            following = True
            colourG = (0, 255, 0)

        if CrossP < 70:
            snapTime = time.time()
            cv2.putText(img, gesture, (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        if snapTime > 0:
            totaltime = time.time()-snapTime

            if totaltime < 1.9:
                cv2.putText(img, "Ready", (120, 260), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

            if totaltime > 2:
                snapTime = 0
                cv2.imwrite(f'Images/{time.time()}.jpg', img)
                cv2.putText(img, "Saved", (120, 260), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        img = xPID.draw(img, [cx, cy])
        img = yPID.draw(img, [cx, cy])
        imageStacked = cvzone.stackImages([img, imgPlotx, imgPloty, imgPlotz], 2, 0.5)
        cv2.putText(img, gesture, (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, colourG, 3)
        #cv2.putText(imageStacked, str(area), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    else:
        imageStacked = cvzone.stackImages([img], 1, 0.75)

    #if following:
    #    me.send_rc_control(0, -zVal, 0, xVal)
    #else:
    #    me.send_rc_control(0, 0, 0, 0)

    cv2.imshow("ImageStacked", imageStacked)

    if cv2.waitKey(5) & 0xFF == ord('q'):
    #    me.land()
        break
cv2.destroyWindow()
