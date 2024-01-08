#import
from PIL import Image
import os
import sys
import cv2
import numpy as np

filenameimg = sys.argv[1]
cropx = int(sys.argv[2])
cropy = int(sys.argv[3])

#coordonnées de la zone de comptage
pyi = 0+2*cropy
pyf = 1080-0*cropy
pxi = 0+1*cropx
pxf = 1920-1*cropx

#nb d'images en x et en y
if len(os.listdir(filenameimg))>36:
    if len(os.listdir(filenameimg))>42:
        ny = 12
    else:
        ny = 7
else:
    ny = 6
    
nx = 6

dy = pyf-pyi
dx = pxf-pxi

height = (ny-2)*dy+(1080-pyi)+pyf
width = (nx-2)*dx+(1920-pxi)+pxf

boite = Image.new('RGB', (width, height))
#dossier contenant les différentes parties de la boite
data_directory = filenameimg
count = 0
for image_filename in sorted(os.listdir(data_directory),reverse=True):
    image_path = os.path.join(data_directory, image_filename)
    cuti = Image.open(image_path)
    
    xx = (count//ny)
    yy = (count%ny)
    
    pxii = pxi
    pyii = pyi
    pxff = pxf
    pyff = pyf
    
    
    if(xx == 0): 
        pxii = 0
    if(xx == nx-1):
        pxff = 1920  
    if(yy == 0):
        pyii = 0
    if(yy == ny-1):
        pyff = 1080
        
    cutf = cuti.crop((pxii, pyii, pxff, pyff))
    boite.paste(cutf,(pxii+xx*dx,pyii+yy*dy))
    count = count+1

boite.save("crop.jpg")
