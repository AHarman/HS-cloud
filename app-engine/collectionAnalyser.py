from bigDict import cardDict
from cardReader import Card, ScreenshotParser
import ast

if __name__ == "__main__":
	import os
	import Image

class Analyser:
	sets = {"CORE"   : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free": 133}, 
	        "EXPERT1": {"Legendary": 33, "Epic": 37, "Rare": 81, "Common": 94, "Free":   0},
	        "REWARD" : {"Legendary":  1, "Epic":  1, "Rare":  0, "Common":  0, "Free":   0},
	        "PROMO"  : {"Legendary":  2, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
	        "NAXX"   : {"Legendary":  6, "Epic":  2, "Rare":  4, "Common": 18, "Free":   0}, 
	        "GVG"    : {"Legendary": 20, "Epic": 26, "Rare": 37, "Common": 40, "Free":   0},
	        "BRM"    : {"Legendary":  5, "Epic":  0, "Rare": 11, "Common": 15, "Free":   0},
	        "TGT"    : {"Legendary": 20, "Epic": 27, "Rare": 36, "Common": 49, "Free":   0},
	        "LOE"    : {"Legendary":  5, "Epic":  2, "Rare": 13, "Common": 25, "Free":   0}}

	dustVals  = {"Free"      : [   0,    0],
	             "Common"    : [  40,    5],
	             "Rare"      : [ 100,   20],
	             "Epic"      : [ 400,  100],
	             "Legendary" : [1600,  400]}
	gDustVals = {"Free"      : [   0,    0],
	             "Common"    : [ 400,   50],
	             "Rare"      : [ 800,  100],
	             "Epic"      : [1600,  400],
	             "Legendary" : [3200, 1600]}

	listrarities = ["Free", "Common", "Rare", "Epic", "Legendary"]
	listheroes = ["Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior", "Neutral"]

	#stringDicts=true means that cards is a set of dicts in string form, newline seperated
	def __init__(self, cards, stringDicts=False):
		if stringDicts:
			self.cards = []
			cards = str(cards)

			for card in cards.split("\n"):
				self.cards.append(Card.fromDict(ast.literal_eval(card)))
		else:
			self.cards = cards
		self.gRarities = {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0}
		self.rarities  = {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0}
		self.classCount = {"Druid"  : [0, 0],
		                   "Hunter" : [0, 0],
		                   "Mage"   : [0, 0],
		                   "Paladin": [0, 0],
		                   "Priest" : [0, 0],
		                   "Rogue"  : [0, 0],
		                   "Shaman" : [0, 0],
		                   "Warlock": [0, 0],
		                   "Warrior": [0, 0],
		                   "Neutral": [0, 0]}
		self.classDust =  {"Druid"  : [0, 0],
		                   "Hunter" : [0, 0],
		                   "Mage"   : [0, 0],
		                   "Paladin": [0, 0],
		                   "Priest" : [0, 0],
		                   "Rogue"  : [0, 0],
		                   "Shaman" : [0, 0],
		                   "Warlock": [0, 0],
		                   "Warrior": [0, 0],
		                   "Neutral": [0, 0]}
		self.classRarity =  {"Druid"  : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Hunter" : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Mage"   : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Paladin": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Priest" : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Rogue"  : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Shaman" : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Warlock": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Warrior": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Neutral": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0}}
		self.gClassRarity = {"Druid"  : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Hunter" : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Mage"   : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Paladin": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Priest" : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Rogue"  : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Shaman" : {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Warlock": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Warrior": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0},
		                     "Neutral": {"Legendary": 0, "Epic": 0, "Rare": 0, "Common": 0, "Free": 0}}
		self.disenchantValue = 0
		self.enchantValue = 0
		self.cardKnowledge = []
		
		self.numCards = len(self.cards)
		self.goldCards = 0
		for card in self.cards:
			if card.golden:
				self.goldCards += 1

		self.findRarities()
		self.findDustValues()
		self.findPotentialCards()
		for hero in self.listheroes:
			for rarity in self.listrarities:
				self.classCount[hero][0] += self.classRarity[hero][rarity]
				self.classCount[hero][1] += self.gClassRarity[hero][rarity]
		return

	def findDustValues(self):
		for rarity in self.listrarities:
			self.enchantValue    += self.dustVals[ rarity][0] * self.rarities[ rarity]
			self.enchantValue    += self.gDustVals[rarity][0] * self.gRarities[rarity]
			self.disenchantValue += self.dustVals[ rarity][1] * self.rarities[ rarity]
			self.disenchantValue += self.gDustVals[rarity][1] * self.gRarities[rarity]
			for hero in self.listheroes:
				self.classDust[hero][0] += self.dustVals[ rarity][0] * self.classRarity[ hero][rarity]
				self.classDust[hero][1] += self.gDustVals[rarity][1] * self.gClassRarity[hero][rarity]
		return

	def findRarities(self):
		for card in self.cards:
			if card.golden:
				self.gRarities[card.rarity] += 1
				self.gClassRarity[card.hero][card.rarity] += 1
			else:
				self.rarities[card.rarity] += 1
				self.classRarity[card.hero][card.rarity] += 1
		return

	def cardsSame(self, card1, card2):
		if (card1.hero == card2.hero and
			card1.golden == card2.golden and
			card1.cardType == card2.cardType and
			card1.rarity == card2.rarity and
			card1.mana == card2.mana and
			card1.quantity == card2.quantity):
			return True
		return False

	def findPotentialCards(self):
		overlaps = []
		tempList = []

		cards = list(self.cards)
		cap = len(cards)
		i = 0
		while i < cap:
			tempList.append(cards[i])
			overlaps.append(0)
			for j in reversed(range(i, len(cards))):
				if self.cardsSame(cards[i], cards[j]):
					overlaps[-1] += 1
					cards.pop(j)
					cap -= 1
			i += 1

		for i in range(len(tempList)):
			card = tempList[i]
			possibilities = [x["Name"] for x in cardDict[card.hero][card.cardType][card.rarity][card.mana]]
			self.cardKnowledge.append({"names":    possibilities,
			                           "hero":     card.hero,
			                           "mana":     card.mana, 
			                           "rarity":   card.rarity,
			                           "cardType": card.cardType,
			                           "quantity": card.quantity, 
			                           "golden":   card.golden,
			                           "overlaps": overlaps[i]})
		return

	def potentialCardsToCSV(self):
		csv = "[Table 1]\n"
		csv += "Potential cards,Class,Mana,Rarity,Type,Quantity,Golden?,Overlaps\n"
		for hero in self.listheroes:
			for mana in range(11) + [12, 20]:
				for card in [x for x in self.cardKnowledge if (x["hero"] == hero and x["mana"] == mana)]:
					for cardName in card["names"][:-1]:
						csv += cardName + "/"
					csv +=     card["names"][-1] + ","
					csv +=     card["hero"]      + ","
					csv += str(card["mana"])     + ","
					csv +=     card["rarity"]    + ","
					csv +=     card["cardType"]  + ","
					csv += str(card["quantity"]) + ","
					csv += str(card["golden"])   + ","
					csv += str(card["overlaps"]) + "\n"
		return csv

def reorderImages(imageNames):
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


if __name__ == "__main__":
	images = []
	for name in reorderImages(os.listdir("../screencaps/")):
		if name[-4:] == ".png":
			images.append(Image.open("../screencaps/" + name))

	p = ScreenshotParser()
	cards = p.getCardsFromImages(images)
	analyser = Analyser(cards)
	analyser.findPotentialCards()
	print analyser.potentialCardsToCSV()
	