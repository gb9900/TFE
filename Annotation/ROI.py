#import
import cv2
import numpy as np
import sys
import os

#image path
img_path = sys.argv[1]

#read image + save dimensions
img = cv2.imread(img_path)
height, width, _ = img.shape

#select ROIs GUI
ROIs = cv2.selectROIs("Select samples",img,True,False)

#counter to save image with different name
count_id = 0

#identification class
class_id = 0

#folder for annotation
data_annotation = "Annotation"
if not os.path.exists(data_annotation):
    os.makedirs(data_annotation)
#set the output annotation file path
image_filename, _ = os.path.splitext(os.path.basename(img_path))
image_filename_txt = image_filename + ".txt"
output_file_path = os.path.join(data_annotation,image_filename_txt)

#folder for individuals images
data_indiv = 'ROI'
if not os.path.exists(data_indiv):
    os.makedirs(data_indiv) 
#sub-folder             
if not os.path.exists(os.path.join(data_indiv,image_filename)):
    os.mkdir(os.path.join(data_indiv,image_filename))
    
#open annotation file
with open(output_file_path, 'w') as output_file:
    #for every ROI
    for rect in ROIs:
        
        #take coordinates
        x_i = rect[0]
        y_i = rect[1]
        w = rect[2]
        h = rect[3]
        
        x_f = x_i+w
        y_f = y_i+h

        #crop ROI from original image
        img_crop = img[y_i:y_f,x_i:x_f]
        
        #normalized coordinates
        x_center = (x_i + (x_f-x_i)/ 2) / width
        y_center = (y_i + (y_f-y_i)/ 2) / height
        width_normalized = (x_f-x_i) / width
        height_normalized = (y_f-y_i) / height
        
        #write in the anntation file
        output_file.write(f"{class_id} {x_center} {y_center} {width_normalized} {height_normalized}\n")

    
        #save cropped image
        cv2.imwrite(os.path.join(os.path.join(data_indiv,image_filename) , 'ROI'+str(count_id)+'.png'), img_crop)

        count_id+=1
