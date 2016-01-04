import os
import Image
import numpy as np
import math
import json
from   utils import *

# def createCumulativeManaImages():
# 	with open("cards.collectible.json", "r") as f:
# 		cardsJSON = json.loads(f.read())
# 	cumManaImages = {}
# 	manaLocation  = [20, 30, 50, 70]
# 	manaThreshold = 245
# 	for i in range(11) + [12, 20]:
# 		cumManaImages[i] = np.zeros((40, 30), dtype=np.uint8)

# 	for card in cardsJSON:
# 		mana = int(card["cost"])
# 		cardImage = Image.open("cardImages/" + card["name"] + ".png")
# 		cardImage = cardImage.resize((247, 339), Image.ANTIALIAS)
# 		manaImage = imgToBW(cardImage.crop(manaLocation), manaThreshold)
# 		cumManaImage = cumManaImages[mana]
# 		for row in range(len(manaImage)):
# 			for col in range(len(manaImage[row])):
# 				if manaImage[row, col] == 0xFF:
# 					cumManaImage[row, col] += 1

# 	cumManaImages = normaliseManaImages(cumManaImages)
# 	for i in range(11) + [12, 20]:
# 		Image.fromarray(cumManaImages[i]).save("./compImages/mana-" + str(i) + ".bmp", "BMP")
def createCumulativeManaImages(cards):
	global actualManas
	cumManaImages = {}
	manaThreshold = 245
	for i in range(11) + [12, 20]:
		cumManaImages[i] = np.zeros((40, 30), dtype=np.uint8)

	for i in range(len(cards)):
		card = cards[i]
		mana = actualManas[i]
		
		manaImage = imgToBW(card.manaImage, manaThreshold)
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
		if maxVal != 0:
			for row in range(height):
				for col in range(width):
					image[row, col] = float(image[row, col]) * (255.0 / maxVal)
	return cumManaImages


class Card:
	manaLocation       =  ( 18,  22,  48,  62)
	def __init__(self, image):
		self.cardImage     = image
		self.manaImage     = self.cardImage.crop(self.manaLocation)
		self.mana = None


class screenshotParser:
	# Create dictionaries with resolutions as key to extend this
	cardLocations     = [( 286,  165,  518,  534),  ( 527,  165,  755,  534),  ( 768,  165, 1000,  534),  (1009,  165, 1241,  534),
	                     ( 286,  544,  518,  913),  ( 527,  544,  755,  913),  ( 768,  544, 1000,  913),  (1009,  544, 1241,  913)]
	cardPresenceTest  = [( 500,  422,  516,  436),  ( 743,  422,  759,  436),  ( 981,  422,  997,  436),  (1222,  422, 1238,  436),
	                     ( 500,  801,  516,  815),  ( 743,  801,  759,  815),  ( 981,  801,  997,  815),  (1222,  801, 1238,  815)]

	classThreshold        = 125
	cardPresenceThreshold = 100
	manaThreshold         = 245

	def __init__(self):
		self.manaArrays = self.loadManaArrays("./compImages/")

	def loadManaArrays(self, pathToImages):
		arrays = {}
		for i in range(11) + [12, 20]:
			arrays[i] = np.asarray(Image.open(pathToImages + "mana-" + str(i) + ".bmp")).reshape(-1)
		return arrays

	def getCardMana(self, card, lowerLimit=0):
		manaImage = imgToBW(card.manaImage, self.manaThreshold).reshape(-1)

		bestGuess = 0
		bestMetric = 0
		metrics = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0}
		for currentMana in range(11) + [12, 20]:
			currentMetric = 0
			currentManaRef = self.manaArrays[currentMana]

			for i in range(len(manaImage)):
				if currentManaRef[i] in [0x00, 0xFF] and manaImage[i] != currentManaRef[i]:
					metrics[currentMana] -= 255
				else:
					metrics[currentMana] += 0xFF - abs(int(manaImage[i]) - int(currentManaRef[i]))

		for mana in range(11) + [12, 20]:
			metrics[mana] /= len(manaImage)
			if bestMetric < metrics[mana]:
				bestMetric = metrics[mana]
				bestGuess = mana
		return metrics



	def numOfCardsInScreenshot(self, screenshot):
		count = 8
		for box in self.cardPresenceTest:
			array = imgToBW(screenshot.crop(box), self.cardPresenceThreshold, image=False).reshape(-1)
			if 0 not in array:
				count -= 1
		return count

	def getCards(self, pathToImages):
		cards = []
		for name in sorted(os.listdir(pathToImages)):
			if name[-4:] == ".png":
				screenshot = Image.open(pathToImages + name)
				#currentClass = self.getClassFromScreenshot(screenshot)

				for i in range(self.numOfCardsInScreenshot(screenshot)):
					card = Card(screenshot.crop(self.cardLocations[i]))
					cards.append(card)
		return cards

	def getManaMetrics(self, cards):
		count = 0
		minMana = 0
		global actualManas
		manaCount      =      {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0}
		metricsMeanAll = { 0: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   1: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   2: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   3: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   4: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   5: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   6: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   7: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   8: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   9: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                  10: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                  12: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                  20: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0}}
		metricsMaxAll  = { 0: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   1: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   2: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   3: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   4: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   5: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   6: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   7: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   8: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                   9: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                  10: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                  12: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0},
		                  20: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0}}
		metricsMinAll  = { 0: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   1: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   2: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   3: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   4: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   5: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   6: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   7: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   8: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                   9: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                  10: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                  12: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500},
		                  20: {0:500, 1:500, 2:500, 3:500, 4:500, 5:500, 6:500, 7:500, 8:500, 9:500, 10:500, 12:500, 20:500}}


		for card in cards:
			actualMana = actualManas[count]
			res = self.getCardMana(card, minMana)

			for i in range(11) + [12, 20]:
				metricsMeanAll[actualMana][i] += res[i]
				metricsMinAll[actualMana][i] = min(res[i], metricsMinAll[actualMana][i])
				metricsMaxAll[actualMana][i] = max(res[i], metricsMaxAll[actualMana][i])
			manaCount[actualMana] += 1

			imgToBW(card.manaImage, self.manaThreshold, image=True).save("./temp/" + str(card.mana) + "-" + str(count) + ".bmp", "BMP")
			count += 1

		for i in range(11) + [12, 20]:
			for j in range(11) + [12, 20]:
				if manaCount[i] != 0:
					metricsMeanAll[i][j] /= manaCount[i]
		print "ALL THE THINGS"
		for i in range(11) + [20]:
			print str(i) + ":"
			print "    Mean: " + str(metricsMeanAll[i])
			print "    Max:  " + str(metricsMaxAll[i])
			print "    Min:  " + str(metricsMinAll[i])
		return cards


p = screenshotParser()
cards = p.getCards("./screencaps/")
createCumulativeManaImages(cards)
p.getManaMetrics(cards)

