#import
import cv2
import numpy as np
import os
import sys
import csv

#récuperation des arguments
filenameimg = sys.argv[1]
scalefact = float(sys.argv[2])
neimin = int(sys.argv[3])
aa = int(sys.argv[4])
  
#coordonnées de la zone de comptage
pyi = 255
pyf = 825
pxi = 500
pxf = 1380

#nb d'images en x et en y
if len(os.listdir(filenameimg))>36:
    if len(os.listdir(filenameimg))>42:
        ny = 12
    else:
        ny = 7
else:
    ny = 6
    
nx = 6

#dossier contenant les différentes parties de la boite
data_directory = filenameimg
#dossier pour sauver les fichiers d'annotation + nom de la classe
data_annot = "annot"

if not os.path.exists(data_annot):
        os.makedirs(data_annot)
if not os.path.exists(os.path.join(data_annot,os.path.basename(filenameimg))):
    #sous-dossier
    os.mkdir(os.path.join(data_annot,os.path.basename(filenameimg)))

class_id = 0

#initailisation des compteurs
count_id = 0
count_part = 0
count_nb = 0
w_tot = 0
h_tot = 0

#parcourt de toutes les parties de la boite
for image_filename in sorted(os.listdir(data_directory),reverse=True):
    image_path = os.path.join(data_directory, image_filename)

    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width, channels = img.shape
    #creation d'un fichier txt pour annotation de chaque insecte dans le but de l'utiliser avec un modèle YOLO
    image_filename_txt, _ = os.path.splitext(image_filename)
    image_filename_txt = image_filename_txt + ".txt"
    output_file_path = os.path.join(os.path.join(data_annot,os.path.basename(filenameimg)), image_filename_txt)

    #conversion en gris
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cascade_classifier = cv2.CascadeClassifier('cascade.xml')
    found = cascade_classifier.detectMultiScale(img_gray,scalefact,neimin,minSize=(aa,aa))
    out = img.copy()
    
    
    #coordonées de la partie par rapport a la boite complète
    xx = (count_part//ny)
    yy = (count_part%ny)
 
    
    pxii = pxi
    pyii = pyi
    pxff = pxf
    pyff = pyf
    
    #augmentation de la taille de la zone de comptage s'il s'agit d'un bord pour le prendre en compte
    if(xx == 0): 
        pxii = 0
    if(xx == nx-1):
        pxff = 1920  
    if(yy == 0):
        pyii = 0
    if(yy == ny-1):
        pyff = 1080
    
    #rectangle comprenant la zone où il faut compter les insectes
    cv2.rectangle(out, (pxii,pyii), (pxff,pyff), (0, 0, 255), 2)

    #ouverture du fichier d'annotation
    with open(output_file_path, 'w') as output_file:
    
    #prise en compte de chaque contour avec une aire minimum
        amount_found = len(found)
        
        if amount_found != 0:
            for (x, y, w, h) in found :
                
                marge = 5
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
                
                #selection des insectes pour le comptage uniquement si le coins supérieur gauche est dans la zone de comptage (arbitraire)
                if xi > pxii and xi < pxff and yi > pyii and yi < pyff:
                    
                    #tracage d'un rectangle en bleu et incrémentation du compteur d'insectes
                    cv2.rectangle(out, (xi,yi), (xf,yf), (255, 0, 0), 2)
                    count_nb += 1
                    w_tot += w
                    h_tot += h
    
                else:
                    #tracage d'un rectange en vert sinon
                    cv2.rectangle(out, (xi,yi), (xf,yf), (0, 255, 0), 2)
               
    
                #découpe de chaque instecte détecté en une image individuelle
                insect = img[yi:yf, xi:xf] 
                #l'image de l'insecte individuel est sauvée dans un dossier avec un ID
                path = 'insect'
                if not os.path.exists(path):
                    os.makedirs(path)

                if not os.path.exists(os.path.join(path,os.path.basename(filenameimg))):
                    #sous-dossier
                    os.mkdir(os.path.join(path,os.path.basename(filenameimg)))
                
                cv2.imwrite(os.path.join(os.path.join(path,os.path.basename(filenameimg)) , 'insect'+str(count_id)+'.png'), insect)
    
                #incrementation du compteur pour l'ID de l'insecte
                count_id += 1

    #resultat
    path2 = 'part'
    if not os.path.exists(path2):
        os.makedirs(path2)
    if not os.path.exists(os.path.join(path2,os.path.basename(filenameimg))):
        #sous-dossier
        os.mkdir(os.path.join(path2,os.path.basename(filenameimg)))
    
    cv2.imwrite(os.path.join(os.path.join(path2,os.path.basename(filenameimg)), 'part'+str(count_part)+'.png'), out)
    count_part += 1
    
print('nombre : '+str(count_nb))
w_mean = w_tot/count_nb
h_mean = h_tot/count_nb

#ouvrir le fichier pour les stats
fichier_existe = 'out.csv'
with open(fichier_existe, mode='a', newline='') as fichier_csv:
    writer = csv.writer(fichier_csv,delimiter=';')

    #écrire les en-têtes si le fichier vient d'être créé
    if not fichier_existe:
        writer.writerow(["ScaleFactor","NeiMin","Path","Count","Width_mean","Height_mean","Method"])

    #écrire une nouvelle ligne avec les valeurs
    writer.writerow([scalefact,neimin,data_directory,count_nb,w_mean,h_mean,0])


