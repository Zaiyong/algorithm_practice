import numpy as np
import cv2
import Person
import time

cnt_up   = 0
cnt_down = 0

# read the video
cap = cv2.VideoCapture('peopleCounter.mov')

# weight, height
w = cap.get(3)
h = cap.get(4)

frameArea = h*w
areaTH = frameArea/250
print ('Area Threshold', areaTH)

#genearete the coordinates of the 4 lines
line_up = int(2*(h/5))
line_down   = int(3*(h/5))

print ("Red line y:",str(line_down))
print ("Blue line y:", str(line_up))
line_down_color = (255,0,0)
line_up_color = (0,0,255)
pt1 =  [0, line_down];
pt2 =  [w, line_down];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up];
pt4 =  [w, line_up];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))


#background
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

#init the parameters
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

#Variables
font = cv2.FONT_HERSHEY_SIMPLEX # set the font value
persons = []
pid = 1

while(cap.isOpened()):
##for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Lee una imagen de la fuente de video
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    #Binariazcion para eliminar sombras (color gris)
    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        #Opening (erode->dilate) para quitar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regiones blancas.
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print ('UP:',cnt_up)
        print ('DOWN:',cnt_down)
        break

    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cnt)
        if area > areaTH:
            M = cv2.moments(cnt)
            # Centroid of the moment: cx,cy
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            # genearete the coordinates of top-left vertex and the size of the rectangle
            x,y,w,h = cv2.boundingRect(cnt)

            new = True
            for i in persons:
                if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                    # this is not a new person
                    new = False
                    i.updateCoords(cx,cy)
                    if i.going_UP(line_up) == True:
                        cnt_up += 1;
                        i.setDone()
                        print ("ID:",i.getId(),'crossed going up at',time.strftime("%c"))
                    elif i.going_DOWN(line_down) == True:
                        cnt_down += 1;
                        i.setDone()
                        print ("ID:",i.getId(),'crossed going down at',time.strftime("%c"))
                    break

            if new == True:
                p = Person.Person(pid,cx,cy)
                persons.append(p)
                pid += 1

            # plot the red dot
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)

            # plot the green rectangle around person
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

    for i in persons:
        cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)

    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    frame = cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    frame = cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
    cv2.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv2.LINE_AA)

    cv2.imshow('Frame',frame)

    #preisonar ESC para salir
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
#END while(cap.isOpened())

#################
#   LIMPIEZA    #
#################
cap.release()
cv2.destroyAllWindows()
