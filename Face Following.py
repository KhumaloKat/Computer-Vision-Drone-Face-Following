from djitellopy import tello
import cv2
import cvzone
from cvzone.FaceDetectionModule import FaceDetector

detector = FaceDetector(minDetectionCon=0.8)

cap = cv2.VideoCapture(0)
h1, w1, _ = 480, 640, True

xVal = 0
yVal = 0
zVal = 0

#using the PID functions to capture all the changes that happens between the drone and us

xPID = cvzone.PID([0.22, 0, 0.1], w1//2)
yPID = cvzone.PID([0.27, 0, 0.1], h1//2, axis=1)
zPID = cvzone.PID([0.005, 0, 0.003], 12000, limit=[-20, 15])

myPlotx = cvzone.LivePlot(yLimit=[-100, 100], char='x')
myPloty = cvzone.LivePlot(yLimit=[-100, 100], char='Y')
myPlotz = cvzone.LivePlot(yLimit=[-100, 100], char='Z')

#activating the tello

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

    #face detection function
    if bboxs:
        cx, cy = bboxs[0]['center']  #box area of the face detected
        x, y, w, h = bboxs[0]['bbox']  #assigning all the values of the box
        area = w * h

        #Take all the values from the tello
        xVal = int(xPID.update(cx))
        yVal = int(yPID.update(cy))
        zVal = int(zPID.update(area))
        #Drawwing the plots of the all the axis and displaying the changes happening
        imgPlotx = myPlotx.update(xVal)
        imgPloty = myPloty.update(yVal)
        imgPlotz = myPlotz.update(zVal)
        img = xPID.draw(img, [cx, cy])
        img = yPID.draw(img, [cx, cy])
        imageStacked = cvzone.stackImages([img, imgPlotx, imgPloty, imgPlotz], 2, 0.5)
        cv2.putText(imageStacked, str(area), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    else:
        imageStacked = cvzone.stackImages([img], 1, 0.75)

    #send remote controls to the tello by using the value calculated using the PID function
    #me.send_rc_control(0, -zVal, -yVal, xVal)
    cv2.imshow("ImageStacked", imageStacked)

    #land and turn of the system is nothing happens in 5 secs or when pressing q
    if cv2.waitKey(5) & 0xFF == ord('q'):
        #me.land()
        break
cv2.destroyWindow()
