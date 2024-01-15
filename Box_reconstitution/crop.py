#import
from PIL import Image
import os
import sys
import cv2
import numpy as np

#folder path + crop to apply
folder_path = sys.argv[1]
crop_x = int(sys.argv[2])
crop_y = int(sys.argv[3])

#coordinates of the cropped zone
y_i = 0+2*crop_y
y_f = 1080-0*crop_y
x_i = 0+1*crop_x
x_f = 1920-1*crop_x

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

delta_y = y_f-y_i
delta_x = x_f-x_i

#determine the size of the reconstructed image
height = (height_box-2)*delta_y+(1080-y_i)+y_f
width = (width_box-2)*delta_x+(1920-x_i)+x_f

#creating a blank image
box = Image.new('RGB', (width, height))

count = 0

#cuts all folder images to defined dimensions
for image_filename in sorted(os.listdir(folder_path),reverse=True):
    image_path = os.path.join(folder_path, image_filename)
    to_cut = Image.open(image_path)
    
    #x and y coordinates of the part
    x_part = (count//height_box)
    y_part = (count%height_box)
    
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
    
    #cuts and places in the right place on the reconstructed image
    cut = to_cut.crop((local_x_i, local_y_i, local_x_f, local_y_f))
    box.paste(cut,(local_x_i+x_part*delta_x,local_y_i+y_part*delta_y))
    count = count+1

#save the result
box.save("crop.jpg")
