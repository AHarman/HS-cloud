import os
import Image
import numpy as np
import math
from   utils import *

np.set_printoptions(linewidth=150)

class Card:
	manaLocation       =  ( 18,  22,  48,  62)
	#quantityLocation  =  ( 75, 238,  99, 254)
	#rarityLocation    =  ( 77, 132,  82, 143)
	#cardNameLocation  =  ( 14, 104, 145, 126)    # TODO: This only works for spells, not minions (different text warp)
	#minionTest        =  (0, 0, 0, 0)    # TODO: Do this
	#weaponTest        =  (0, 0, 0, 0)    # TODO: Do this
	#quantityThreshold = 125

	def __init__(self, image):
		self.cardImage     = image
		#self.nameImage     = self.cardImage.crop(self.cardNameLocation)
		self.manaImage     = self.cardImage.crop(self.manaLocation)
		#self.quantityImage = self.cardImage.crop(self.quantityLocation)
		#self.rarityImage   = self.cardImage.crop(self.rarityLocation)

		self.name = None
		self.hero = None

	def show(self):
		return self.cardImage.show()
	
	def determineRarity(self):
		return None

class screenshotParser:
	# All these use 1366x768 as the resolution
	# Create dictionaries with resolutions as key to extend this
	cardLocations     = [( 286,  165,  518,  534),  ( 527,  165,  755,  534),  ( 768,  165, 1000,  534),  (1009,  165, 1241,  534),
	                     ( 286,  544,  518,  913),  ( 527,  544,  755,  913),  ( 768,  544, 1000,  913),  (1009,  544, 1241,  913)]
	cardPresenceTest  = [( 500,  422,  516,  436),  ( 743,  422,  759,  436),  ( 981,  422,  997,  436),  (1222,  422, 1238,  436),
	                     ( 500,  801,  516,  815),  ( 743,  801,  759,  815),  ( 981,  801,  997,  815),  (1222,  801, 1238,  815)]
	classLocation     =  ( 676,  111,  848,  137)

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

	# TODO: Make sure this works for mana of 10, 12 and 20 (I don't have those cards in the test data)
	# Could optimise this as you know that, say, you're not going to go from 1 mana to 5 because of basic cards
	def getCardMana(self, card, lowerLimit=0):
		#refWidth  = 30
		#refHeight = 40
		manaImage = imgToBW(card.manaImage, self.manaThreshold).reshape(-1)
		#print manaImage.getbbox()
		#manaImage.show()
		#raw_input("cmon")

		bestGuess = 0
		bestMetric = 0
		metrics = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 12:0, 20:0}
		for currentMana in range(11) + [12, 20]:
			currentMetric = 0
			currentManaRef = self.manaArrays[currentMana]

			for i in range(len(manaImage)):
				metrics[currentMana] += 0xFF - abs(int(manaImage[i]) - int(currentManaRef[i]))

		for mana in range(11) + [12, 20]:
			metrics[mana] /= len(manaImage)
			if bestMetric < metrics[mana]:
				bestMetric = metrics[mana]
				bestGuess = mana
		#print metrics
		#print bestGuess
		#card.manaImage.show()
		#raw_input("cmon")
		return metrics

	def numOfCardsInScreenshot(self, screenshot):
		count = 8
		for box in self.cardPresenceTest:
			#a = imgToBW(screenshot.crop(box), self.cardPresenceThreshold, image=True)
			#a.show()
			#raw_input("\\n pls")
			array = imgToBW(screenshot.crop(box), self.cardPresenceThreshold, image=False).reshape(-1)
			if 0 not in array:
				count -= 1
		return count

	def getCardsFromImages(self, pathToImages):
		cards = []
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

		for name in sorted(os.listdir(pathToImages)):
			if name[-4:] == ".png":
				screenshot = Image.open(pathToImages + name)
				#currentClass = self.getClassFromScreenshot(screenshot)

				for i in range(self.numOfCardsInScreenshot(screenshot)):
					card = Card(screenshot.crop(self.cardLocations[i]))
					cards.append(card)
					actualMana = actualManas[count]
					res = self.getCardMana(card, minMana)

					for i in range(11) + [12, 20]:
						metricsMeanAll[actualMana][i] += res[i]
						metricsMinAll[actualMana][i] = min(res[i], metricsMinAll[actualMana][i])
						metricsMaxAll[actualMana][i] = max(res[i], metricsMaxAll[actualMana][i])
					manaCount[actualMana] += 1

					#imgToBW(card.manaImage, self.manaThreshold, image=True).save("./temp/" + str(card.mana) + "-" + str(count) + ".bmp", "BMP")
					count += 1

				# TODO: do this based on class once we have class detection implemented. This won't work if the cards fill the page neatly
				#if self.numOfCardsInScreenshot(screenshot) < 8:
				#	minMana = 0
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
		#print metricsMax
		#print metricsMin
		return cards

p = screenshotParser()
p.getCardsFromImages("./screencaps/")