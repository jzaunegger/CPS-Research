# Import dependencies
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os, sys

# Initalize Parameters
images_folder = 'image-data'
output_folder = 'visulization-images'
img_sample_count = 5

imgs = {}

# Check if input folder exists
images_path = os.path.join(os.getcwd(), images_folder)
if(os.path.exists(images_path)):
    sub_dirs = os.listdir(images_path)

    imgs = {}
    for sub_dir in sub_dirs:
        sub_path = os.path.join(images_path, sub_dir)
        sub_files = os.listdir(sub_path)

        img_paths = []
        for sub_file in sub_files:
            img_paths.append(os.path.join(sub_path, sub_file))

        imgs[sub_dir] = img_paths

# Throw Error if the image folder does not exist
else:
    print(" ")
    print("System Error:")
    print("-------------------------------------------------------------------------------")
    print("The given path to the image folder does not exist. The image folder must be in ")
    print("the same working directory as this script.")
    print(" ")
    sys.exit()

# Create output folder if none exists
output_path = os.path.join(os.getcwd(), output_folder)
if(os.path.exists(output_path) == False):
    os.mkdir(output_path)  

# Iterate through the dict object
for key in imgs:
    image_name = key + "-visulization"
    img_paths = imgs[key][0:img_sample_count]
    
    width = 5
    height = 1

    figure = plt.figure(figsize=(10, 10))

    counter = 1
    for img_path in img_paths[0:6]:
        image = mpimg.imread(img_path)
        figure.add_subplot(counter, 1, 1)
        plt.imshow(image)
        counter += 1
    plt.show()