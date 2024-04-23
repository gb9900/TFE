# Analyse des boîtes entomologiques : détection et classification des insectes

## ROI.py (sélection des ROI d'une image) :
1. Utilisez la commande python avec l'image dont vous voulez extraire les ROI en argument (ex. "python ROI.py GxABT_single.bmp")
2. Sélectionnez une ROI sur l'image avec votre souris
3. Appuyez sur ENTER ou ESPACE pour enregistrer la ROI
4. Répétez les étapes 2) et 3) autant que nécessaire
5. Appuyez sur ÉCHAP pour quitter
6. Le fichier txt d'annotation est enregistré dans le dossier "Annotation_txt" et les images individuelles sont enregistrées dans un sous-dossier du dossier "Individuals_images"

## crop.py (reconstruction d'une boîte à partir de ses parties) :
1. Utilisez la commande python avec : (ex. "python crop.py GxABT_box 500 240")
   a) Chemin vers le dossier contenant les images de la boîte à reconstruire
   b) Nombre de pixels à rogner sur les côtés horizontaux
   c) Nombre de pixels à rogner sur les côtés verticaux
2. La boîte reconstruite sera enregistrée dans le répertoire actuel

## parameters_chooser.py (détection du contraste pour obtenir le nombre d'insectes d'une boîte entomologique) :
1. Utilisez la commande python pour lancer l'interface graphique : "python parameters_chooser.py"
2. Sélectionnez une image à visualiser avec le bouton : "Choisir une image"
3. Ajustez les paramètres avec les curseurs
4. (optionnel) Enregistrez les paramètres dans un fichier csv avec le bouton : "Enregistrer les paramètres"
5. (optionnel) Chargez les paramètres à partir d'un fichier csv avec le bouton : "Charger les paramètres"
6. Commencez le décompte pour une boîte sur des parties (méthode GxABT) avec le bouton : "Commencer le décompte (parties de la boîte)"
6bis. Commencez le décompte pour une seule image (méthode Africamuseum) avec le bouton : "Commencer le décompte (boîte complète)"
7. Les fichiers txt d'annotation sont enregistrés dans le dossier "Annotation_txt", les insectes individuels sont enregistrés dans un sous-dossier du dossier "Insects" et les images annotées avec des cadres englobants sont enregistrées dans un sous-dossier du dossier "Parts" (GxABT) ou "Out" (Africamuseum). Les paramètres, le nombre, la largeur moyenne et la hauteur moyenne sont enregistrés dans le fichier "out.csv"

## gembloux_method_haar.py et africamuseum_method_haar.py (détection de cascade pour obtenir le nombre d'insectes d'une boîte entomologique) :
1. Utilisez la commande python avec : (ex. "python gembloux_method_haar.py 1.2 3 3 GxABT_box cascade.xml ")
   a) Facteur d'échelle
   b) Nombre minimum de voisins
   c) Taille minimum de détection
   d) Chemin vers le dossier contenant les images de la boîte (GxABT) ou vers l'image unique (Africamuseum)
   e) Chemin vers le fichier xml en cascade
2. Les fichiers txt d'annotation sont enregistrés dans le dossier "Annotation_txt", les insectes individuels sont enregistrés dans un sous-dossier du dossier "Insects" et les images annotées avec des cadres englobants sont enregistrées dans un sous-dossier du dossier "Parts" (GxABT) ou "Out" (Africamuseum). Les paramètres, le nombre, la largeur moyenne et la hauteur moyenne sont enregistrés dans le fichier "out.csv"

## yolo_custom.ipynb (détection en utilisant YOLO pour obtenir le nombre d'insectes d'une boîte entomologique) : suivez les instructions du cahier Jupiter
## cnn.ipynb (classification avec un CNN) : suivez les instructions du cahier Jupiter
## svm.ipynb (classification avec un SVM) : suivez les instructions du cahier Jupiter
