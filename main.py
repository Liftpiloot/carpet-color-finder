from rembg import remove
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import io
import os
from color import get_colour_name
from color_map import COLOR_MAP
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Let user select image file from explorer

def select_images_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="open image folder")
    return folder_path

def get_image_files(folder_path):
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return image_files

# Let user select folder to save image file
def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="select folder to save image")
    return folder_path

#remove background from selected image

def remove_bg(input_path):
    with open(input_path, "rb") as i:
        input = i.read()
        output = remove(input)
        return output

def get_output_filename(image):
    # Get the dimensions (width, height, and depth) of the image
    w, h, d = tuple(image.shape)

    # Reshape the image into a 2D array, where each row represents a pixel
    pixel = np.reshape(image, (w * h, d))
    n_colors = 20

    # Create a KMeans model with the specified number of clusters and fit it to the pixels
    model = KMeans(n_clusters=n_colors, random_state=42).fit(pixel)

    # Get the cluster centers (representing colors) from the model
    colour_palette = np.uint8(model.cluster_centers_)

    # plot colour palette
    plt.imshow([colour_palette])
    for i, colour in enumerate(colour_palette):
        name, key_name = get_colour_name(colour[:3])
        # Convert the RGBA array to an RGB tuple
        rgb_tuple = tuple(colour[:3] / 255)
        plt.text(0, i, name + ", " + key_name, fontsize=12, color=rgb_tuple, ha='left', va='center')
    plt.show()


    # Get the color name of each cluster center
    colour_names = []
    for colour in colour_palette:
        name, key_name = get_colour_name(colour[:3])
        print(colour[:3], name, key_name)
        color = key_name
        # append color name if it is not in the list
        if color not in colour_names:
            colour_names.append(color)

    filename = "_".join(colour_names) + ".png"
    return filename

def get_rgb_values(image):
    width, height = image.size
    channels = len(image.getdata()[0])
    data = np.array(image.getdata()).reshape((height, width, channels))
    if channels == 4:
        rgb = data[:,:,:3]  # Exclude the alpha channel
        alpha = data[:,:,3]  # Get the alpha channel
    else:
        rgb = data
        alpha = None
    return rgb, alpha


def main():
    images_folder = select_images_folder()
    image_files = get_image_files(images_folder)
    output_folder = select_output_folder()
    for i, image_file in enumerate(image_files):
        transparent = remove_bg(image_file)
        image = Image.open(io.BytesIO(transparent))

        image_np = np.array(image)

        output_filename = get_output_filename(image_np)  # Pass both rgb and alpha to get_output_filename
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "wb") as o:
            o.write(transparent)

if __name__ == "__main__":
    main()
