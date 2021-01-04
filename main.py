#import matplotlib.image as mpimg
#import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageChops, ImageDraw
import math
import random

# ──────────────────── RMSE FUNCTION ────────────────────

# RMSE function for using file paths
def rmseFunctionPaths(path1, path2):
    im1 = Image.open(path1)
    im2 = Image.open(path2)
    err = np.asarray(ImageChops.difference(im1, im2)) / 255 
    err = math.sqrt(np.mean(np.square(err)))
    return err

# RMSE function for using PIL Images
def rmseFunction(im1, im2):
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


# Example of using the rmse path function to find the error between two images.
"""
path1 = "images/image1.png"
path2 = "images/image2.png"
err = rmseFunctionPath(path1, path2)
print(err)
"""

# ──────────────────── CANVAS SETUP ────────────────────

original = Image.open("images/palette.jpg") # Opening the original image

averageOriginalColor = original.resize((1,1)).getpixel((0,0)) # Gets the average color of the original image

# Creates a blank canvas which will be the start of the geometric primitive image
#   first parameter specifies the 'mode' of the new image (RGB)
#   second parameter specifies the size of the canvas (a tuple containing the width and height of the original image)
#   third parameter specifies the starting color of the canvas (the average color of the original image)
originalWidth, originalHeight = original.size

canvas = Image.new("RGB", (originalWidth, originalHeight), averageOriginalColor)

#canvas.show() # Shows the starting canvas

# ──────────────────── HILL CLIMBING ────────────────────

def getRandomBoundingBox():
    x0 = random.randrange(originalWidth-1)
    y0 = random.randrange(originalHeight-1)
    x1 = random.randrange(originalWidth-1)
    y1 = random.randrange(originalHeight-1)

    # Stupid complicated ternary stuff:
    #   The ellipse drawing feature for PIL only works if x1 is larger than x0 AND if y1 is greater than y0.
    #   That means I have to return the smallest randomly generated x coordinate and y coordinate as x0 and y0 (respectively)
    #       (and the same goes for x1 and y1, but they have to be the biggest.)
    return ((x0 if x0 < x1 else x1),(y0 if y0 < y1 else y1),(x0 if x0 > x1 else x1),(y0 if y0 > y1 else y1))

# Getting the average color of the space inside of the added shape
def getAverageColorInShape(shapeCoordinates):
    transparent = Image.new('RGBA', (originalWidth,originalHeight), (0, 0, 0, 0))
    transparentEdit = ImageDraw.Draw(transparent)
    transparentEdit.ellipse(shapeCoordinates, fill ="#000000")
    transparent1 = Image.new('RGBA', (originalWidth,originalHeight), (0, 0, 0, 0))
    transparent1.paste(original, (0,0), mask=transparent)
    #transparent1.show()
    areaColor = transparent1.resize((1,1)).getpixel((0,0))

    return areaColor

canvasEdit = ImageDraw.Draw(canvas)
x0,y0,x1,y1 = getRandomBoundingBox()
shape = [(x0, y0), (x1, y1)] 

areaColor = getAverageColorInShape(shape)

canvasEdit.ellipse(shape, fill = areaColor)

err = rmseFunction(original, canvas)
print(err)
#canvas.show()

for i in range(4):
    i+=1
    canvasAlternate = Image.new("RGB", (originalWidth, originalHeight), averageOriginalColor)
    canvasEditAlternate = ImageDraw.Draw(canvasAlternate)
    x0a,y0a,x1a,y1a = getRandomBoundingBox()
    shapeAlternate = [(x0a, y0a), (x1a, y1a)] 
    areaColorAlternate = getAverageColorInShape(shapeAlternate)

    canvasEditAlternate.ellipse(shapeAlternate, fill = areaColorAlternate)

    errAlternate = rmseFunction(original, canvasAlternate)
    if errAlternate < err:
        canvas = canvasAlternate
        cavnasEdit = canvasEditAlternate

        x0 = x0a
        x1 = x1a
        y0 = y0a
        y1 = y1a

        shape = shapeAlternate
        areaColor = areaColorAlternate
        err = errAlternate
        print(err)

canvas.show()

        
