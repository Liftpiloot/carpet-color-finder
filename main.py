import shutil

from matplotlib import colors
from rembg import remove
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import io
import os

import color_map
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

def get_color_palette(image, n_colors):
    # Get the dimensions (width, height, and depth) of the image
    w, h, d = tuple(image.shape)
    # Reshape the image into a 2D array, where each row represents a pixel
    pixel = np.reshape(image, (w * h, d))
    # If the image has an alpha channel (i.e., it's a RGBA image), remove transparent pixels
    if d == 4:
        pixel = pixel[pixel[:, 3] > 200]
    # Create a KMeans model with the specified number of clusters and fit it to the pixels
    model = KMeans(n_clusters=n_colors, random_state=42).fit(pixel)
    # Get the cluster centers (representing colors) from the model
    colour_palette = np.uint8(model.cluster_centers_)
    return colour_palette

def get_output_filename(image, filename, n_colors=10):
    # Get the cluster centers (representing colors) from the model
    colour_palette = get_color_palette(image, n_colors)

    # Plot the colour palette
    plot_pallete(colour_palette, n_colors)

    # Get the color name of each cluster center
    colour_names = []
    for colour in colour_palette:
        name, key_name = get_colour_name(colour[:3])
        color = key_name
        # append color name if it is not in the list
        if color not in colour_names:
            colour_names.append(color)
    output_filename = "_".join(colour_names) + ".jpg"
    return "col" + "_" + output_filename


def plot_pallete(colour_palette, n_colors=10, euclidean=False):
    # plot colour palette
    fig, ax = plt.subplots()
    plt.imshow([colour_palette])
    for i, colour in enumerate(colour_palette):
        colour_normal = colour / 255
        ax.add_patch(plt.Rectangle((0, i), 1, 1, color=colour_normal))
        if euclidean:
            name = color_map.get_euc_distance(colour[:3])
        else:
            act_name, name = get_colour_name(colour[:3])
        ax.text(1.2, i + 0.5, str(colour) + ": " + name + ": " + name, va='center')

        # Set limits and labels
    ax.set_xlim(0, 2)
    ax.set_ylim(0, n_colors)
    ax.set_axis_off()
    plt.show()


def get_filename_euc(image, filename, n_colors=10):
    # Get the cluster centers (representing colors) from the model
    colour_palette = get_color_palette(image, n_colors)

    # Plot the colour palette
    plot_pallete(colour_palette, n_colors, euclidean=True)

    # Get the color name of each cluster center
    colour_names = []
    for colour in colour_palette:
        key_name = color_map.get_euc_distance(colour[:3])
        color = key_name
        # append color name if it is not in the list
        if color not in colour_names:
            colour_names.append(color)
    output_filename = "_".join(colour_names)
    return filename + "_" + output_filename


def show_done_message(store_location):
    root = tk.Tk()
    root.title("Done")
    root.geometry("800x300")
    label = tk.Label(root, text=f"Done with store location: {store_location}")
    label.pack()
    button = tk.Button(root, text="OK", command=root.destroy)
    button.pack()
    root.wait_window()


def open_selection_window():
    global high_low
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    high_low = tk.simpledialog.askstring("High or Low", "Enter High or Low:", parent=root)
    root.destroy()  # Destroy the root window


def main():
    images_folder = select_images_folder()
    image_files = get_image_files(images_folder)
    output_folder = select_output_folder()
    # open selection window
    open_selection_window()
    for i, image_file in enumerate(image_files):
        transparent = remove_bg(image_file)
        image = Image.open(io.BytesIO(transparent))
        image_np = np.array(image)
        filename = os.path.basename(image_file)
        # remove file extension
        filename = filename.split(".")[0]
        # append -t~high or -t~low to the end of filename
        filename = filename + "-t~" + high_low
        # append -c~ to the end of filename
        filename = filename + "-c~"

        # The hard way
        #output_filename = get_output_filename(image_np, filename)  # Pass both rgb and alpha to get_output_filename
        #output_path = os.path.join(output_folder ,output_filename)
        #shutil.copy(image_file, output_path)

        # The easy way
        output_filename_euc = get_filename_euc(image_np, filename, n_colors=7)
        output_path_euc = os.path.join(output_folder, output_filename_euc) + ".jpg"
        output_path_trans = os.path.join(output_folder, output_filename_euc + ".png")
        shutil.copy(image_file, output_path_euc)

        # Save transparent image
        image.save(output_path_trans, "PNG")


    show_done_message(output_folder)


if __name__ == "__main__":
    main()
