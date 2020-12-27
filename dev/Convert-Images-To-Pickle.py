# Import Dependencies
import os, sys, pickle
from PIL import Image
from numpy import asarray

folder_name = 'image-data'
pickleFolder = 'pickle-data'
pickleFileName = 'CPS-Image-Data.p'

image_folder_path = os.path.join(os.getcwd(), folder_name)

pickle_folder_path = os.path.join(os.getcwd(), pickleFolder)
if os.path.exists(pickle_folder_path) == False:
    os.mkdir(pickle_folder_path)

pickle_path = os.path.join(pickle_folder_path, pickleFileName)

if os.path.exists(image_folder_path):
    print("-------------------------------------------------------------------------------")
    print("Reading files from:", image_folder_path)
    print("-------------------------------------------------------------------------------")

    labels = []
    image_data = []


    # Determine sub folders (image classes)
    sub_folders = os.listdir(image_folder_path)
    for sub in sub_folders:
        sub_images = []
        sub_labels = []
        sub_path = os.path.join(image_folder_path, sub)
        sub_files = os.listdir(sub_path)


        # Read image files
        for sub_file in sub_files:
            filepath = os.path.join(sub_path, sub_file)
            if filepath.endswith('.png'):
                current_img = Image.open(filepath)
                sub_images.append(asarray(current_img))
                sub_labels.append(sub)
        image_data.append(sub_images)
        labels.append(sub_labels)

    # Log the status
    num_classes = len(image_data)
    class_sizes = []
    total_images = 0

    for class_size in image_data:
        class_sizes.append( len(class_size) )
        total_images += len(class_size)
    

    for i in range(len(labels)):
        print("Read {} images from the class {}.".format(class_sizes[i], labels[i][0]))
    print("-------------------------------------------------------------------------------")
    print("Read {} total images from the {} classes.".format(total_images, len(class_sizes)))
    print("-------------------------------------------------------------------------------")

    data = {
        "image-data": image_data,
        "image-labels": labels
    }

    with open(pickle_path, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

else:
    print(" ")
    print("System Error:")
    print("-------------------------------------------------------------------------------")
    print("The given path to the image folder does not exist.")
    print("The folder path should be in the same working directory as this script. ")
    print("This system expects a directory of directories, each containing png images.")
    print(" ")
    sys.exit()
