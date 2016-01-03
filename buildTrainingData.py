import os
import Image
import numpy as np
import math
import json

def imgToBW(img, threshold):
    width, height = img.size
    imgBW = np.asarray(img.convert("L"))

    result = np.ones((height, width), dtype=np.uint8)

    for row in range(height):
        for col in range(width):
            if imgBW[row][col] > threshold:
                result[row][col] = 0xFF
            else:
                result[row][col] = 0x00
    return result

manaLocation  = [22, 35, 59, 82]
manaThreshold = 245

cumManaImages = {}
for i in range(11) + [12, 20]:
   cumManaImages[i] = np.zeros((47, 37), dtype=np.uint8)

with open("cards.collectible.json", "r") as f:
	cardsJSON = json.loads(f.read())

for card in cardsJSON:
	mana = int(card["cost"])
	cardImage = Image.open("cardImages/" + card["name"] + ".png")
	manaImage = imgToBW(cardImage.crop(manaLocation), manaThreshold)
	cumManaImage = cumManaImages[mana]
	for row in range(len(manaImage)):
		for col in range(len(manaImage[row])):
			if manaImage[row, col] == 0xFF:
				cumManaImage[row, col] += 1

for i in range(11) + [12, 20]:
	image = cumManaImages[i]
	height, width = image.shape
	maxVal = np.amax(image)
	for row in range(height):
		for col in range(width):
			image[row, col] *= (0xFF / maxVal)
	Image.fromarray(cumManaImages[i]).save("./compImages/mana-" + str(i) + ".bmp", "BMP")