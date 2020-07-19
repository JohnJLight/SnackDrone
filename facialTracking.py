import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# To capture video from webcam. 
cap = cv2.VideoCapture(0)
state = 'none'

while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.line(img,(100,100),(100,480),(12,12,240),5)
    img = cv2.line(img,(540,100),(540,480),(12,12,240),5)
    img = cv2.line(img,(0,100),(640,100),(12,12,240),5)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Feed Me',(200,60), font, 2,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img,'Start',(6,300), font, 2,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img,'Land',(440,300), font, 2,(255,255,255),2,cv2.LINE_AA)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #draw rectangle around face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        xEnd = x + w
        yEnd = y + h
        if y <= 100 or yEnd <= 100:
            if state != 'feed':
                print("feed")
                state = 'feed'
        elif x <= 100 or xEnd <= 100:
            if state != 'fly':
                print("fly1")
                state = 'fly'
        elif x >= 540 or xEnd >= 540 :
            if state != 'land':
                print("land")
                state = 'land' 
        elif(x < 540 and xEnd < 540 and x > 100 and xEnd > 100 and y > 100 and yEnd > 100):
            if state != 'none' :
                state = 'none'
                # print("none")
    #display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
cap.release()