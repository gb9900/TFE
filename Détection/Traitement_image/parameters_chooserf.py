#import
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout ,  QFileDialog
from PyQt5 import QtCore
import cv2
import numpy as np
import sys
import os
import subprocess
import time

#définition d'une taille maximale d'affichage des images pour utiliser le GUI facilement
MAX_WIDTH=1200
MAX_HEIGHT=675

def nothing(x):
    pass

def close_project():
    sys.exit(app.exec_())

#chargement de l'image + resize si besoin
def load_img(filename):
    global hMin
    global sMin
    global vMin
    global hMax
    global sMax
    global vMax
    global blur
    global erodex
    global erodey
    global sizeMin
    global sizeMax

    image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width, channels = image.shape
    
    #création d'une fenêtre vierge
    cv2.namedWindow('image')

    #création de curseurs pour modifier les paramètres
    cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
    cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
    cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
    cv2.createTrackbar('VMax', 'image', 0, 255, nothing)
    cv2.createTrackbar('Blur', 'image', 0, 150, nothing)
    cv2.createTrackbar('ErodeX', 'image', 0, 1000, nothing)
    cv2.createTrackbar('ErodeY', 'image', 0, 1000, nothing)
    cv2.createTrackbar('AreaMin', 'image', 0, 50000, nothing)
    cv2.createTrackbar('AreaMax', 'image', 0, 2000000, nothing)

    #valeurs par défaut
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)
    cv2.setTrackbarPos('AreaMin', 'image', 50000)
    cv2.setTrackbarPos('AreaMax', 'image', 2000000)

    while(1):
        #time.sleep(0.5)
        #prend les positions actuelles des curseurs comme valeurs des paramètres
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')
        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')
        blur = cv2.getTrackbarPos('Blur', 'image')
        erodex = cv2.getTrackbarPos('ErodeX', 'image')
        erodey = cv2.getTrackbarPos('ErodeY', 'image')
        sizeMin = cv2.getTrackbarPos('AreaMin', 'image')
        sizeMax = cv2.getTrackbarPos('AreaMax', 'image')
        
        #bornes pour appliquer un seuil
        lower = np.array([hMin, sMin, vMin], np.uint8)
        upper = np.array([hMax, sMax, vMax], np.uint8)

        #application du seuil hsv
        mask = cv2.inRange(hsv, lower, upper)
        
        #le taille du noyau doit être impaire pour le flou médian
        if(blur%2==1):    
            mb = cv2.medianBlur(mask,blur)
            
        else:
            mb = cv2.medianBlur(mask,blur+1)
            
        if(erodex%2==1):
            erodexx = erodex
    
        else:
            erodexx = erodex+1

        if(erodey%2==1):
            erodeyy = erodey
            
        else:
            erodeyy = erodey+1
            
        kernel = np.ones((erodeyy, erodexx), np.uint8)
        ero = cv2.dilate(mb, kernel)
        erob = cv2.copyMakeBorder(ero,1,1,1,1, cv2.BORDER_CONSTANT, value=255)
        edges1 = cv2.Canny(erob, 0, 150)
        edges = cv2.dilate(edges1, np.ones((3, 3), np.uint8))
 
        #contours des insectes
        contours, _ = cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        out = image.copy()
        ero2 = erob.copy()
        #prise en compte de chaque contour avec une aire définie par le curseur sizeMin
        for co in contours:
            area = cv2.contourArea(co)
            if area > sizeMin and area < sizeMax:      
                x,y,w,h = cv2.boundingRect(co)
                #si le contour fait 3/4 de la largeur ou hauteur, c'est probablement une erreur
                if w>0.75*width or h>0.75*height:
                    continue
                    
                #marge de chaque coté car median blur peut effacer des details
                marge = 5
                xi = max(0,x-marge)
                xf = min(width,x+w+marge)
                yi = max(0,y-marge)
                yf = min(height,y+h+marge)
                cv2.rectangle(ero2, (xi,yi), (xf,yf), (0, 255, 0), 8)
               
                cv2.rectangle(out, (xi,yi), (xf,yf), (0, 255, 0), 8)
                        
        
        #montre le masque ansi que l'image de base avec les détections
        if width>MAX_WIDTH:
            #print("RESIZE")
            f1 = MAX_WIDTH / width
            f2 = MAX_HEIGHT / height
            f = min(f1, f2)
            dim = (int(width * f), int(height * f))
            ero2 = cv2.resize(ero2, dim)
            out = cv2.resize(out, dim)
        cv2.imshow('image', ero2)
        cv2.imshow('image2', out)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def saveparam():
    #sélection du chemin vers le fichier csv
    tmpdial=QFileDialog()
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    #options |= QFileDialog.DontConfirmOverwrite 
    
    filename, _ = tmpdial.getSaveFileName(None, 
            "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
    if os.path.exists(filename):
        print("REMOVE")
        os.remove(filename)
    if filename:
        print(filename)
        #ouverture du fichier
        f=open(filename, 'w')
        #écriture de tous les paramètres
        f.write("\t".join([str(hMin), str(sMin), str(vMin), str(hMax),str(sMax), str(vMax), str(blur), str(erodex),str(erodey),str(sizeMin),str(sizeMax),filenamei]))
        f.close()
        

           
            
def choose_img(x):
    global filenameimg
    global filenamei
    
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
    print("IMAGE SELECTED")
    if filename:
        filenameimg = os.path.dirname(filename)
        filenamei = filename
        print(filename)
        load_img(filename)


def loadparam(x):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt);;CSV Files (*.csv)", options=options)
    if filename:
        print(filename)
        with open(filename, 'r') as fichier_csv:
    
            premiere_ligne = fichier_csv.readline().rstrip('\n')

            valeurs = premiere_ligne.split('\t')

            #récuperation des valeurs de la première ligne
            hMin, sMin, vMin, hMax, sMax, vMax, blur, erodex, erodey, sizeMin, sizeMax = map(int,valeurs[:11])
            cv2.setTrackbarPos('HMin', 'image', hMin)
            cv2.setTrackbarPos('SMin', 'image', sMin)
            cv2.setTrackbarPos('VMin', 'image', vMin)
            cv2.setTrackbarPos('HMax', 'image', hMax)
            cv2.setTrackbarPos('SMax', 'image', sMax)
            cv2.setTrackbarPos('VMax', 'image', vMax)
            cv2.setTrackbarPos('Blur', 'image', blur)
            cv2.setTrackbarPos('ErodeX', 'image', erodex)
            cv2.setTrackbarPos('ErodeY', 'image', erodey)
            cv2.setTrackbarPos('AreaMin', 'image', sizeMin)
            cv2.setTrackbarPos('AreaMax', 'image', sizeMax)
          
            print("LOADED")
            
