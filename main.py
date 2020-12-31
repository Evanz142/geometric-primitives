#import matplotlib.image as mpimg
#import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageChops
import math

# 

def rmseFunction(path1, path2):
    im1 = Image.open(path1)
    im2 = Image.open(path2)
    #im1.show() # Opens up the image using Windows Photos (for me)
    err = np.asarray(ImageChops.difference(im1, im2)) / 255 
    err = math.sqrt(np.mean(np.square(err)))
    return err


#image1 = mpimg.imread('images/image1.png');
#image2 = mpimg.imread('images/image2.png');
#imgplot = plt.imshow(ref)

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
#path1 = "images/image1.png"
#path2 = "images/image2.png"
#err = rmseFunction(path1, path2)
#print(err)

