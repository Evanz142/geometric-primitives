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
    x0 = random.randrange(originalWidth-3) + 1
    y0 = random.randrange(originalHeight-3) + 1
    x1 = random.randrange(originalWidth-3) + 1
    y1 = random.randrange(originalHeight-3) + 1

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

canvasAlternate = canvas
canvasEditAlternate = ImageDraw.Draw(canvasAlternate)
canvasEdit.ellipse(shape, fill = areaColor)

err = rmseFunction(original, canvasAlternate)
print(err)
#canvas.show()

for i in range(4):
    i+=1
    canvasAlternate = Image.new("RGB", (originalWidth, originalHeight), averageOriginalColor)

    x0a,y0a,x1a,y1a = getRandomBoundingBox()

    while (x1a - x0a < 11 or y1a - y0a < 11): # To make sure the generated shape isn't too small
        x0a,y0a,x1a,y1a = getRandomBoundingBox()

    shapeAlternate = [(x0a, y0a), (x1a, y1a)] 

    areaColorAlternate = getAverageColorInShape(shapeAlternate)

    canvasEditAlternate.ellipse(shapeAlternate, fill = areaColorAlternate)

    errAlternate = rmseFunction(original, canvasAlternate)
    if errAlternate < err:
        #canvas = canvasAlternate
        #cavnasEdit = canvasEditAlternate

        x0 = x0a
        x1 = x1a
        y0 = y0a
        y1 = y1a

        #shape = shapeAlternate
        #areaColor = areaColorAlternate
        err = errAlternate
        print(err)

changePossibilities = ("xCenter", "yCenter", "xRadius", "yRadius") # 
multiplierPossibilities = (1,-1) # possible multipliers for when randomly moving shape, (-) vs (+) determines what direction

changerFactorConstant = 100 # A constant that determines the range (in pixels) of possible shape edits

for i in range(50):

    x0a = x0
    x1a = x1
    y0a = y0
    y1a = y1

    canvasAlternate = Image.new("RGB", (originalWidth, originalHeight), averageOriginalColor)
    canvasEditAlternate = ImageDraw.Draw(canvasAlternate)

    change = random.choice(changePossibilities)

    if change == "xCenter":

        changeFactor = random.randrange(originalWidth // changerFactorConstant) + 2 # The x position can change by anywhere from 2 pixels to 1/50th of the screen width
        multiplier = random.choice(multiplierPossibilities) # Randomly chooses whether it moves positive or negative

        # This while loops is to make sure the edit doesn't force the shape to spawn outside of the image boundries and create an error.
        while (x0a + (changeFactor * multiplier) < 0) or (x1a + (changeFactor * multiplier) > originalWidth - 1):
            print("a")
            # Same stuff as what was written before the while loop
            changeFactor = random.randrange(originalWidth // changerFactorConstant) + 2
            multiplier = random.choice(multiplierPossibilities)
            
        # Making the changes to the x coordinates
        x0a += (changeFactor * multiplier) 
        x1a += (changeFactor * multiplier)

    elif change == "yCenter":

        changeFactor = random.randrange(originalHeight // changerFactorConstant) + 2 # The y position can change by anywhere from 2 pixels to 1/50th of the screen height
        multiplier = random.choice(multiplierPossibilities) # Randomly chooses whether it moves positive or negative

        # This while loops is to make sure the edit doesn't force the shape to spawn outside of the image boundries and create an error.
        while (y0a + (changeFactor * multiplier) < 0) or (y1a + (changeFactor * multiplier) > originalHeight - 1):
            print("b")
            # Same stuff as what was written before the while loop
            changeFactor = random.randrange(originalHeight // changerFactorConstant) + 2
            multiplier = random.choice(multiplierPossibilities)
            
        # Making the changes to the y coordinates
        y0a += (changeFactor * multiplier) 
        y1a += (changeFactor * multiplier)

    elif change == "xRadius":

        changeFactor = random.randrange(originalWidth // (changerFactorConstant / 2)) + 2 # I divided the changeFactorConstant by 2 so that I can add the same constant to both coordinates
        multiplier = random.choice(multiplierPossibilities)

        # I added an extra conditional check to make sure the the mutation doesn't make the shape smaller than 10 pixels
        while (x0a + (changeFactor * multiplier) < 0) or (x1a + (changeFactor * multiplier) > originalWidth - 1) and (x1a - x0a - (changeFactor * multiplier * 2) < 10):
            print("c")
            changeFactor = random.randrange(originalWidth // (changerFactorConstant / 2)) + 2
            multiplier = random.choice(multiplierPossibilities)

        x0a += (changeFactor * multiplier)
        x1a += (changeFactor * multiplier)

    elif change == "yRadius":

        changeFactor = random.randrange(originalHeight // (changerFactorConstant / 2)) + 2 # I divided the changeFactorConstant by 2 so that I can add the same constant to both coordinates
        multiplier = random.choice(multiplierPossibilities)

        # I added an extra conditional check to make sure the the mutation doesn't make the shape smaller than 10 pixels
        while (y0a + (changeFactor * multiplier) < 0) or (y1a + (changeFactor * multiplier) > originalHeight - 1) and (y1a - y0a - (changeFactor * multiplier * 2) < 10):
            print("d")
            changeFactor = random.randrange(originalHeight // (changerFactorConstant / 2)) + 2
            multiplier = random.choice(multiplierPossibilities)

        y0a += (changeFactor * multiplier)
        y1a += (changeFactor * multiplier)


    shapeAlternate = [(x0a, y0a), (x1a, y1a)] 

    areaColorAlternate = getAverageColorInShape(shapeAlternate)

    canvasEditAlternate.ellipse(shapeAlternate, fill = areaColorAlternate)

    errAlternate = rmseFunction(original, canvasAlternate)
    if errAlternate < err:
        #canvas = canvasAlternate
        #cavnasEdit = canvasEditAlternate

        x0 = x0a
        x1 = x1a
        y0 = y0a
        y1 = y1a

        #shape = shapeAlternate
        #areaColor = areaColorAlternate
        err = errAlternate
        print(err)
    else: 
        print("Mutation failed")

print(err)
#canvas.show()

        