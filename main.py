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