def start_cnt_gem(x):
    subprocess.run(["python", "det-gemblouxf.py", str(hMin), str(sMin), str(vMin), str(hMax), str(sMax), str(vMax), str(blur), str(erodex), str(erodey), str(sizeMin), str(sizeMax),filenameimg])
    
def start_cnt_terv(x):
    subprocess.run(["python", "det-tervf.py", str(hMin), str(sMin), str(vMin), str(hMax), str(sMax), str(vMax), str(blur), str(erodex), str(erodey), str(sizeMin), str(sizeMax),filenamei])
   
        
app = QApplication([])
window = QWidget()
window.setWindowTitle("Insect counter")
window.setMinimumWidth(500)
layout = QVBoxLayout()
but_img=QPushButton('Choose image')
layout.addWidget(but_img)
but_img.clicked.connect(choose_img)

but_save_param=QPushButton('Save parameters')
layout.addWidget(but_save_param)
but_save_param.clicked.connect(saveparam)

but_load_param=QPushButton('Load parameters')
layout.addWidget(but_load_param)
but_load_param.clicked.connect(loadparam)

but_cnt=QPushButton('Start counting (box parts)')
layout.addWidget(but_cnt)
but_cnt.clicked.connect(start_cnt_gem)

but_cnt=QPushButton('Start counting (complete box)')
layout.addWidget(but_cnt)
but_cnt.clicked.connect(start_cnt_terv)



window.setLayout(layout)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window.show()
app.exec()
