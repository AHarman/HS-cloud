from bigDict import cardDict
from cardReader import Card, ScreenshotParser

class collectionAnalyser:
	sets = {  "CORE"   : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free": 133}, 
              "EXPERT1": {"Legendary": 33, "Epic": 37, "Rare": 81, "Common": 94, "Free":   0},
              "REWARD" : {"Legendary":  1, "Epic":  1, "Rare":  0, "Common":  0, "Free":   0},
              "PROMO"  : {"Legendary":  2, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
              "NAXX"   : {"Legendary":  6, "Epic":  2, "Rare":  4, "Common": 18, "Free":   0}, 
              "GVG"    : {"Legendary": 20, "Epic": 26, "Rare": 37, "Common": 40, "Free":   0},
              "BRM"    : {"Legendary":  5, "Epic":  0, "Rare": 11, "Common": 15, "Free":   0},
              "TGT"    : {"Legendary": 20, "Epic": 27, "Rare": 36, "Common": 49, "Free":   0},
              "LOE"    : {"Legendary":  5, "Epic":  2, "Rare": 13, "Common": 25, "Free":   0}}

	'''weHave = {"CORE"   : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0}, 
              "EXPERT1": {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
              "REWARD" : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
              "PROMO"  : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
              "NAXX"   : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0}, 
              "GVG"    : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
              "BRM"    : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
              "TGT"    : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0},
              "LOE"    : {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0}}'''

	weHave = {"Legendary":  0, "Epic":  0, "Rare":  0, "Common":  0, "Free":   0}

	dustVals =  {"Free"      : [   0,    0],
                 "Common"    : [  40,    5],
                 "Rare"      : [ 100,   20],
                 "Epic"      : [ 400,  100],
                 "Legendary" : [1600,  400]}
	gDustVals = {"Free"      : [   0,    0],
                 "Common"    : [ 400,   50],
                 "Rare"      : [ 800,  100],
                 "Epic"      : [1600,  400],
                 "Legendary" : [3200, 1600]}

	rarities = ["Free", "Common", "Rare", "Epic", "Legendary"]


	def getPotentialCards(cards):
		for card in cards:
			card.possibles = cardDict[card.hero][card.cardType][card.rarity][card.mana]

	if __name__ == "__main__":
		p = ScreenshotParser()
		cards = p.getCardsFromImages("./screencaps/")

		for card in cards:
			weHave[card.rarity] += 1

		getPotentialCards(cards)

		print "You have: "
		totalDust = 0
		for rarity in rarities:
			totalDust += weHave[rarity] * dustVals[rarity][0]
			print str(weHave[rarity]) + " " + rarity + " cards"
			print "Total disenchant value: " + str(totalDust)

