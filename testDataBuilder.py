import os
import Image
import numpy as np
import math
import json
from   app_engine.utils import *
from app_engine.cardReader import Card, ScreenshotParser
from trainingDataInfo import *

class TestingDataCreator:

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

		cumManaImages = self.normaliseManaImages(cumManaImages)
		for i in range(11) + [12, 20]:
			Image.fromarray(cumManaImages[i]).save("./images/compImages/mana-" + str(i) + ".bmp", "BMP")

	def normaliseManaImages(self, cumManaImages):
		for i in range(11) + [12, 20]:
			image = cumManaImages[i]
			height, width = image.shape
			maxVal = np.amax(image)
			if maxVal != 0:
				for row in range(height):
					for col in range(width):
						image[row, col] = float(image[row, col]) * (255.0 / maxVal)
		return cumManaImages

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
			res = self.screenshotParser.getCardMana(card, minMana, True)

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

	# Just so we don't waste time getting all the stuff we don't need, I've copied this across
	def getCardsFromImages(self, pathToImages):
		cards = []
		count = 0
		minMana = 0
		
		global actualManas
		for name in sorted(os.listdir(pathToImages)):
			if name[-4:] == ".png":
				screenshot = Image.open(pathToImages + name)
				for i in range(self.screenshotParser.numOfCardsInScreenshot(screenshot)):
					card = Card(screenshot.crop(self.screenshotParser.cardLocations[i]))
					cards.append(card)
					card.cardType = self.screenshotParser.getCardType(card)
					card.golden = self.screenshotParser.isGolden(card)
					card.mana = actualManas[count]
					card.cardImage.save("./images/temp/" + str(count) + ".bmp", "BMP")


					count += 1
					print "Card " + str(count)
		return cards

if __name__ == "__main__":
	p = TestingDataCreator()
	cards = p.getCardsFromImages("./images/trainingData/")
	p.createCumulativeManaImages(cards)
	p.getManaMetrics(cards)
	


