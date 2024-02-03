import numpy as np

COLOR_MAP = {
    'red': ['firebrick', 'crimson', 'coral', 'darksalmon', 'rubyred'],
    'orange': ['darkorange', 'orange', 'tomato', 'orangered'],
    'yellow': ['peru', 'gold', 'yellow', 'lightyellow', 'lemonchiffon', 'lightgoldenrodyellow', 'papayawhip', 'moccasin', 'peachpuff', 'palegoldenrod', 'khaki'],
    'green': ['lawngreen', 'chartreuse', 'limegreen', 'lime', 'forestgreen', 'green', 'darkgreen', 'greenyellow', 'yellowgreen', 'springgreen', 'mediumspringgreen', 'lightgreen', 'palegreen', 'darkseagreen', 'mediumseagreen', 'olive', 'olivedrab'],
    'blue': ['darkslategrey', 'darkslateblue', 'aqua', 'cyan', 'lightcyan', 'paleturquoise', 'aquamarine', 'turquoise', 'mediumturquoise', 'darkturquoise', 'lightseagreen', 'cadetblue', 'darkcyan', 'teal', 'lightblue', 'powderblue', 'lightsteelblue', 'skyblue', 'lightskyblue', 'deepskyblue', 'dodgerblue', 'cornflowerblue', 'steelblue', 'royalblue', 'blue', 'mediumblue', 'darkblue', 'navy', 'midnightblue', 'indigo'],
    'purple': ['lavender', 'thistle', 'plum', 'violet', 'orchid', 'fuchsia', 'magenta', 'mediumorchid', 'mediumpurple', 'blueviolet', 'darkviolet', 'darkorchid', 'darkmagenta', 'purple', 'indigo'],
    'pink': ['darksalmon', 'salmon', 'lightsalmon', 'pink', 'lightpink', 'hotpink', 'deeppink', 'palevioletred', 'mediumvioletred', 'indianred'],
    'brown': ['lightcoral', 'crimson', 'firebrick', 'darkred', 'red', 'snow', 'lightcoral', 'brown', 'firebrick', 'darkred', 'mistyrose', 'salmon', 'tomato', 'darksalmon', 'coral', 'orangered', 'lightcoral', 'sienna', 'seashell', 'chocolate', 'sandybrown', 'peachpuff', 'linen', 'bisque', 'darkorange', 'burlywood', 'antiquewhite', 'tan', 'navajowhite', 'blanchedalmond', 'papayawhip', 'moccasin', 'orange', 'wheat', 'oldlace', 'floralwhite', 'darkgoldenrod', 'goldenrod', 'cornsilk', 'gold', 'lemonchiffon', 'khaki', 'palegoldenrod', 'darkkhaki', 'ivory', 'beige', 'lightyellow', 'lightgoldenrodyellow', 'yellow', 'olive', 'yellowgreen', 'darkolivegreen', 'greenyellow', 'chartreuse', 'lawngreen', 'darkgreen', 'green', 'forestgreen', 'lime', 'limegreen', 'palegreen', 'lightgreen', 'mediumspringgreen', 'springgreen', 'mediumseagreen', 'olivedrab', 'darkolivegreen'],
    'black': ['gainsboro', 'slategray', 'black'],
    'white': ['white', 'dimgray', 'snow', 'honeydew', 'mintcream', 'azure', 'aliceblue', 'ghostwhite', 'whitesmoke', 'seashell', 'beige', 'oldlace', 'floralwhite', 'ivory', 'antiquewhite', 'linen', 'lavenderblush', 'mistyrose'],
    'gray': ['lightslategray', 'gainsboro', 'lightgray', 'darkgray', 'gray', 'slategray', 'darkslategray', 'darkkhaki'],
    'beige': ['beige', 'rosybrown', 'bisque', 'blanchedalmond', 'wheat', 'cornsilk', 'lemonchiffon', 'lightgoldenrodyellow', 'lightyellow', 'sienna', 'chocolate', 'sandybrown', 'burlywood', 'tan', 'moccasin', 'navajowhite', 'peachpuff', 'palegoldenrod', 'khaki', 'darkkhaki'],
    'turquoise': ['aqua', 'seagreen', 'cyan', 'lightcyan', 'paleturquoise', 'aquamarine', 'turquoise', 'mediumturquoise', 'darkturquoise', 'lightseagreen', 'cadetblue', 'darkcyan', 'teal'],
    'indigo': ['indigo', 'midnightblue', 'navy', 'darkblue', 'mediumblue', 'blue', 'royalblue', 'cornflowerblue', 'lightsteelblue', 'steelblue', 'dodgerblue', 'deepskyblue', 'lightskyblue', 'skyblue', 'lightblue', 'powderblue', 'aliceblue', 'ghostwhite'],
    'magenta': ['fuchsia', 'magenta', 'violet', 'plum', 'orchid', 'mediumorchid', 'darkorchid', 'darkviolet', 'blueviolet', 'purple', 'mediumpurple', 'thistle'],
    'gold': ['gold', 'yellow', 'lightyellow', 'lemonchiffon', 'lightgoldenrodyellow', 'papayawhip', 'moccasin', 'peachpuff', 'palegoldenrod', 'khaki', 'darkkhaki'],
    'silver': ['gainsboro', 'silver', 'gray', 'slategray'],
    'cupper': ['copper'],
    'rubyred': ['rubyred', 'saddlebrown', 'maroon'],
    'olive': ['olive', 'darkolivegreen', 'olivedrab']
}

COLOR_LIST = {
    'red':(160,20,20),
    'Orange':(255,165,0),
    'Yellow':(200,150,40),
    'Green':(71,91,31),
    'Blue':(20,20,160),
    'Purple':(128,0,128),
    'Pink':(200,157,179),
    'Brown':(82,60,43),
    'Black':(20,20,20),
    'White':(190,190,190),
    'Gray':(100,100,100),
    'Beige':(160,125,93),
    'Turquoise':(90, 142, 156),
    'Indigo':(36,33,78),
    'Magenta':(117,30,73),
    'Gold':(207, 173, 6),
    'Silver':(180, 180, 180),
    'Copper':(183, 115, 51),
    'Rubyred':(93, 25, 35),
    'Olive':(106, 100, 42)
}

def get_euc_distance(color):
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

    return closest_color
