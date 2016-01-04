import os
import Image
import numpy as np
import math
import pylab as plt
from   utils import *

np.set_printoptions(linewidth=150)

class Card:
	#quantityLocation  = ( 75, 238,  99, 254)
	# TODO: Golden minions need their own

	#cardNameLocation  = ( 14, 104, 145, 126)    # TODO: This only works for spells, not minions (different text warp)
	#minionTest        = (0, 0, 0, 0)    # TODO: Do this
	#weaponTest        = (0, 0, 0, 0)    # TODO: Do this
	#quantityThreshold = 125

	def __init__(self, image):
		self.cardImage     = image
		#self.nameImage     = self.cardImage.crop(self.cardNameLocation)
		#self.quantityImage = self.cardImage.crop(self.quantityLocation)
		#self.rarityImage   = self.cardImage.crop(self.rarityLocation)

		self.name = None
		self.hero = None
		self.rarity = None
		self.cardType = None

	def show(self):
		return self.cardImage.show()
	

class screenshotParser:
	# All these use 1366x768 as the resolution
	# Create dictionaries with resolutions as key to extend this
	cardLocations    = [( 286,  165,  518,  534),  ( 527,  165,  755,  534),  ( 768,  165, 1000,  534),  (1009,  165, 1241,  534),
	                    ( 286,  544,  518,  913),  ( 527,  544,  755,  913),  ( 768,  544, 1000,  913),  (1009,  544, 1241,  913)]
	cardPresenceTest = [( 500,  422,  516,  436),  ( 743,  422,  759,  436),  ( 981,  422,  997,  436),  (1222,  422, 1238,  436),
	                    ( 500,  801,  516,  815),  ( 743,  801,  759,  815),  ( 981,  801,  997,  815),  (1222,  801, 1238,  815)]
	classLocation    =  ( 676,  111,  848,  137)
	quantityTest     =  (  74,  346,  174,  356)
	legendaryTest    =  ( 192,   13,  215,   23)
	weaponTest       =  (  61,    6,   72,   21)
	minionTest       =  (   0,  260,   10,  275)    #Needs to be checked AFTER weapon check
	rarityLocation   =  {"Spell" : (113, 203, 122, 215),
	                     "Minion": (120, 197, 129, 209), 
	                     "Weapon": (118, 198, 127, 210)}
	
	manaLocation     = ( 18,  22,  48,  62)

	classThreshold        = 125
	quantityThreshold     = 125
	cardPresenceThreshold = 100
	manaThreshold         = 245
	cardPresenceThreshold = 100
	legendaryThreshold    = 100
	weaponThreshold       = 100
	minionThreshold       = 100

	def __init__(self):
		self.manaArrays = self.loadManaArrays("./compImages/")

	def loadManaArrays(self, pathToImages):
		arrays = {}
		for i in range(11) + [12, 20]:
			arrays[i] = np.asarray(Image.open(pathToImages + "mana-" + str(i) + ".bmp")).reshape(-1)
		return arrays

	def getCardQuantity(self, card):
		if 0 in imgToBW(card.cardImage.crop(self.quantityTest), self.quantityThreshold).reshape(-1):
			return 2
		else:
			return 1

	def isLegendary(self, card):
		return (0 in imgToBW(card.cardImage.crop(self.legendaryTest), self.legendaryThreshold).reshape(-1))

	def getCardRarity(self, card):
		if self.isLegendary(card):
			return "Legendary"
		return None

	def getCardType(self, card):
		if card.rarity == "Legendary":
			return "Minion"

		weaponImage = imgToBW(card.cardImage.crop(self.weaponTest), self.weaponThreshold).reshape(-1)
		if sum(1 for i in weaponImage if i == 0) > 10 and 0 in weaponImage:
			return "Weapon"

		minionImage = imgToBW(card.cardImage.crop(self.minionTest), self.minionThreshold).reshape(-1)
		if 0 in minionImage:
			return "Minion"

		return "Spell"

	def getCardRarity(self, card):
		if self.isLegendary(card):
			return "Legendary"
		return None


	# TODO: Make sure this works for mana of 10, 12 and 20 (I don't have those cards in the test data)
	# Could optimise this as you know that, say, you're not going to go from 1 mana to 5 because of basic cards
	def getCardMana(self, card, lowerLimit=0):
		#refWidth  = 30
		#refHeight = 40
		manaImage = imgToBW(card.cardImage.crop(self.manaLocation), self.manaThreshold).reshape(-1)
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
					card.rarity = self.getCardRarity(card)
					card.cardType = self.getCardType(card)
					card.quantity = self.getCardQuantity(card)
					actualMana = actualManas[count]
					'''res = self.getCardMana(card, minMana)

					for i in range(11) + [12, 20]:
						metricsMeanAll[actualMana][i] += res[i]
						metricsMinAll[actualMana][i] = min(res[i], metricsMinAll[actualMana][i])
						metricsMaxAll[actualMana][i] = max(res[i], metricsMaxAll[actualMana][i])
					manaCount[actualMana] += 1
					count += 1

					#imgToBW(card.manaImage, self.manaThreshold, image=True).save("./temp/" + str(card.mana) + "-" + str(count) + ".bmp", "BMP")
					

		for i in range(11) + [12, 20]:
			for j in range(11) + [12, 20]:
				if manaCount[i] != 0:
					metricsMeanAll[i][j] /= manaCount[i]
		print "ALL THE THINGS"
		for i in range(11) + [20]:
			print str(i) + ":"
			print "    Mean: " + str(metricsMeanAll[i])
			print "    Max:  " + str(metricsMaxAll[i])
			print "    Min:  " + str(metricsMinAll[i])'''
		return cards


