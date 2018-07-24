#version 0.02
#log 0.02: tambahan write/append data total muka yang terdeteksi per menit dalam notepad

import cv2
import numpy as np


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


cap = cv2.VideoCapture(0)
z = 0
z0 = 0
z1 = 0
z2 = 0
milsec = 0
delay = 0
delta = 0
menit = 0
counter = 0
f= open("test.txt","a+")
f.write('\r\n')
f.close()
while True:
    #deteksi muka dengan cascade
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    
    #gambar kotak dan counter untuk muka    
    for (x,y,w,h) in faces:
       cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
       #z = z + 1
       roi_gray = gray[y:y+h, x:x+w]
       roi_color = img[y:y+h, x:x+w]
       eyes = eye_cascade.detectMultiScale(roi_gray)
       for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew,ey+eh), (0,255,0), 2)
            z = z + 1

    #interval deteksi
    milsec = milsec + 100

    #delay bila tidak ada muka yang terdeteksi
    if z==0:
      delay = delay + 100
      if delay >= 2000:
        delta=0
        z0=0
    
    #bila muka terdeteksi
    elif z>=1:
      if milsec>=2000:
        delay=0
        milsec=0
        delta = z0-z
        if z0<=z:
          z2= z2 + abs(delta)
        z0=z
     
    #menghitung detik
    counter=counter + 100
    detik= counter/1000

    #print total orang per __ (1 sekon = 1000 ms)
    if counter >=5000:
      menit = menit + 1
      space=120+(menit*20)
      print('Menit '+str(menit)+': '+str(z2)+' orang')
      f= open("test.txt","a+")
      f.write('Menit '+str(menit)+': '+str(z2)+' orang\r\n')
      f.close()
      z2=0
      z0=0
      counter=0
      
   	font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,str(milsec)+'ms',(10,20), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Delta: '+str(abs(delta)),(10,40), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Person: '+str(z),(10,60), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Total: '+str(z2),(10,80), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Delay: '+str(delay)+'ms',(10,100), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Detik: '+str(detik),(10,120), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'z0: '+str(z0),(10,140), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    
    #reset counter pendeteksi muka 
    z=0

    #menunjukan window video 
    cv2.imshow('img',img)
    #waitkey() isi lama frame ditampilkan di window misal:33 = menunggu 33ms sebelum berganti frame
    #gunakan 33 dengan asumsi video berjalan 30fps (33=1000ms/30fps)
    cv2.waitKey(33)
 
cap.release()
cv2.destroyAllWindows
                                     
