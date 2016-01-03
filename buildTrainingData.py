import os
import Image
import numpy as np
import math
import json
from   utils import imgToBW

def createCumulativeManaImages():
	with open("cards.collectible.json", "r") as f:
		cardsJSON = json.loads(f.read())
	cumManaImages = {}
	manaLocation  = [20, 30, 50, 70]
	manaThreshold = 245
	for i in range(11) + [12, 20]:
		cumManaImages[i] = np.zeros((40, 30), dtype=np.uint8)

	for card in cardsJSON:
		mana = int(card["cost"])
		cardImage = Image.open("cardImages/" + card["name"] + ".png")
		cardImage = cardImage.resize((247, 339), Image.ANTIALIAS)
		manaImage = imgToBW(cardImage.crop(manaLocation), manaThreshold)
		cumManaImage = cumManaImages[mana]
		for row in range(len(manaImage)):
			for col in range(len(manaImage[row])):
				if manaImage[row, col] == 0xFF:
					cumManaImage[row, col] += 1

	cumManaImages = normaliseManaImages(cumManaImages)
	for i in range(11) + [12, 20]:
		Image.fromarray(cumManaImages[i]).save("./compImages/mana-" + str(i) + ".bmp", "BMP")


def normaliseManaImages(cumManaImages):
	for i in range(11) + [12, 20]:
		image = cumManaImages[i]
		height, width = image.shape
		maxVal = np.amax(image)
		for row in range(height):
			for col in range(width):
				image[row, col] *= (255.0 / maxVal)
	return cumManaImages

createCumulativeManaImages()