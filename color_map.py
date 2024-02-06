import numpy as np

COLOR_LIST = {
    'red':(160,20,20),
    'Orange':(255,165,0),
    'Yellow':(200,150,40),
    'Green':(71,91,31),
    'Blue':(20,20,160),
    'Purple':(128,0,128),
    'Pink':(200,157,179),
    'Brown':(127,66,43),
    'Black':(20,20,20),
    'White':(200,200,200),
    'Gray':(100,100,100),
    'Beige':(160,125,93),
    'Turquoise':(90, 142, 156),
    'Indigo':(36,33,78),
    'Magenta':(117,30,73),
    'Gold':(207, 173, 6),
    'Silver':(190, 190, 190),
    'Copper':(183, 115, 51),
    'Rubyred':(93, 25, 35),
    'Olive':(106, 100, 42)
}

def get_closest_color(color):
    min_dist = float('inf')
    closest_color = None

    # Convert RGB to numpy array for easier computation
    rgb_np = np.array(color)

    for color_name, color_rgb in COLOR_LIST.items():
        # Convert color RGB values to numpy array
        color_rgb_np = np.array(color_rgb)

        # Calculate Euclidean distance between rgb and color_rgb
        distance = np.linalg.norm(rgb_np - color_rgb_np)

        # Update the closest color if distance is smaller
        if distance < min_dist:
            min_dist = distance
            closest_color = color_name

    return closest_color, int(min_dist)
