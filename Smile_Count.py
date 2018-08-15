#version 0.06
'''
#log 0.02: tambahan write/append data total muka yang terdeteksi per menit dalam notepad
#log 0.04: revisi sistem detik/waktu yang benar
memasukan input fps sesuai videonya
break bila durasi video habis
sistem interval dan delay pengecekan muka diubah, sekarang menggunakan detik, bukan frame
#log 0.05: setting parameter detectMultiScale untuk mengatur sensitivitas dan akurasi deteksi muka
write durasi proses, durasi video, dan parameter detectMultiScale
#log 0.05b: tambah variabel dan write interval dan delay
#log 0.06: z counter untuk menghitung jumlah muka yang terdeteksi digantikan numDetect
'''
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import cv2
import numpy as np
import time
import argparse
import imutils


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = load_model('lenet.hdf5')
fps=17.5
captMedia=0
cap = cv2.VideoCapture(captMedia)

nsmile = 0
smile = 0
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

start=time.time()

#parameter detectMultiScale2
#scaleFactor 1.05 - 1.4, less=better, detect less, slower (minimum=1.05)
#minNeighbors 3 - 6, less= detect more, less accuracy
#minSize (50, 50) for faces, limit minimum size that can be detected, less=more processing time
scaleFactor = 1.05
minNeighbors= 6
minSize=	  (30, 30)

#setting interval dan delay
minInterval=4
minDelay=4

while True:
    #deteksi muka dengan cascade
    ret, frame = cap.read()
    if not ret:
      detik=int(detik)
      durasi = time.time()-start
      '''
      print('Durasi proses: %.4f' %durasi, ' detik')
      print('Durasi video:', menit,' menit', detik, ' detik')
      '''
      f= open("test.txt","a+")
      f.write('\r\n')
      f.write('Durasi proses: %.4f' %durasi + ' detik'+ '\r\n')
      f.write('Durasi video: '+ str(menit)+ ' menit '+ str(detik)+ ' detik '+ '\r\n')
      f.write('scaleFactor= '+ str(scaleFactor)+ '\r\n'+ 'minNeighbors= '+ str(minNeighbors)+ '\r\n'+ 'minSize= '+ str(minSize)+'\r\n')
      f.write('interval= '+ str(minInterval)+ '\r\n'+ 'delay= '+ str(minDelay))
      f.close()
      break
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces, numDetect = face_cascade.detectMultiScale2(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    numDetect=len(numDetect)
    img = frame.copy()
    
    #gambar kotak dan counter untuk muka    
    for (x,y,w,h) in faces:
      roi = gray[y:y + h, x:x + w]
      roi = cv2.resize(roi, (28, 28))
      roi = roi.astype("float") / 255.0
      roi = img_to_array(roi)
      roi = np.expand_dims(roi, axis=0)

      (notSmiling, smiling) = model.predict(roi)[0]
      label = "Smiling" if smiling > notSmiling else "Not Smiling"
      if label == 'Smiling':
        smile = smile + 1
      elif label == 'Not Smiling':
        nsmile = nsmile + 1

      cv2.putText(img, label, (x, y - 10),
      cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
      cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
       
    
    
       
    #menghitung detik asli video
    counter=counter + 1
    detik= counter/fps

    #interval deteksi
    counter2 = counter2 + 1
    interval = counter2/fps

    #delay bila tidak ada muka yang terdeteksi
    if numDetect==0:
      counter3 = counter3 + 1
      delay = counter3/fps
      if delay >= minDelay:
        delta=0
        z0=0
    
    #bila muka terdeteksi
    if numDetect>=1:
      delay=0
      if interval>=minInterval:
        counter2=0
        counter3=0
        delta = z0-numDetect
        if z0<=numDetect:
          z2= z2 + abs(delta)
        z0=numDetect
     

    
    
    

    #print total orang per __ detik
    if detik >=60:
      menit = menit + 1
      space=120+(menit*20)
      print('Menit '+str(menit)+': '+str(z2)+' orang')
      '''
      f= open("test.txt","a+")
      f.write('Menit '+str(menit)+': '+str(z2)+' orang\r\n')
      f.close()
      '''
      z2=0
      z0=0
      counter=0
    
    if captMedia==0:
      font = cv2.FONT_HERSHEY_SIMPLEX
      #cv2.putText(img,str(numDetect),(10,160), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      
      detik=int(detik)
      #cv2.putText(img,str(interval)+'s',(10,20), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Smile: '+ str(smile),(10,20), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'NSmile: '+ str(nsmile),(10,40), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      #cv2.putText(img,'Delta: '+str(abs(delta)),(10,40), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Person: '+str(numDetect),(10,60), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.putText(img,'Total: '+str(z2),(10,80), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      #cv2.putText(img,'Delay: '+str(delay),(10,100), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      #cv2.putText(img,'Detik: '+str(detik),(10,120), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      #cv2.putText(img,'z0: '+str(z0),(10,140), font, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.imshow('img',img)
      smile = 0
      nsmile = 0
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 

     
      
      
        
cap.release()
cv2.destroyAllWindows
                                     