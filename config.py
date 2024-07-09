# This file MUST be configured in order for the code to run properly

# Make sure you put all your input images into an 'assets' folder. 
# Each layer (or category) of images must be put in a folder of its own.

# CONFIG is an array of objects where each object represents a layer
# THESE LAYERS MUST BE ORDERED.

# Each layer needs to specify the following
# 1. id: A number representing a particular layer
# 2. name: The name of the layer. Does not necessarily have to be the same as the directory name containing the layer images.
# 3. directory: The folder inside assets that contain traits for the particular layer
# 4. required: If the particular layer is required (True) or optional (False). The first layer must always be set to true.
# 5. rarity_weights: Denotes the rarity distribution of traits. It can take on three types of values.
#       - None: This makes all the traits defined in the layer equally rare (or common)
#       - "random": Assigns rarity weights at random. 
#       - array: An array of numbers where each number represents a weight. 
#                If required is True, this array must be equal to the number of images in the layer directory. The first number is  the weight of the first image (in alphabetical order) and so on...
#                If required is False, this array must be equal to one plus the number of images in the layer directory. The first number is the weight of having no image at all for this layer. The second number is the weight of the first image and so on...

# Be sure to check out the tutorial in the README for more details.                

CONFIG = [
    {
        'id': 1,
        'name': 'background',
        'directory': 'Layer 1 Background (Updated)',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 2,
        'name': 'horns1',
        'directory': 'Layer 2 Horns #1 (Updated)',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 3,
        'name': 'wings',
        'directory': 'Layer 3 Wings',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 4,
        'name': 'skin',
        'directory': 'Layer 4 Skin (Updated)',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 5,
        'name': 'hats',
        'directory': 'Layer 5 Hats (Updated)',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 6,
        'name': 'horns2',
        'directory': 'Layer 6 Horns #2 (Updated)',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 7,
        'name': 'clothes',
        'directory': 'Layer 7 Clothes',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 8,
        'name': 'mouth',
        'directory': 'Layer 8 Mouth (Updated)',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 9,
        'name': 'eyes',
        'directory': 'Layer 9 Eyes (Updated)',
        'required': True,
        'rarity_weights': None,
    },
]
