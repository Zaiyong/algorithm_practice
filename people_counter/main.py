import numpy as np
import cv2
import Person
import time

cnt_left   = 0
cnt_right = 0

# read the video
# cap = cv2.VideoCapture('peopleCounter_rotate.mov')
cap = cv2.VideoCapture(0)


# weight, height
w = cap.get(3)
h = cap.get(4)

frameArea = h*w
areaTH = frameArea/250
print ('Area Threshold', areaTH)

#genearete the coordinates of the 4 lines
line_left = int(2*(w/5))
line_right   = int(3*(w/5))

print ("Red line y:",str(line_left))

line_left_color = (255,0,0)
pt1_left =  [line_left,0];
pt2_left =  [line_left,h];
pts_left = np.array([pt1_left,pt2_left], np.int32)
pts_left = pts_left.reshape((-1,1,2))


print ("Blue line y:", str(line_right))
line_right_color = (0,0,255)
pt1_right =  [line_right,0];
pt2_right =  [line_right,h];
pts_right = np.array([pt1_right,pt2_right], np.int32)
pts_right = pts_right.reshape((-1,1,2))


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
    # frame=cv2.flip(frame, 0)
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
        print ('UP:',cnt_left)
        print ('DOWN:',cnt_right)
        break

    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        # cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
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
                    if i.goingRight(line_right) == True:
                        cnt_right += 1;
                        i.setDone()
                        print ("ID:",i.getId(),'crossed going left at',time.strftime("%c"))
                    elif i.goingLeft(line_left) == True:
                        cnt_left += 1;
                        i.setDone()
                        print ("ID:",i.getId(),'crossed going right at',time.strftime("%c"))
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

    str_left = 'LEFT: '+ str(cnt_left)
    str_right = 'RIGHT: '+ str(cnt_right)
    frame = cv2.polylines(frame,[pts_left],False,line_left_color,thickness=2)
    frame = cv2.polylines(frame,[pts_right],False,line_right_color,thickness=2)
    cv2.putText(frame, str_left ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_left ,(10,40),font,0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(frame, str_right ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_right ,(10,90),font,0.5,(0,0,255),1,cv2.LINE_AA)

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
