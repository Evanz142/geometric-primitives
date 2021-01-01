#import matplotlib.image as mpimg
#import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageChops
import math

# ──────────────────── RMSE FUNCTION ────────────────────

def rmseFunction(path1, path2):
    im1 = Image.open(path1)
    im2 = Image.open(path2)
    #im1.show() # Opens up the image using Windows Photos (for me)
    err = np.asarray(ImageChops.difference(im1, im2)) / 255 
    err = math.sqrt(np.mean(np.square(err)))
    return err

"""
# This code snippet succesfully used the machine learning image-similiarity API to compare two images and return
#      their similarity. It works, but it isn't fast enough to process thousands of requests without taking hours.

import requests
r = requests.post(
    "https://api.deepai.org/api/image-similarity",
    files={
        'image1': open('C:/Users/evman/Documents/GitHub/geometric-primitives/images/image1.jpg', 'rb'),
        'image2': open('C:/Users/evman/Documents/GitHub/geometric-primitives/images/image1.jpg', 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())
"""


# Example of using the rmse function to find the error between two images.
"""
path1 = "images/image1.png"
path2 = "images/image2.png"
err = rmseFunction(path1, path2)
print(err)
"""

# ──────────────────── CANVAS SETUP ────────────────────

original = Image.open("images/image1.png") # Opening the original image

averageOriginalColor = original.resize((1,1)).getpixel((0,0)) # Gets the average color of the original image

# Creates a blank canvas which will be the start of the geometric primitive image
#   first parameter specifies the 'mode' of the new image (RGB)
#   second parameter specifies the size of the canvas (a tuple containing the width and height of the original image)
#   third parameter specifies the starting color of the canvas (the average color of the original image)
canvas = Image.new("RGB", original.size, averageOriginalColor)

#canvas.show() # Shows the starting canvas