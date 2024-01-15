#import
import cv2
import numpy as np
import os
import sys
import csv

#retrieving arguments (parameters + folder path)
scale_factor = float(sys.argv[1])
nei_min = int(sys.argv[2])
min_size = int(sys.argv[3])
image_path = sys.argv[4]
cascade_path = sys.argv[5]

#class identifier
class_id = 0

#counted insects counter
count_nb = 0
#total width and height (to calcumate mean)
w_tot = 0
h_tot = 0

#read image + save dimensions
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
height, width, channels = img.shape

#folder for annotation
data_annotation = "Annotation_txt"
if not os.path.exists(data_annotation):
        os.makedirs(data_annotation)
#set the output annotation file path
image_filename_sp, _ = os.path.splitext(os.path.basename(image_path))
image_filename_txt = image_filename_sp + ".txt"
output_file_path = os.path.join(data_annotation,image_filename_txt)

#create cascade classifier from xml file
cascade_classifier = cv2.CascadeClassifier(cascade_path)
#detect objects
found = cascade_classifier.detectMultiScale(img,scale_factor,nei_min,min_size)

#copy original image for visualization
out = img.copy()

#open annotation file
with open(output_file_path, 'w') as output_file:

    #if there is at least one detection
    if len(found) != 0:
        #for every detected object
        for (x, y, w, h) in found :
             
            #apply a margin on each side
            margin = 5
            x_i_det = max(0,x-margin)
            x_f_det = min(width,x+w+margin)
            y_i_det = max(0,y-margin)
            y_f_det = min(height,y+h+margin)
            
            #normalized coordinates
            x_center = (x_i_det + (x_f_det-x_i_det)/ 2) / width
            y_center = (y_i_det + (y_f_det-y_i_det)/ 2) / height
            width_normalized = (x_f_det-x_i_det) / width
            height_normalized = (y_f_det-y_i_det) / height
           
            #write in the anntation file
            output_file.write(f"{class_id} {x_center} {y_center} {width_normalized} {height_normalized}\n")
            
                
            #visualization of bounding boxes in blue and increment counters
            cv2.rectangle(out, (x_i_det,y_i_det), (x_f_det,y_f_det), (255, 0, 0), 8)
            count_nb += 1
            w_tot += w
            h_tot += h
    
     
    
            #cuts every insect in an individual image
            insect = img[y_i_det:y_f_det, x_i_det:x_f_det] 
            #folder for individuals images
            data_indiv = 'Insects'
            if not os.path.exists(data_indiv):
                os.makedirs(data_indiv)           
            if not os.path.exists(os.path.join(data_indiv,image_filename_sp)):
                #sub-folder with the name of the box
                os.mkdir(os.path.join(data_indiv,image_filename_sp))
            
            #save every individual image (insect)
            cv2.imwrite(os.path.join(os.path.join(data_indiv,image_filename_sp) , 'insect'+str(count_nb)+'.png'), insect)
            
#folder for visualization
data_out = "Out"
if not os.path.exists(data_out):
        os.makedirs(data_out)   
#save the annoted image for visualization    
cv2.imwrite(os.path.join(data_out,'out_'+os.path.basename(image_path)+'.png'), out)

print('Number of insects : '+str(count_nb))
w_mean = w_tot/count_nb
h_mean = h_tot/count_nb

#open file for statistical analysis
fichier_stat = 'out.csv'
with open(fichier_stat, mode='a', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv,delimiter=';')

    #write headers if the file has just been created
    if not fichier_stat:
        writer.writerow(["ScaleFactor","NeiMin","MinSize","Path","Count","Width_mean","Height_mean","Method"])

    #write a new line with the values
    writer.writerow([scale_factor,nei_min,min_size,image_path,count_nb,w_mean,h_mean,0])

