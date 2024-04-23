# Analysis of Entomological Boxes: Insect Detection and Classification

## ROI.py (Select Regions of Interest of an Image)

1. Use the Python command with the image you want to extract ROIs as an argument (e.g., "python ROI.py GxABT_single.bmp").
2. Select a ROI on the image with your mouse.
3. Press ENTER or SPACE to save the ROI.
4. Repeat steps 2 and 3 as long as needed.
5. Press ESC to quit.
6. Annotation txt file is saved in the "Annotation_txt" folder, and individual images are saved in a sub-folder in the "Individuals_images" folder.

## crop.py (Reconstruct a Box from its Parts)

1. Use the Python command with: (e.g., "python crop.py GxABT_box 500 240")
    - Path to the folder containing the images of the box to be reconstructed
    - Number of pixels to crop on horizontal sides
    - Number of pixels to crop on vertical sides
2. The reconstructed box will be saved in the current directory.

## parameters_chooser.py (Contrast Detection to Get the Number of Insects of an Entomological Box)

1. Use the Python command to launch the GUI: "python parameters_chooser.py".
2. Select an image to visualize with the button: "Choose image".
3. Adjust parameters with cursors.
4. (Optional) Save parameters to a CSV file with the button: "Save parameters".
5. (Optional) Load parameters from a CSV file with the button: "Load parameters".
6. Start counting for a box on parts (GxABT method) with the button: "Start counting (box parts)".
    - OR -
    Start counting for a single image (Africamuseum method) with the button: "Start counting (complete box)".
7. Annotation txt files are saved in the "Annotation_txt" folder, individual insects are saved in a sub-folder in the "Insects" folder, and annotated images with bounding boxes are saved in a sub-folder in the "Parts" folder (GxABT) or "Out" folder (Africamuseum). Parameters, number, width mean, and height mean are saved in the "out.csv" file.

## gembloux_method_haar.py and africamuseum_method_haar.py (Cascade Detection to Get the Number of Insects of an Entomological Box)

1. Use the Python command with: (e.g., "python gembloux_method_haar.py 1.2 3 3 GxABT_box cascade.xml ")
    - Scale Factor
    - Minimum number of neighbors
    - Minimum size of detection
    - Path to the folder containing the images of the box (GxABT) or to the single image (Africamuseum)
    - Path to the cascade XML file
2. Annotation txt files are saved in the "Annotation_txt" folder, individual insects are saved in a sub-folder in the "Insects" folder, and annotated images with bounding boxes are saved in a sub-folder in the "Parts" folder (GxABT) or "Out" folder (Africamuseum). Parameters, number, width mean, and height mean are saved in the "out.csv" file.

## yolo_custom.ipynb (Detection using YOLO to Get the Number of Insects of an Entomological Box)

Follow the instructions in the Jupyter notebook.

## cnn.ipynb (Classification with a CNN)

Follow the instructions in the Jupyter notebook.

## svm.ipynb (Classification with a SVM)

Follow the instructions in the Jupyter notebook.
