import cv2
import numpy as np
import time


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


captMedia=0
cap = cv2.VideoCapture(captMedia)
fps = 17.25

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

#detectMultiScale2 parameter
#scaleFactor 1.05 - 1.4, less=better, detect less, slower (minimum=1.05)
#minNeighbors 3 - 6, less= detect more, less accuracy
#minSize (50, 50) for faces, limit minimum size that can be detected, less=more processing time

scaleFactor = 1.05
minNeighbors= 12
minSize=	  (90, 90)

#setting interval dan delay
minInterval=4
minDelay=4

while True:
    #Detect face with Haar Cascade
    ret, img = cap.read()
    if not ret:
      #Detection documentation, write to test.txt
      detik=int(detik)
      durasi = time.time()-start
      print('Durasi proses: %.4f' %durasi, ' detik')
      print('Durasi video:', menit,' menit', detik, ' detik')
      f= open("test.txt","a+")
      f.write('\r\n')
      f.write('Durasi proses: %.4f' %durasi + ' detik'+ '\r\n')
      f.write('Durasi video: '+ str(menit)+ ' menit '+ str(detik)+ ' detik '+ '\r\n')
      f.write('scaleFactor= '+ str(scaleFactor)+ '\r\n'+ 'minNeighbors= '+ str(minNeighbors)+ '\r\n'+ 'minSize= '+ str(minSize)+'\r\n')
      f.write('interval= '+ str(minInterval)+ '\r\n'+ 'delay= '+ str(minDelay))
      f.close()
      break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces, numDetect = face_cascade.detectMultiScale2(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    numDetect=len(numDetect)
    
    #Draw Bounding boxes for faces    
    for (x,y,w,h) in faces:
       cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
       
       
    #Count video real second
    counter=counter + 1
    detik= counter/fps

    #Detection interval
    counter2 = counter2 + 1
    interval = counter2/fps

    #Delay if no face is detected
    if numDetect==0:
      counter3 = counter3 + 1
      delay = counter3/fps
      if delay >= minDelay:
        delta=0
        z0=0
    
    #If a face is detected
    if numDetect>=1:
      delay=0
      if interval>=minInterval:
        counter2=0
        counter3=0
        delta = z0-numDetect
        if z0<=numDetect:
          z2= z2 + abs(delta)
        z0=numDetect
     

    #Write how many faces detected in one minute
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
    
    if captMedia==0:
      font = cv2.FONT_HERSHEY_SIMPLEX
      #cv2.putText(img,str(numDetect),(10,160), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      
      detik=int(detik)
      cv2.putText(img,str(interval)+'s',(10,20), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Delta: '+str(abs(delta)),(10,40), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Person: '+str(numDetect),(10,60), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Total: '+str(z2),(10,80), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Delay: '+str(delay),(10,100), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Detik: '+str(detik),(10,120), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'z0: '+str(z0),(10,140), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.imshow('img',img)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
      
      
        
cap.release()
cv2.destroyAllWindows
                                     