p = screenshotParser()
cards = p.getCardsFromImages("./screencaps/")

'''maxs = {"Free": [0]*768, "Common": [0]*768, "Rare": [0]*768, "Epic": [0]*768, "Legendary": [0]*768}
mins = {"Free": [0]*768, "Common": [0]*768, "Rare": [0]*768, "Epic": [0]*768, "Legendary": [0]*768}
avgs = {"Free": [0]*768, "Common": [0]*768, "Rare": [0]*768, "Epic": [0]*768, "Legendary": [0]*768}

for i in range(len(rarities)):
	if i not in goldenMinions:
		card = cards[i]
		rarity = rarities[i]
		if i < len(actualTypes):
			cardType = actualTypes[i]
		else:
			cardType = "Minion"
		
		rarityImage = card.cardImage.crop(card.rarityLocation[cardType])
		hist = rarityImage.histogram()
		for j in range(768):
			maxs[rarity][j] = max(maxs[rarity][j], hist[j])
			mins[rarity][j] = min(mins[rarity][j], hist[j])
			avgs[rarity][j] += hist[j]
		card.cardImage.crop(card.rarityLocation[cardType]).save("temp/" + str(i) + "-" + cardType + ".bmp", "BMP")
		card.cardImage.save("temp/" + str(i) + ".bmp", "BMP")

for i in range(768):
 	avgs["Free"  ][i] = float(avgs[rarity][i]) / float(frees)
 	avgs["Common"][i] = float(avgs[rarity][i]) / float(commons)
 	avgs["Rare"  ][i] = float(avgs[rarity][i]) / float(rares)
 	avgs["Epic"  ][i] = float(avgs[rarity][i]) / float(epics)

print frees
print commons
print rares
print epics

print "R:"
print "Free: "   + str(int(sum(avgs["Free"  ][:256][:-128])))
print "Common: " + str(int(sum(avgs["Common"][:256][:-128])))
print "Rare: "   + str(int(sum(avgs["Rare"  ][:256][:-128])))
print "Epic: "   + str(int(sum(avgs["Epic"  ][:256][:-128])))

print "\nG:"
print "Free: "   + str(int(sum(avgs["Free"  ][256:-256][:-128])))
print "Common: " + str(int(sum(avgs["Common"][256:-256][:-128])))
print "Rare: "   + str(int(sum(avgs["Rare"  ][256:-256][:-128])))
print "Epic: "   + str(int(sum(avgs["Epic"  ][256:-256][:-128])))

print "\nB:"
print "Free: "   + str(int(sum(avgs["Free"  ][:-128])))
print "Common: " + str(int(sum(avgs["Common"][:-128])))
print "Rare: "   + str(int(sum(avgs["Rare"  ][:-128])))
print "Epic: "   + str(int(sum(avgs["Epic"  ][:-128])))

print "Free"
plt.plot(avgs["Free"])
plt.show()
print "Common"
plt.plot(avgs["Common"])
plt.show()
print "Rare"
plt.plot(avgs["Rare"])
plt.show()
print "Epic"
plt.plot(avgs["Epic"])
plt.show()'''