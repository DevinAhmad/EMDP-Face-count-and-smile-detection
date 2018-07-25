#version 0.05
'''
#log 0.02: tambahan write/append data total muka yang terdeteksi per menit dalam notepad
#log 0.04: revisi sistem detik/waktu yang benar
memasukan input fps sesuai videonya
break bila durasi video habis
sistem interval dan delay pengecekan muka diubah, sekarang menggunakan detik, bukan frame
#log 0.05: setting parameter detectMultiScale untuk mengatur sensitivitas dan akurasi deteksi muka
write durasi proses, durasi video, dan parameter detectMultiScale 
'''

import cv2
import numpy as np
import time


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



cap = cv2.VideoCapture('bandicam_1.mp4')
fps = 17.25
z = 0
z0 = 0
z1 = 0
z2 = 0
interval = 0
delay = 0
delta = 0
menit = 0
counter = 0
counter2=0
counter3=0
detik = 0
f= open("test.txt","a+")
f.write('\r\n')
f.close()
start=time.time()

#parameter detectMultiScale2
#scaleFactor 1.05 - 1.4, less=better, detect less, slower (minimum=1.05)
#minNeighbors 3 - 6, less= detect more, less accuracy
#minSize (50, 50) for faces, limit minimum size that can be detected
scaleFactor = 1.05
minNeighbors= 6
minSize=	  (90, 90)

while True:
    #deteksi muka dengan cascade
    ret, img = cap.read()
    if not ret:
      print('Durasi proses:', time.time()-start, ' detik')
      print('Durasi video:', menit,' menit', detik, ' detik')
      f= open("test.txt","a+")
      f.write('\r\n')
      f.write('Durasi proses: '+ str(time.time()-start)+ ' detik'+ '\r\n')
      f.write('Durasi video: '+ str(menit)+ ' menit '+ str(detik)+ ' detik '+ '\r\n')
      f.write('scaleFactor= '+ str(scaleFactor)+ '\r\n'+ 'minNeighbors= '+ str(minNeighbors)+ '\r\n'+ 'minSize= '+ str(minSize))
      f.close()
      break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces, numDetect = face_cascade.detectMultiScale2(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    #gambar kotak dan counter untuk muka    
    for (x,y,w,h) in faces:
       cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
       z = z + 1
       
    #menghitung detik asli video
    counter=counter + 1
    detik= counter/fps

    #interval deteksi
    counter2 = counter2 + 1
    interval = counter2/fps

    #delay bila tidak ada muka yang terdeteksi
    if z==0:
      counter3 = counter3 + 1
      delay = counter3/fps
      if delay >= 3:
        delta=0
        z0=0
    
    #bila muka terdeteksi
    if z>=1:
      delay=0
      if interval>=3:
        counter2=0
        counter3=0
        delta = z0-z
        if z0<=z:
          z2= z2 + abs(delta)
        z0=z
     

    '''
    counter += 1;
    if counter %1 == 0:
        detik = time.time() - start
        print ("time", detik)
    '''





    
    

    #print total orang per __ detik
    if detik >=60:
      menit = menit + 1
      space=120+(menit*20)
      print('Menit '+str(menit)+': '+str(z2)+' orang')
      f= open("test.txt","a+")
      f.write('Menit '+str(menit)+': '+str(z2)+' orang\r\n')
      f.close()
      z2=0
      z0=0
      counter=0
    
    #cv2.putText(img,str(numDetect)+'s',(10,20), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    '''
    detik=int(detik)
    cv2.putText(img,str(interval)+'s',(10,20), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Delta: '+str(abs(delta)),(10,40), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Person: '+str(z),(10,60), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Total: '+str(z2),(10,80), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Delay: '+str(delay),(10,100), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'Detik: '+str(detik),(10,120), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    cv2.putText(img,'z0: '+str(z0),(10,140), font, 0.5,(255,0,0),1,cv2.LINE_AA)
    '''

    #reset counter pendeteksi muka 
    z=0

    #menunjukan window video(25, 33, 57) 
    #cv2.imshow('img',img)
    #if cv2.waitKey(25) & 0xFF == ord('q'):
    # break
 
cap.release()
cv2.destroyAllWindows
                                     
