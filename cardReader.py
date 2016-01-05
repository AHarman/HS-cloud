import os
import Image
import numpy as np
import math
import pylab as plt
from   utils import *

np.set_printoptions(linewidth=150)

class Card:
	#cardNameLocation  = ( 14, 104, 145, 126)    # TODO: This only works for spells, not minions (different text warp)
	#weaponTest        = (0, 0, 0, 0)    # TODO: Do this
	#quantityThreshold = 125

	def __init__(self, image):
		self.cardImage = image

		self.name = None
		self.hero = None
		self.rarity = None
		self.cardType = None
		self.mana = None
		self.golden = None

	def show(self):
		return self.cardImage.show()
	

class ScreenshotParser:
	# Create dictionaries with resolutions as key to extend this
	cardLocations    = [( 286,  165,  518,  534),  ( 527,  165,  755,  534),  ( 768,  165, 1000,  534),  (1009,  165, 1241,  534),
	                    ( 286,  544,  518,  913),  ( 527,  544,  755,  913),  ( 768,  544, 1000,  913),  (1009,  544, 1241,  913)]
	cardPresenceTest = [( 500,  422,  516,  436),  ( 743,  422,  759,  436),  ( 981,  422,  997,  436),  (1222,  422, 1238,  436),
	                    ( 500,  801,  516,  815),  ( 743,  801,  759,  815),  ( 981,  801,  997,  815),  (1222,  801, 1238,  815)]
	quantityTest     =  (  74,  346,  174,  356)
	legendaryTest    =  ( 192,   13,  215,   23)
	weaponTest       =  (  61,    6,   72,   21)
	minionTest       =  (   0,  260,   10,  275)    #Needs to be checked AFTER weapon check
	goldenTest       =  {"Spell" : (212, 126, 228, 132),
	                     "Minion": ( 48, 139,  57, 159),
	                     "Weapon": ( 48, 138,  57, 158)}
	rarityLocation   =  {"Spell" : (113, 203, 122, 215),
	                     "Minion": (120, 197, 129, 209), 
	                     "Weapon": (118, 198, 127, 210)}
	gRarityLocation  =  {"Spell" : (115, 202, 124, 214),
	                     "Minion": (114, 201, 123, 213), 
	                     "Weapon": (120, 197, 129, 209)}
	heroLocation     =  {"Druid"  :(256,   0, 312,  20),
	                     "Hunter" :(326,   0, 382,  20),
	                     "Mage"   :(396,   0, 452,  20),
	                     "Paladin":(466,   0, 522,  20),
	                     "Priest" :(536,   0, 592,  20),
	                     "Rogue"  :(606,   0, 662,  20),
	                     "Shaman" :(676,   0, 732,  20),
	                     "Warlock":(746,   0, 802,  20),
	                     "Warrior":(816,   0, 872,  20),
	                     "Neutral":(886,   0, 942,  20)}
	
	manaLocation     = ( 18,  22,  48,  62)
	gManaLocation    = {"Minion": (14,  23,  44,  63),
	                    "Spell" : (18,  22,  48,  62),
	                    "Weapon": (18,  22,  48,  62)}


	quantityThreshold     = 125
	cardPresenceThreshold = 100
	manaThreshold         = 245
	cardPresenceThreshold = 100
	legendaryThreshold    = 100
	weaponThreshold       = 100
	minionThreshold       = 100
	heroThreshold        = 100
	goldenThresholds      = {"Minion": 50,
	                         "Weapon": 50,
	                         "Spell":  70}

	possibleManas = {}

	def __init__(self):
		self.manaArrays = self.loadManaArrays("./compImages/")

	def loadManaArrays(self, pathToImages):
		arrays = {}
		for i in range(11) + [12, 20]:
			arrays[i] = np.asarray(Image.open(pathToImages + "mana-" + str(i) + ".bmp")).reshape(-1)
		return arrays

	def isGolden(self, card):
		if 0 in imgToBW(card.cardImage.crop(self.goldenTest[card.cardType]), self.goldenThresholds[card.cardType]):
			return False
		return True


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
		
		if card.golden:
			rarityImage = card.cardImage.crop(self.gRarityLocation[card.cardType])
		else:
			rarityImage = card.cardImage.crop(self.rarityLocation[card.cardType])

		colours = [0, 0, 0]
		hist = rarityImage.histogram()
		for j in range(256):
			colours[0] += hist[j] * j
			colours[1] += hist[j + 256] * j
			colours[2] += hist[j + 512] * j

		if colours[2] > 2.5 * colours[0]:
			return "Rare"
		if colours[1] * 2 < colours[0]:
			return "Epic"
		if ((colours[0] > colours[1] and colours[1] > colours[2]) or 
			(abs(colours[0] - colours[1]) < 1000 and abs(colours[0] - colours[2]) < 1000)):
			return "Free"
		return "Common"

	# TODO: Make sure this works for mana of 10, 12 and 20 (I don't have those cards in the test data)
	# Could optimise this as you know that, say, you're not going to go from 1 mana to 5 because of basic cards
	def getCardMana(self, card, lowerLimit=0, getMetrics=False):
		if card.golden:
			manaImage = imgToBW(card.cardImage.crop(self.gManaLocation[card.cardType]), self.manaThreshold).reshape(-1)
		else:
			manaImage = imgToBW(card.cardImage.crop(self.manaLocation), self.manaThreshold).reshape(-1)

		bestGuess = None
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
			metrics[currentMana] /= len(manaImage)

			if metrics[currentMana] > bestMetric:
				bestMetric = metrics[currentMana]
				bestGuess = currentMana
		if getMetrics:
			return metrics
		return bestGuess

	def getClassFromScreenshot(self, screenshot):
		heroes = ["Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior", "Neutral"]
		for hero in heroes:
			if 0xFF in imgToBW(screenshot.crop(self.heroLocation[hero]), self.heroThreshold):
				return hero

	def numOfCardsInScreenshot(self, screenshot):
		count = 8
		for box in self.cardPresenceTest:
			array = imgToBW(screenshot.crop(box), self.cardPresenceThreshold, image=False).reshape(-1)
			if 0 not in array:
				count -= 1
		return count

	# If you take two screenshots in the same second, they'll appear out of order when you sort them
	def reorderImages(self, imageNames):
		imageNames.sort()
		i = 0
		sortedImageNames = []
		while i < len(imageNames):
			image = imageNames[i]
			if image[-4:] == ".png":
				if image[-6:-5] == " ":
					sortedImageNames.append(imageNames[i+1])
					i += 1
				sortedImageNames.append(image)
			i += 1
		return sortedImageNames

	def getCardsFromImages(self, pathToImages):
		cards = []
		count = 0
		minMana = 0
		
		global rarities
		for name in self.reorderImages(os.listdir(pathToImages)):
			if name[-4:] == ".png":
				screenshot = Image.open(pathToImages + name)
				currentHero = self.getClassFromScreenshot(screenshot)

				for i in range(self.numOfCardsInScreenshot(screenshot)):
					card = Card(screenshot.crop(self.cardLocations[i]))
					cards.append(card)
					card.cardType = self.getCardType(card)
					card.golden = self.isGolden(card)
					card.rarity = self.getCardRarity(card)
					card.quantity = self.getCardQuantity(card)
					card.hero = currentHero
					#card.mana = self.getCardMana(card, minMana)
					if card.rarity != rarities[count]:
						card.cardImage.show()
						print "card " + str(count) + " is " + str(card.rarity) + " should be " + rarities[count]
						raw_input()
					count += 1
					print count
		return cards


if __name__ == "__main__":
	p = ScreenshotParser()
	cards = p.getCardsFromImages("./screencaps/")