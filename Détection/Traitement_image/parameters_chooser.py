#import
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout ,  QFileDialog
from PyQt5 import QtCore
import cv2
import numpy as np
import sys
import os
import subprocess
import time

#definition of a maximum image display size for easy GUI use
MAX_WIDTH=1200
MAX_HEIGHT=675

def nothing(x):
    pass

def close_project():
    sys.exit(app.exec_())

#def to create visualization windows
def load_img(img_path):
    #global parameters
    global hMin
    global sMin
    global vMin
    global hMax
    global sMax
    global vMax
    global blur
    global erodeX
    global erodeY
    global sizeMin
    global sizeMax

    #load visualization image + size, create an hsv version
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    height, width, channels = image.shape
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    #create a blank window
    cv2.namedWindow('image')

    #create cursors to modify parameters
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

    #default values
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)
    cv2.setTrackbarPos('AreaMin', 'image', 50000)
    cv2.setTrackbarPos('AreaMax', 'image', 2000000)

    while(1):
        #takes current cursor positions as parameter values
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')
        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')
        blur = cv2.getTrackbarPos('Blur', 'image')
        erodeX = cv2.getTrackbarPos('ErodeX', 'image')
        erodeY = cv2.getTrackbarPos('ErodeY', 'image')
        sizeMin = cv2.getTrackbarPos('AreaMin', 'image')
        sizeMax = cv2.getTrackbarPos('AreaMax', 'image')
        
        #threshold bounds
        lower = np.array([hMin, sMin, vMin], np.uint8)
        upper = np.array([hMax, sMax, vMax], np.uint8)

        #application of the threshold
        mask = cv2.inRange(hsv, lower, upper)
        
        #kernel size must be odd for median blur and erode
        #apply median blur
        if(blur%2==1):    
            med_blur = cv2.medianBlur(mask,blur)  
        else:
            med_blur = cv2.medianBlur(mask,blur+1)
        
        if(erodeX%2==1):
            erode_horiz = erodeX
        else:
            erode_horiz = erodeX+1
        if(erodeY%2==1):
            erode_vertic = erodeY  
        else:
            erode_vertic = erodeY+1
        
        #apply erosion 
        kernel = np.ones((erode_vertic, erode_horiz), np.uint8)
        erode = cv2.dilate(med_blur, kernel)
        #add a contour to the edge to close all contours
        erode_with_border = cv2.copyMakeBorder(erode,1,1,1,1, cv2.BORDER_CONSTANT, value=255)
        edges = cv2.Canny(erode_with_border, 0, 150)
        edges_dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8))
 
        #contour detection
        contours, _ = cv2.findContours(edges_dilated, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        
        #copy original and eroded image for visualization
        out_visu = image.copy()
        erode_visu = erode_with_border.copy()
        
        #each contour between sizeMin and sizeMax is taken into account 
        for cont in contours:
            area = cv2.contourArea(cont)
            if area > sizeMin and area < sizeMax:  
                #bounding box coordinates    
                x,y,w,h = cv2.boundingRect(cont)
                #if the contour is too long, it is rejected
                if w>0.75*width or h>0.75*height:
                    continue
                    
                #apply a margin on each side
                margin = 5
                x_i = max(0,x-margin)
                x_f = min(width,x+w+margin)
                y_i = max(0,y-margin)
                y_f = min(height,y+h+margin)
                
                #visualization of bounding boxes on original and eroded image 
                cv2.rectangle(erode_visu, (x_i,y_i), (x_f,y_f), (0, 255, 0), 8)
                cv2.rectangle(out_visu, (x_i,y_i), (x_f,y_f), (0, 255, 0), 8)
                        
        #resize if the maximum size is exceeded
        if width>MAX_WIDTH:
            #determine factor of reduction
            f1 = MAX_WIDTH / width
            f2 = MAX_HEIGHT / height
            f = min(f1, f2)
            dim = (int(width * f), int(height * f))
            erode_visu_resized = cv2.resize(erode_visu, dim)
            out_visu_resized = cv2.resize(out_visu, dim)
        cv2.imshow('image', erode_visu_resized)
        cv2.imshow('image2', out_visu_resized)
        
        #quit the GUI when "q" is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

#def to save parameters in a csv file
def saveparam():
    #select path to csv file
    tmpdial=QFileDialog()
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    csv_pah, _ = tmpdial.getSaveFileName(None, 
            "Save File", "", "All Files(*);;Text Files(*.txt)", options = options)
            
    #overwrite existing file
    if os.path.exists(csv_pah):
        print('OVERWRITE')
        os.remove(csv_pah)
        
    if csv_pah:
        print(csv_pah)
        #open file
        f=open(csv_pah, 'w')
        #write every parameters on one line
        f.write("\t".join([str(hMin), str(sMin), str(vMin), str(hMax),str(sMax), str(vMax), str(blur), str(erodeX),str(erodeY),str(sizeMin),str(sizeMax),img_path_visu]))
        f.close()

#def to select an image for visualization
def choose_img(x):
    #global variables for path to folder and visualization image
    global folder_path
    global img_path_visu
    
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    img_path, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
    print("IMAGE SELECTED")
    #save the path to the image and its folder
    if img_path:
        folder_path = os.path.dirname(img_path)
        img_path_visu = img_path
        print(img_path_visu)
        load_img(img_path_visu)

#def to load parameters from a csv file
def loadparam(x):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    img_path, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt);;CSV Files (*.csv)", options=options)
    if img_path:
        print(img_path)
        #open file
        with open(img_path, 'r') as fichier_csv:
            
            #read the only line    
            line = fichier_csv.readline().rstrip('\n')
            
            #retrieves line values
            values = line.split('\t')
            hMin, sMin, vMin, hMax, sMax, vMax, blur, erodeX, erodeY, sizeMin, sizeMax = map(int,values[:11])
            
            #sets cursors to these values
            cv2.setTrackbarPos('HMin', 'image', hMin)
            cv2.setTrackbarPos('SMin', 'image', sMin)
            cv2.setTrackbarPos('VMin', 'image', vMin)
            cv2.setTrackbarPos('HMax', 'image', hMax)
            cv2.setTrackbarPos('SMax', 'image', sMax)
            cv2.setTrackbarPos('VMax', 'image', vMax)
            cv2.setTrackbarPos('Blur', 'image', blur)
            cv2.setTrackbarPos('ErodeX', 'image', erodeX)
            cv2.setTrackbarPos('ErodeY', 'image', erodeY)
            cv2.setTrackbarPos('AreaMin', 'image', sizeMin)
            cv2.setTrackbarPos('AreaMax', 'image', sizeMax)
          
            print("LOADED")
        
#def to run script for counting method (gembloux), giving all the parameters
def start_cnt_gem(x):
    subprocess.run(["python", "gembloux_method.py", str(hMin), str(sMin), str(vMin), str(hMax), str(sMax), str(vMax), str(blur), str(erodeX), str(erodeY), str(sizeMin), str(sizeMax),folder_path]) #folder path is given
   
#def to run script for counting method (africamuseum), giving all the parameters
def start_cnt_terv(x):
    subprocess.run(["python", "africamuseum_method.py", str(hMin), str(sMin), str(vMin), str(hMax), str(sMax), str(vMax), str(blur), str(erodeX), str(erodeY), str(sizeMin), str(sizeMax),img_path_visu]) #image path is given
   
#create actions window with buttons
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
