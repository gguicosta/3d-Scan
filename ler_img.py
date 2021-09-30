# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 12:23:04 2021

@author: gguic
"""

import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
from stl import mesh
from scipy.spatial import ConvexHull, Delaunay

    # termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def calib (criteria): #Encontrando a distorção radial da camera para calibrar a imagem 
    lin = 7 # linha no Cartão Xadrez
    col = 7 # coluna no Cartão Xadrez
    # preparar as posições em pontos, criando os espaços em: (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((col*lin,3), np.float32)
    objp[:,:2] = np.mgrid[0:lin,0:col].T.reshape(-1,2)
    
    # Arrays para guardar os pontos de todas as imagens
    objpoints = [] # 3d no plano da figura
    objp = objp.reshape(-1,1,3)
    imgpoints = [] # 2d no plano da imagem.
    
    cont= 0
    path = "c:/Users/gguic/Desktop/TCC/fotos/"
    
    for fname in glob.glob(path+"calib*"):
    
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # cv2.imshow('img', cv2.resize(gray,(600,400)))
    # Encontrar os cantos do xadrez 
        ret, corners = cv2.findChessboardCorners(gray, (lin,col),None)
    
    # Se achou, adicionar os pontos 2d e 3d (já refinados)
        if ret == True:
            objpoints.append(objp)
    
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
    
        # Mostrando os cantos
            # img2 = cv2.drawChessboardCorners(img, (lin,col), corners2, ret)
            # cv2.imshow('img2',cv2.resize(img2, (600,400)))
            # cv2.waitKey(500)
    
        else :
            print ("erro") 
    
        cont+= 1
        
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)    
    print("calibrou")
    

    return [ret, mtx, dist, rvecs, tvecs]

def superf(mtx, dist):

    file = "C:/Users/gguic/Desktop/TCC/fotos/new_dog*l.jpg"
    maxx = 4
    n=0
    ii=0
    cont= 0
    pointcloud= []
    hull = []
    for k in glob.glob(file):
        n+= 1
    #    if(n>maxx):
    #           break
    ang=360/n
    print(ang)
    
    for img1 in sorted(glob.glob(file), key=len):
        #img1 = "C:/Users/gguic/Desktop/TCC/fotos/cilindro1l.jpg"
        print(img1)
        img1 = cv2.imread(img1)
        h = img1.shape[0]
        w = img1.shape[1]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        dst = cv2.remap(img1,mapx,mapy,cv2.INTER_LINEAR)

        # recortando a imagem sem a distorção
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        # a=cv2.imwrite('calibresult.png',dst)
        # print(a)

        img = dst
        img2= dst
        #zeros= np.zeros(img.shape[:2], dtype = "unit8")
        (az, verd, verm) = cv2.split(img)
        (az2, verd2, verm2) = cv2.split(img2)


        edges = cv2.Canny(verm,20, 110)
        verm2 = cv2.Canny(verm2,100, 150)

        a, b = int(img.shape[0]),int(img.shape[1])
        z0=645
        y0=949
        teta=29*np.pi/180
        x,y,z= [],[],[]
        dte=(ang*np.pi/180)*ii
        ii+=1
        rvecs=np.asarray([0.0,0.0,dte])
        #rotation_matrix = np.zeros(shape=(3,3))
        R = cv2.Rodrigues(rvecs)[0]

        for i in range (a):
            pix=np.where(edges[i,:] == 255)
            shapepix=np.shape(pix)


            if (shapepix[1]>0):
                zi=-i+z0
                yi=pix[0][0]-y0
                xi=yi/np.tan(teta)

                if(yi>=-50):
                    if(yi<=200):
                        if(zi>=0):
                            x.append(xi)
                            y.append(yi)
                            z.append(zi)

            x=np.asarray(x)
            y=np.asarray(y)
            z=np.asarray(z)

            point0 = np.array([x,y,z]).T
            point1 = np.dot(point0, R).T
            point1 = point1   
        # for j in range(len(x)):
        #     # # Computing rotation matrix
        #     # rotation_matrix = np.zeros(shape=(3,3))
        #     # cv2.Rodrigues(rvecs, rotation_matrix)
        #     # #Apply rotation matrix to point
        #     # original_point = np.matrix([[1],[0],[0]])
        #     # rotated_point = rotation_matrix*original_point
        #     x[j]=R[0][0]*x[j]+R[0][1]*y[j]
        #     y[j]=R[1][0]*x[j]+R[1][1]*y[j]            

        pointcloud.append(point1)
        cont+=1

    # if (cont>maxx):
    #     break
    # '''termina de ler as imagens, saindo do loop'''
    # criando a figura com os pontos encontrados
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    pts = []
    
    
    for l in range(cont):
        for k in range(np.shape(pointcloud[l][2])[0]):
            popo = [(pointcloud[l][0][k]),(pointcloud[l][1][k]),(pointcloud[l][2][k])]
            pts.append(popo)


    pts = np.asarray(pts)
    
    
    # Plotando os pontos
    for k in range(cont):
        ax.scatter3D(pointcloud[k][0],pointcloud[k][1],pointcloud[k][2], color = "green", marker='.')
    
    # hull = ConvexHull(pts)
    # tess = Delaunay(hull.points)
    # # # print(hull.simplices)
    
    # for s in hull.simplices:
    #     s = np.append(s, s[0])  # Here we cycle back to the first coordinate
    #     ax.plot(pts[s, 0], pts[s, 1], pts[s, 2], "r-")
     
    
    plt.title("simple 3D scatter plot")
    ax.view_init(elev=10., azim=30)
    
    # show plot
    # plt.xlim(-100,100)
    # plt.ylim(-100,100)
    plt.show()
    
ret, mtx, dist, rvecs, tvecs = calib (criteria)
superf(mtx, dist)
