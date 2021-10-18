
import requests
import cv2
import numpy as np
import os, glob
import time
#os.remove("c:/Users/gguic/Desktop/TCC/fotos/fotos*.jpg")
from cv2 import waitKey as wK

url = "http://192.168."
ip_ard=url+"1.115" #input("complete o ip do ard 192.168.")
ip_cam= url+"1.109" #input("complete o ip da cam 192.168.")
path = "c:/Users/gguic/Desktop/TCC/fotos/"
cont = 0
nome = input("nome: ")
#l = requests.get(ip_ard+"/laserOFF")
#requests.get(ip_cam+":8080/disabletorch")
f = "off"
c = str("on")

def getimage(ip_cam):  #return img
    

 
    img_resp = requests.get(ip_cam+":8080/shot.jpg")
    img_arr = np.array(bytearray(img_resp.content))
    img = cv2.imdecode(img_arr, -1)
        
    y = int(img.shape[0])
    x = int(img.shape[1])

    


    
    if wK(10) == ord('c'):
        a= int(x/2)
        b= int(y/2)
        print ("x= " , x,"a = ", a,"y = ", y , "b = ", b)
        i = 0
        while (i==0): 
            img = cv2.line(img, (a,0), (a,y), (0, 255, 0), 3)
            img = cv2.line(img, (0,b), (x,b), (0, 255, 0), 3)
            cv2.imshow("vivi", cv2.resize(img,(600,400)))

            if wK(10) == ord('c'):
                i = 1
                cv2.destroyWindow("vivi")

    return img

def led(url, f):
    # turn on or off the flash light
    if f =="off":
        requests.get(url+":8080/enabletorch")
        f = "on"
        print ("flash ligado")
    
    elif f == "on": 
        requests.get(url+":8080/disabletorch")
        f = "off"
    requests.get(url+":8080/focus")
    return f

def camera(url, c):

        requests.get(url+":8080/settings/ffc?set={}".format(c))
        c = str("off")

        requests.get(url+":8080/settings/ffc?set={}".format(c))
        c = str("on")
        requests.get(url+":8080/focus")
        return c

n = int(input("quantas fotos serão tiradas? máx: 128 \n"))

if (n>=129):
    print("erro")
    n = input("quantas fotos serão tiradas? máx: 32")

ppf=256/(2*n) #Passo Por Foto
print("necessario ", ppf)
Pm = 128 #passos para completar uma volta, chamada no arduino é 2 por vez
P=0
o=ppf-int(ppf)
sobr= 0

#requests.get(ip_cam+":8080/focus")
l=requests.get(ip_ard+"/laserON")

while (cont<n):
    file =path+nome+"%s" % cont
    img=getimage(ip_cam)    
    filel=file+"l.jpg"
    b = cv2.imwrite(filel,img)
    print("Image written to file-system : ", b)
    print("File name: ", filel)
    #roda (x graus)/(y passos) 1 chamada = 2 passos
    p=0
    while (p<int(ppf)):
        f=requests.get(ip_ard+"/passo")
        print(f.text)
        print("ok")
        p=p+1
        print(p)
        P=P+1
        if(P>=Pm):
            break
    if(P>=Pm):
        break
        
    sobr= sobr+o
    
    if (sobr>=1):
        sobr=sobr-1
        f=requests.get(ip_ard+"/passo")
        P=P+1
        
    cont=cont+1
    #repete
    
f = led(ip_cam, "off")    
# cont=0
# P=0
# sobr=0
# while (cont<n):
#     file =path+nome+"%s" % cont
#     img=getimage(ip_cam)
#     #cv2.imshow("androidCam", cv2.resize(img,(600,400)))
#     #tirar foto c/flash //falta controlar o flash
#     filef=file+"f.jpg"
#     b = cv2.imwrite(filef,img)
#     print("Image written to file-system : ", b)
#     print("File name: ", filef)
#     #roda (x graus)/(y passos) 1 chamada = 2 passos
#     p=0
#     while (p<int(ppf)):
#          f=requests.get(ip_ard+"/passo")
#          print(f.text)
#          print("ok")
#          p=p+1
#          print(p)
#          P=P+1
#          if(P>=Pm):
#              break
#     if(P>=Pm):
#          break
         
#     sobr= sobr+o
    
#     if (sobr>=1):
#         sobr=sobr-1
#         f=requests.get(ip_ard+"/passo")
#         P=P+1
#     cont=cont+1
    
# f = led(ip_cam, "on")
# print("fotos tiradas")