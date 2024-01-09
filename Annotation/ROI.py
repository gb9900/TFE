#import
import cv2
import numpy as np
import sys
import os

#image path
img_path= sys.argv[1]

#read image
img_raw = cv2.imread(img_path)
height, width, channels = img_raw.shape

#select ROIs GUI
ROIs = cv2.selectROIs("Select samples",img_raw,True,False)

#counter to save image with different name
count_id=0

#identification class
class_id = 0

#folder for annotation
data_annot = "annot"
if not os.path.exists(data_annot):
    os.makedirs(data_annot)
image_filename_sp, _ = os.path.splitext(os.path.basename(img_path))
image_filename_txt = image_filename_sp + ".txt"
output_file_path = os.path.join(data_annot,image_filename_txt)

#folder for individuals images
path = 'ROI'
if not os.path.exists(path):
    os.makedirs(path)           
if not os.path.exists(os.path.join(path,image_filename_sp)):
    #sous-dossier
    os.mkdir(os.path.join(path,image_filename_sp))
    
#for every box
with open(output_file_path, 'w') as output_file:
    for rect in ROIs:
            xi=rect[0]
            yi=rect[1]
            w=rect[2]
            h=rect[3]
            
            xf = xi+w
            yf = yi+h

            #crop roi from original image
            img_crop=img_raw[yi:yf,xi:xf]
            
            x_center = (xi + (xf-xi)/ 2) / width
            y_center = (yi + (yf-yi)/ 2) / height
            width_normalized = (xf-xi) / width
            height_normalized = (yf-yi) / height
            
            output_file.write(f"{class_id} {x_center} {y_center} {width_normalized} {height_normalized}\n")

        
	        #save cropped image
            cv2.imwrite(os.path.join(os.path.join(path,image_filename_sp) , 'ROI'+str(count_id)+'.png'), img_crop)

            count_id+=1

