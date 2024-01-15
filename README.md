# Analysis of entomological boxes: insect detection and classification
ROI.py (select ROIs of an image) :
    1) Use python command with the image you want to extract ROIs as argument (ex. "python ROI.py GxABT_single.bmp")
    2) Select a ROI on the image with your mouse
    3) Press ENTER or SPACE to save ROI
    4) Repeat 2) and 3) as long as you like
    5) Press ESC to quit
    6) Annotation txt file is saved on "Annotation_txt" folder and individuals images are saved on a sub-folder on "Individuals_images" folder

crop.py (reconstruct a box form its parts):
    1) Use python command with : (ex. "python crop.py GxABT_box 500 240")
        a) Path to the folder containing the images of the box to be reconstructed
        b) Number of pixels to crop on horizontal sides
        c) Number of pixels to crop on vertical sides
    2) Reconstructed box will be saved on the current directory

parameters_chooser.py (contrast detection to get the number of insects of an entomological box) : 
    1) Use python command to launch GUI : "python parameters_chooser.py"
    2) Select an image to visualize with the button : "Choose image"
    3) Adjust parameters with cursors
    4) (optional) Save parameters on a csv file with the button : "Save parameters"
    5) (optional) Load parameters from a csv file with the button : "Load parameters"
    6) Start counting for a box on parts (GxABT method) with the button : "Start counting (box parts)"
    6bis) Start counting for a single image (Africamuseum method) with the button : "Start counting (complete box)"
    7) Annotation txt files are saved on "Annotation_txt" folder, individuals insects are saved on a sub-folder on "Insects" folder and annoted images with bounding boxes are saved on a sub-folder on "Parts" folder (GxABT) or "Out" folder (Africamuseum). Parameters, number, width mean and height mean are saved on "out.csv" file

gembloux_method_haar.py and africamuseum_method_haar.py (cascade detection to get the number of insects of an entomological box) :
    1) Use python command with : (ex. "python gembloux_method_haar.py 1.2 3 3 GxABT_box cascade.xml ")
        a) Scale Factor
        b) Minimum number of neighbors
        c) Minimum size of detection
        d) Path to the folder containing the images of the box (GxABT) or to the single image (Africamuseum)
        e) Path to the cascade xml file
    2)  Annotation txt files are saved on "Annotation_txt" folder, individuals insects are saved on a sub-folder on "Insects" folder and annoted images with bounding boxes are saved on a sub-folder on "Parts" folder (GxABT) or "Out" folder (Africamuseum). Parameters, number, width mean and height mean are saved on "out.csv" file

yolo_custom.ipynb (detection using YOLO to get the number of insects of an entomological box) : follow jupiter notebook instructions
cnn.ipynb (classification with a CNN) : follow jupiter notebook instructions
svm.ipynb (classification with a SVM) : follow jupiter notebook instructions
