import cv2
from matplotlib import pyplot as plt

#ouverture de l'image
img = cv2.imread('entomo_X12_Y06_Z100.bmp')
#conversion
img_rgb2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

cascade_classifier = cv2.CascadeClassifier('cascade.xml')
found = cascade_classifier.detectMultiScale(img_rgb2,1.4,3)

amount_found = len(found)

if amount_found != 0:
	for (x, y, width, height) in found:
		cv2.rectangle(img_rgb, (x, y),
					(x + height, y + width),
					(0, 255, 0), 2)
		
cv2.imwrite('haarf.png',img_rgb)
