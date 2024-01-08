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
#creation d'un fichier txt pour annotation de chaque insecte dans le but de l'utiliser avec un modèle YOLO
image_filename_txt, _ = os.path.splitext(image_path)
image_filename_txt = image_filename_txt + ".txt"

#conversion en gris
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cascade_classifier = cv2.CascadeClassifier('cascade.xml')
found = cascade_classifier.detectMultiScale(img_gray,scalefact,neimin,minSize=(aa,aa))



#copie et recuperation des dimensions pour les statistiques
out = img.copy()



#ouverture du fichier d'annotation
with open(image_filename_txt, 'w') as output_file:

#prise en compte de chaque contour avec une aire minimum
    amount_found = len(found)
    
    if amount_found != 0:
        for (x, y, w, h) in found :
    
                
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
            cv2.rectangle(out, (xi,yi), (xf,yf), (255, 0, 0), 2)
            count_nb += 1
            w_tot += w
            h_tot += h
    
     
    
            #découpe de chaque instecte détecté en une image individuelle
            insect = img[yi:yf, xi:xf] 
            #l'image de l'insecte individuel est sauvée dans un dossier avec un ID
            if not os.path.exists('insect'):
                os.makedirs('insect')
            path = 'insect'
            cv2.imwrite(os.path.join(path , 'insect'+str(count_nb)+'.png'), insect)


#resultat
cv2.imwrite(os.path.join('out.png'), out)
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
    writer.writerow([scalefact,neimin,image_path,count_nb,w_mean,h_mean,0])

