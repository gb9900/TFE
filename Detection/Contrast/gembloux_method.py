#import
import cv2
import numpy as np
import os
import sys
import csv

#retrieving arguments (parameters + path folder)
h_min = int(sys.argv[1])
s_min = int(sys.argv[2])
v_min = int(sys.argv[3])
h_max = int(sys.argv[4])
s_max = int(sys.argv[5])
v_max = int(sys.argv[6])
blur = int(sys.argv[7])
erode_x = int(sys.argv[8])
erode_y = int(sys.argv[9])
size_min = int(sys.argv[10])
size_max = int(sys.argv[11])
folder_path = sys.argv[12]

#kernel size must be odd for median blur and erode
if(blur%2!=1):
    blur = blur+1
if(erode_x%2==1):
    erode_x = erode_x
else:
    erode_x = erode_x+1    
if(erode_y%2==1):
    erode_y = erode_y      
else:
    erode_y = erode_y+1
#kernel for erosion (horizontal and vertical cobined)
kernel = np.ones((erode_y, erode_x), np.uint8)
  
#coordinates of the counting zone
y_i = 255
y_f = 825
x_i = 500
x_f = 1380

#determine the height of the box (number of images in y) according to the total number of images in the folder
if len(os.listdir(folder_path))>36:
    if len(os.listdir(folder_path))>42:
        height_box = 12
    else:
        height_box = 7
else:
    height_box = 6
    
#width of the box (number of images in x) is always 6
width_box = 6

#folder for annotation
data_annot = "Annotation"
if not os.path.exists(data_annot):
        os.makedirs(data_annot)
if not os.path.exists(os.path.join(data_annot,os.path.basename(folder_path))):
    #sub-folder with the name of the box
    os.mkdir(os.path.join(data_annot,os.path.basename(folder_path)))

#class identifier
class_id = 0

#insects counter
count_id = 0
#part counter (to know x and y part position)
count_part = 0
#counted insects counter
count_nb = 0
#total width and height (to calcumate mean)
w_tot = 0
h_tot = 0

#for every part of the box
for image_filename in sorted(os.listdir(folder_path),reverse=True):
    image_path = os.path.join(folder_path, image_filename)
    
    #read the image associated to the part + save dimenssions
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width, channels = img.shape
    
    #create an annotation file per part
    #set the output annotation file path
    image_filename_txt, _ = os.path.splitext(image_filename)
    image_filename_txt = image_filename_txt + ".txt"
    output_file_path = os.path.join(os.path.join(data_annot,os.path.basename(folder_path)), image_filename_txt)

    #convert to HSV space
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #HSV threshold [Hue, Saturation, Value]
    #Hue [0,179] all colors
    #Saturation [0,255] from least to most saturated (color)
    #Value [0,255] from darkest (black) to lightest (brightness)
    lower = np.array([h_min, s_min, v_min], np.uint8)
    upper = np.array([h_max, s_max, v_max], np.uint8)

    #application of the threshold
    mask = cv2.inRange(hsv, lower, upper)

    #apply median blur
    med_blur = cv2.medianBlur(mask,blur)
    #apply erosion
    erode = cv2.dilate(med_blur,kernel)
    #add a contour to the edge to close all contours
    erode_with_border = cv2.copyMakeBorder(erode,1,1,1,1, cv2.BORDER_CONSTANT, value=255)
    #apply canny to detect edges
    edges = cv2.Canny(erode_with_border, 0, 150)
    #dilate edges a bit to avoid discontinuity
    edges_dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8))
    
    #list every contours
    contours, _ = cv2.findContours(edges_dilated, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

    #copy original image for visualization
    out = img.copy()
    
    #x and y coordinates of the part
    x_part = (count_part//height_box)
    y_part = (count_part%height_box)
    
    #create local variables to modify the zone if needed
    local_y_i = y_i
    local_y_f = y_f
    local_x_i = x_i
    local_x_f = x_f
    
    #if it is an edge, extend the zone up to it
    if(x_part == 0): 
        local_x_i = 0
    if(x_part == width_box-1):
        local_x_f = 1920  
    if(y_part == 0):
        local_y_i = 0
    if(y_part == height_box-1):
        local_y_f = 1080
    
    #visualization of the counting zone (in red)
    cv2.rectangle(out, (local_x_i,local_y_i), (local_x_f,local_y_f), (0, 0, 255), 2)

    #open annotation file
    with open(output_file_path, 'w') as output_file:
    
        #each contour between sizeMin and sizeMax is taken into account 
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > size_min and area < size_max:
                #bounding box coordinates     
                x,y,w,h = cv2.boundingRect(contour)
                #if the contour is too long, it is rejected
                if w>0.75*width or h>0.75*height:
                    continue
                    
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
                
                #taken into account if is situated in the counting zone
                if x_i_det > local_x_i and x_i_det < local_x_f and y_i_det > local_y_i and y_i_det < local_y_f:
                    
                    #visualization of bounding boxes in blue and increment counters
                    cv2.rectangle(out, (x_i_det,y_i_det), (x_f_det,y_f_det), (255, 0, 0), 2)
                    count_nb += 1
                    w_tot += w
                    h_tot += h
    
                else:
                    #visualization of bounding boxes in green otherwise
                    cv2.rectangle(out, (x_i_det,y_i_det), (x_f_det,y_f_det), (0, 255, 0), 2)
               
                #cuts every insect in an individual image
                insect = img[y_i_det:y_f_det, x_i_det:x_f_det] 
                #folder for individuals images
                data_indiv = 'Insect'
                if not os.path.exists(data_indiv):
                    os.makedirs(data_indiv)
                if not os.path.exists(os.path.join(data_indiv,os.path.basename(folder_path))):
                    #sub-folder with the name of the box
                    os.mkdir(os.path.join(data_indiv,os.path.basename(folder_path)))
                
                #save every individual image (insect)
                cv2.imwrite(os.path.join(os.path.join(data_indiv,os.path.basename(folder_path)) , 'insect'+str(count_id)+'.png'), insect)
                count_id += 1

    #folder for visualization
    data_visu = 'part'
    if not os.path.exists(data_visu):
        os.makedirs(data_visu)
    if not os.path.exists(os.path.join(data_visu,os.path.basename(folder_path))):
        #sub-folder with the name of the box
        os.mkdir(os.path.join(data_visu,os.path.basename(folder_path)))
    
    #save every image annoted for visualization
    cv2.imwrite(os.path.join(os.path.join(data_visu,os.path.basename(folder_path)), 'part'+str(count_part)+'.png'), out)
    count_part += 1
    
print('Number of insects : '+str(count_nb))
#calculate width and height mean
w_mean = w_tot/count_nb
h_mean = h_tot/count_nb

#open file for statistical analysis
fichier_stat = 'out.csv'
with open(fichier_stat, mode='a', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv,delimiter=';')

    #write headers if the file has just been created
    if not fichier_stat:
        writer.writerow(["H_min", "S_min", "V_min","H_max", "S_max", "V_max","Blur","Erode_x","Erode_y","Area_min","Area_max","Path","Count","Width_mean","Height_mean","Method"])

    #write a new line with the values
    writer.writerow([h_min,s_min,v_min,h_max,s_max,v_max,blur,erode_x,erode_y,size_min,size_max,folder_path,count_nb,w_mean,h_mean,0])


