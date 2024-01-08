#import
import cv2
import numpy as np
import os
import sys
import csv

#récuperation des arguments
h_min = int(sys.argv[1])
s_min = int(sys.argv[2])
v_min = int(sys.argv[3])
h_max = int(sys.argv[4])
s_max = int(sys.argv[5])
v_max = int(sys.argv[6])
blurr = int(sys.argv[7])
dilx = int(sys.argv[8])
dily = int(sys.argv[9])
sizem = int(sys.argv[10])
sizema = int(sys.argv[11])
filenameimg = sys.argv[12]

if(blurr%2!=1):
    blurr = blurr+1
    
if(dilx%2==1):
    dilx = dilx
else:
    dilx = dilx+1    
if(dily%2==1):
    dily = dily      
else:
    dily = dily+1

kernel = np.ones((dily, dilx), np.uint8)

#chemin vers l'image de base
image_path = filenameimg

#nom de la classe pour annotation
class_id = 0

#initailisation du compteur
count_nb = 0
w_tot = 0
h_tot = 0

img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
height, width, channels = img.shape

data_annot = "annot"
if not os.path.exists(data_annot):
        os.makedirs(data_annot)
#creation d'un fichier txt pour annotation de chaque insecte dans le but de l'utiliser avec un modèle YOLO
image_filename_sp, _ = os.path.splitext(os.path.basename(image_path))
image_filename_txt = image_filename_sp + ".txt"
output_file_path = os.path.join(data_annot,image_filename_txt)

#conversion en HSV
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#seil de detection en HSV [Hue, Saturation, Value]
#Hue [0,179] toutes les couleurs
#Saturation [0,255] du moins au plus sature (couleur)
#Value [0,255] du plus sombre (noir) au plus clair (luminosite)
SEUIL_MIN = np.array([h_min, s_min, v_min], np.uint8)
SEUIL_MAX = np.array([h_max, s_max, v_max], np.uint8)

#application du seil pour détection des insectes
seuil = cv2.inRange(hsv, SEUIL_MIN, SEUIL_MAX)

#flou median pour homogeniser chaque insecte
mb = cv2.medianBlur(seuil,blurr)
ero = cv2.dilate(mb,kernel)
erob = cv2.copyMakeBorder(ero,1,1,1,1, cv2.BORDER_CONSTANT, value=255)
edges1 = cv2.Canny(erob, 0, 150)
edges = cv2.dilate(edges1, np.ones((3, 3), np.uint8))

#contours des insectes
contours, _ = cv2.findContours(edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

#copie et recuperation des dimensions pour les statistiques
out = img.copy()

#ouverture du fichier d'annotation
with open(output_file_path, 'w') as output_file:

#prise en compte de chaque contour avec une aire minimum
    for co in contours:
        area = cv2.contourArea(co)
        if area > sizem and area < sizema:      
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
            
            x_center = (xi + (xf-xi)/ 2) / width
            y_center = (yi + (yf-yi)/ 2) / height
            width_normalized = (xf-xi) / width
            height_normalized = (yf-yi) / height
            
            output_file.write(f"{class_id} {x_center} {y_center} {width_normalized} {height_normalized}\n")
            
                
            #tracage d'un rectangle en bleu et incrémentation du compteur d'insectes
            cv2.rectangle(out, (xi,yi), (xf,yf), (255, 0, 0), 8)
            count_nb += 1
            w_tot += w
            h_tot += h
    
            #découpe de chaque instecte détecté en une image individuelle
            insect = img[yi:yf, xi:xf] 
            #l'image de l'insecte individuel est sauvée dans un dossier avec un ID
            path = 'insect'
            if not os.path.exists(path):
                os.makedirs(path)           
            if not os.path.exists(os.path.join(path,image_filename_sp)):
                #sous-dossier
                os.mkdir(os.path.join(path,image_filename_sp))
            
            
            cv2.imwrite(os.path.join(os.path.join(path,image_filename_sp) , 'insect'+str(count_nb)+'.png'), insect)


#resultat
data_out = "out"
if not os.path.exists(data_out):
        os.makedirs(data_out)       
cv2.imwrite(os.path.join(data_out,'out_'+os.path.basename(image_path)+'.png'), out)
print('nombre : '+str(count_nb))
w_mean = w_tot/count_nb
h_mean = h_tot/count_nb
#ouvrir le fichier pour les stats
fichier_existe = 'out.csv'
with open(fichier_existe, mode='a', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv,delimiter=',')

    #écrire les en-têtes si le fichier vient d'être créé
    if not fichier_existe:
        writer.writerow(["H_min", "S_min", "V_min","H_max", "S_max", "V_max","Blur","Erode_x","Erode_y","Area_min","Area_max","Path","Count","Width_mean","Height_mean","Method"])

    #écrire une nouvelle ligne avec les valeurs
    writer.writerow([h_min,s_min,v_min,h_max,s_max,v_max,blurr,dilx,dily,sizem,sizema,image_path,count_nb,w_mean,h_mean,1])
