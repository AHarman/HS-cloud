import os
import Image
import numpy as np
import math
import json
from   utils import *
from cardReader import Card, ScreenshotParser

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
class trainingDataBuilder:

	def __init__(self):
		self.screenshotParser = ScreenshotParser()

	def createCumulativeManaImages(self, cards):
		global actualManas
		cumManaImages = {}
		manaThreshold = 245
		for i in range(11) + [12, 20]:
			cumManaImages[i] = np.zeros((40, 30), dtype=np.uint8)

		for i in range(len(cards)):
			card = cards[i]
			mana = actualManas[i]
		
			if card.golden:
				manaImage = imgToBW(card.cardImage.crop(self.screenshotParser.gManaLocation[card.cardType]), self.screenshotParser.manaThreshold)
			else:
				manaImage = imgToBW(card.cardImage.crop(self.screenshotParser.manaLocation), self.screenshotParser.manaThreshold)
				cumManaImage = cumManaImages[mana]
				for row in range(len(manaImage)):
					for col in range(len(manaImage[row])):
						if manaImage[row, col] == 0xFF:
							cumManaImage[row, col] += 1

		cumManaImages = self.normaliseImages(cumManaImages)
		for i in range(11) + [12, 20]:
			Image.fromarray(cumManaImages[i]).save("./compImages/mana-" + str(i) + ".bmp", "BMP")

	def createCumlativeMinAttImages(self, cards):
		global minAttacks
		cumAttImages = []
		threshold = 245
		attImage = None

		for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
			cumAttImages.append(np.zeros((40, 30), dtype=np.uint8))

		i = 0
		for card in cards:
			if card.cardType == "Minion":
				attack = minAttacks[i]
				cumAttImage = cumAttImages[attack]
				if card.golden:
					attImage = imgToBW(card.cardImage.crop(self.screenshotParser.gMinAttLocation), threshold)
					#card.cardImage.crop(self.screenshotParser.gMinAttLocation ).show()
				else:
					attImage = imgToBW(card.cardImage.crop(self.screenshotParser.minAttLocation ), threshold)
					#card.cardImage.crop(self.screenshotParser.minAttLocation ).show()
			
				#Image.fromarray(attImage).show()
				#raw_input(str(attack))
				for row in range(len(attImage)):
					for col in range(len(attImage[row])):
						if attImage[row, col] == 0xFF:
							cumAttImage[row, col] += 1
				i += 1

		cumAttImages = self.normaliseImages(cumAttImages)
		for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
			Image.fromarray(cumAttImages[i]).save("./compImages/minAtt-" + str(i) + ".bmp", "BMP")

	def normaliseImages(self, images):
		for i in range(len(images)):
			print str(i) + " " + str(len(images))
			image = images[i]
			height, width = image.shape
			maxVal = np.amax(image)
			if maxVal != 0:
				for row in range(height):
					for col in range(width):
						image[row, col] = float(image[row, col]) * (255.0 / maxVal)
		return images

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
			res = self.screenshotParser.getCardMana(card, minMana)

			for i in range(11) + [12, 20]:
				metricsMeanAll[actualMana][i] += res[i]
				metricsMinAll[actualMana][i] = min(res[i], metricsMinAll[actualMana][i])
				metricsMaxAll[actualMana][i] = max(res[i], metricsMaxAll[actualMana][i])
			manaCount[actualMana] += 1

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

	def getMinAttMetrics(self, cards):
		count = 0
		global minAttacks
		attCount      =       {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0}
		metricsMeanAll = { 0: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   1: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   2: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   3: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   4: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   5: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   6: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   7: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   8: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   9: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                  10: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                  12: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0}}
		metricsMaxAll  = { 0: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   1: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   2: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   3: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   4: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   5: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   6: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   7: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   8: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                   9: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                  10: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0},
		                  12: {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0}}
		metricsMinAll  = { 0: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   1: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   2: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   3: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   4: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   5: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   6: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   7: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   8: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                   9: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                  10: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999},
		                  12: {0:999, 1:999, 2:999, 3:999, 4:999, 5:999, 6:999, 7:999, 8:999, 9:999, 10:999, 12:999}}

		for card in cards:
			if card.cardType == "Minion":
				actualAtt = minAttacks[count]
				res = self.screenshotParser.getMinAttack(card, getMetrics=True)

				for i in range(11) + [12]:
					metricsMeanAll[actualAtt][i] += res[i]
					metricsMinAll[actualAtt][i] = min(res[i], metricsMinAll[actualAtt][i])
					metricsMaxAll[actualAtt][i] = max(res[i], metricsMaxAll[actualAtt][i])
				attCount[actualAtt] += 1

				count += 1

		for i in range(11) + [12]:
			for j in range(11) + [12]:
				if attCount[i] != 0:
					metricsMeanAll[i][j] /= attCount[i]
		print "ALL THE THINGS"
		for i in range(11) + [12]:
			print str(i) + ":"
			print "    Mean: " + str(metricsMeanAll[i])
			print "    Max:  " + str(metricsMaxAll[i])
			print "    Min:  " + str(metricsMinAll[i])
		return cards

	# Just so we don't waste time getting all the stuff we don't need, I've copied this across
	def getCardsFromImages(self, pathToImages):
		cards = []
		count = 0
		minMana = 0
		
		global actualManas
		for name in self.screenshotParser.reorderImages(os.listdir(pathToImages)):
			if name[-4:] == ".png":
				screenshot = Image.open(pathToImages + name)
				for i in range(self.screenshotParser.numOfCardsInScreenshot(screenshot)):
					card = Card(screenshot.crop(self.screenshotParser.cardLocations[i]))
					cards.append(card)
					card.cardType = self.screenshotParser.getCardType(card)
					card.golden = self.screenshotParser.isGolden(card)
					#card.mana = actualManas[count]


					count += 1
					print "Card " + str(count)
		return cards

if __name__ == "__main__":
	p = trainingDataBuilder()
	cards = p.getCardsFromImages("./screencaps/")
	#p.createCumulativeManaImages(cards)
	#p.createCumlativeMinAttImages(cards)
	#p.getManaMetrics(cards)
	p.getMinAttMetrics(cards)
	


