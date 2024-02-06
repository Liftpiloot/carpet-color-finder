import shutil

from matplotlib import pyplot as plt
from rembg import remove
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import io
import os

import color_map
from sklearn.cluster import KMeans


# Let user select image file from explorer
def select_images_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder with images to process")
    return folder_path


# Get all image files from selected folder
def get_image_files(folder_path):
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                   f.endswith(('.png', '.jpg', '.jpeg'))]
    return image_files


# Let user select folder to save image file
def select_output_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder to save images to")
    return folder_path


# remove background from selected image
def remove_bg(input_path):
    with open(input_path, "rb") as i:
        input = i.read()
        output = remove(input)
        return output


def get_color_palette(image, n_colors):
    """
    Get the colour palette of an image using KMeans clustering
    :param image: input image
    :param n_colors: number of clusters (i.e., colours) to find
    :return: the colour palette
    """
    # Get the dimensions (width, height, and depth) of the image
    w, h, d = tuple(image.shape)
    # Reshape the image into a 2D array, where each row represents a pixel
    pixel = np.reshape(image, (w * h, d))
    # If the image has an alpha channel (i.e., it's an RGBA image), remove transparent pixels
    if d == 4:
        pixel = pixel[pixel[:, 3] > 200]
    # Create a KMeans model with the specified number of clusters and fit it to the pixels
    model = KMeans(n_clusters=n_colors, random_state=42).fit(pixel)
    # Get the cluster centers (representing colors) from the model
    colour_palette = np.uint8(model.cluster_centers_)
    return colour_palette


# Plot the colour palette with the color names
def plot_pallete(colour_palette, n_colors=10):
    # plot colour palette
    fig, ax = plt.subplots()
    plt.imshow([colour_palette])
    for i, colour in enumerate(colour_palette):
        colour_normal = colour / 255
        ax.add_patch(plt.Rectangle((0, i), 1, 1, color=colour_normal))
        name, distance = color_map.get_closest_color(colour[:3])
        ax.text(1.2, i + 0.5, str(colour) + ": " + name + ": " + str(distance), va='center')

        # Set limits and labels
    ax.set_xlim(0, 2)
    ax.set_ylim(0, n_colors)
    ax.set_axis_off()
    plt.show()


def get_filename_euc(image, filename, n_colors=10, min_distance=20):
    """
    Get the filename based on the color palette of the image
    :param image: input    :param filename:  filename
    :param n_colors: number of clusters (i.e., colours) to find
    :return: filename plus color names
    """
    # Get the cluster centers (representing colors) from the model
    colour_palette = get_color_palette(image, n_colors)
    # Plot the colour palette (optional)
    # plot_pallete(colour_palette, n_colors)

    # Get the color name of each cluster center using the Euclidean distance
    colour_names = []
    for colour in colour_palette:
        color_name, distance = color_map.get_closest_color(colour[:3])
        # append color name if it is not in the list
        if color_name not in colour_names:
            if distance < min_distance:
                colour_names.append(color_name)
    output_filename = "_".join(colour_names)
    return filename + "_" + output_filename


# Display a message box to show when the process is done
def show_done_message(store_location):
    root = tk.Tk()
    root.title("Done")
    root.geometry("800x300")
    label = tk.Label(root, text=f"Done, results: {store_location}")
    label.pack()
    button = tk.Button(root, text="OK", command=root.destroy)
    button.pack()
    root.wait_window()


# Prompt the user to enter high or low
def open_selection_window():
    global high_low
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    high_low = tk.simpledialog.askstring("High or Low", "Enter High or Low:", parent=root)
    root.destroy()  # Destroy the root window


# 1. Prompt the user to select the input folder
# 2. Prompt the user to select the output folder
# 3. Prompt the user to enter high or low
# 4. Images are processed and saved in the output folder
# 5. A message box is displayed to show when the process is done
def main():
    # Let user select image folder
    images_folder = select_images_folder()
    image_files = get_image_files(images_folder)
    output_folder = select_output_folder()

    # select high or low
    open_selection_window()
    for i, image_file in enumerate(image_files):
        # remove background from image
        image = remove_bg(image_file)
        image = Image.open(io.BytesIO(image))
        image_np = np.array(image)
        filename = os.path.basename(image_file)
        # remove file extension
        filename = filename.split(".")[0]
        # append -t~high or -t~low to the end of filename
        filename = filename + "-t~" + high_low
        # append -c~ to the end of filename
        filename = filename + "-c~"

        # Calculate euclidean distance and map it to the closest color (more accurate). n_colors is the number of
        # clusters, min_distance is the minimum distance to be considered as a color, play around with these values
        # to get the best result
        output_filename_euc = get_filename_euc(image_np, filename, n_colors=17, min_distance=30)
        output_path_euc = os.path.join(output_folder, output_filename_euc) + ".jpg"
        shutil.copy(image_file, output_path_euc)

        # Save transparent image as well
        # output_path_trans = os.path.join(output_folder, output_filename_euc + ".png")
        # image.save(output_path_trans, "PNG")

    show_done_message(output_folder)


# Run the main function
if __name__ == "__main__":
    main()
