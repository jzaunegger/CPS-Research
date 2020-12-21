# Import dependencies
from PIL import Image, ImageDraw, ImageFont
import os, sys
from HelperFunctions import *

# Initalize Parameters
images_folder = 'image-data'
output_folder = 'visulization-images'
img_sample_count = 5

img_padding = 10
img_size = [10, 20]
text_size = 24
resize_factor = 10
resample_method = Image.LANCZOS
background_color = (255, 255, 255)
text_color = (0, 0, 0)
text_font = 'OpenSans-Regular.ttf'

imgs = {}
category_names = []
font_path = os.path.join(os.getcwd(), os.path.join('fonts', text_font))
sys_font = ImageFont.truetype(font_path, text_size)

def create_complete_visualization(path_name, out_file_name):
    if os.path.exists(path_name):
        sub_files = os.listdir(path_name)

        # Read in the images
        sample_images = []
        for sub_file in sub_files:
            sub_file_path = os.path.join(path_name, sub_file)
            sample_images.append(Image.open(sub_file_path))

        # Determine the new image size
        widths, heights = zip(*(i.size for i in sample_images))
        total_width = max(widths)
        total_height = sum(heights)

        # Create new Image
        new_image = Image.new('RGB', (total_width, total_height), color=background_color)

        # Plot the sub images
        y_off = 0
        for sample in sample_images:
            new_image.paste(sample, (0, y_off))
            y_off += sample.size[1]

        # Save the image

        if out_file_name.endswith('.png') == False:
            print(" ")
            print("System Error:")
            print("-------------------------------------------------------------------------------")
            print(out_file_name)
            print("is not a valid image format. Please ensure the file name ends ")
            print("with a .png extension")
            print(" ")
            sys.exit()


        out_file_path = os.path.join(path_name, out_file_name)
        new_image.save(out_file_path)
        print("Successfully generated {} and saved it to {}".format(out_file_name, out_file_path))


    else:
        print(" ")
        print("System Error:")
        print("-------------------------------------------------------------------------------")
        print("The given path to the image folder does not exist.")
        print(" ")
        sys.exit()



def create_category_visualizations(imgs, output_path):

    # Process the thumbnail image for each classification
    text_width = longestCatName(category_names) * text_size
    print(" ")
    print("Visualizing Images")
    print("---------------------------------------------------")
    for key in imgs:
        image_name = key + "_visulization.png"
        new_img_path = os.path.join(output_path, image_name)
        img_paths = imgs[key]

        print("Visualizing", key)

        # Read the images
        images = []
        for x in img_paths:
            temp_img = Image.open(x)

            # Determine the size, and what the new size will be
            img_width, img_height = temp_img.size
            img_width = img_width * resize_factor
            img_height = img_height * resize_factor

            # Resize and append the new image
            resized = temp_img.resize((img_width, img_height), resample=resample_method)
            images.append(resized)

        # Get the total image width, and the height
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        # Account for gaps between images
        total_width = total_width + ((img_sample_count+1) * img_padding)
        total_height = max_height + (img_padding * 2) + text_size * 2

        # Create new image, and current draw, and get the current category
        new_image = Image.new('RGB', (total_width, total_height), color=background_color)
        current_draw = ImageDraw.Draw(new_image)
        current_category = formatCategoryName(key)

        # Display the sub-images
        x_offset = img_padding
        for img in images:
            new_image.paste(img, (x_offset, img_padding + text_size * 2))
            x_offset += img.size[0] + img_padding
        
        # Draw Label
        text_location = (img_padding, img_padding + text_size - text_size)
        current_draw.text(text_location, current_category, fill=text_color, font=sys_font)
        
        # Save Image
        new_image.save(new_img_path)


# Check if input folder exists
images_path = os.path.join(os.getcwd(), images_folder)
if(os.path.exists(images_path)):
    sub_dirs = os.listdir(images_path)

    imgs = {}
    for sub_dir in sub_dirs:
        category_names.append(sub_dir)
        sub_path = os.path.join(images_path, sub_dir)
        sub_files = os.listdir(sub_path)

        img_paths = []
        for sub_file in sub_files[0:img_sample_count]:
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

create_category_visualizations(imgs, output_path)
create_complete_visualization(output_path, 'CPS-Data-Image-Samples.png')


print("---------------------------------------------------")
print(" ")