import json
import pprint

# Get this file from https://hearthstonejson.com/
with open("cards.collectible.json", "r") as f:
	cardsJSON = json.loads(f.read())

# Levels in tree: Hero, type, rarity, cost
playerClasses = ["Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior", "Neutral"]
cardTypes     = ["Minion", "Spell", "Weapon"]
rarities      = ["Free", "Common", "Rare", "Epic", "Legendary"]
costs         = range(11) + [12, 20]

# Tree dictionary
cards = {}

minAttack = []
minHealth = []
wepAttack = []
wepDurab = []

# Whether to use minion attack/health and weapon attack/durability
usingAttributes = False

# Get all the values to build up our card tree
if usingAttributes:
	for card in cardsJSON:
		if card["type"] == "Minion":
			if int(card["attack"]) not in minAttack:
				minAttack.append(int(card["attack"]))
			if int(card["health"]) not in minHealth:
				minHealth.append(int(card["health"]))

		if card["type"] == "Weapon":
			if int(card["attack"]) not in wepAttack:
				wepAttack.append(int(card["attack"]))
			if int(card["durability"]) not in wepDurab:
				wepDurab.append(int(card["durability"]))


# Build the structure of our card tree
for playerClass in playerClasses:
	cards[playerClass] = {}
	for cardType in cardTypes:
		cards[playerClass][cardType] = {}
		for rarity in rarities:
			cards[playerClass][cardType][rarity] = {}
			for cost in costs:
				if cardType == "Spell" or not usingAttributes:
					cards[playerClass][cardType][rarity][cost] = []
				elif cardType == "Minion":
					cards[playerClass][cardType][rarity][cost] = {}
					for attack in minAttack:
						cards[playerClass][cardType][rarity][cost][attack] = {}
						for health in minHealth:
							cards[playerClass][cardType][rarity][cost][attack][health] = []
				elif cardType == "Weapon":
					cards[playerClass][cardType][rarity][cost] = {}
					for attack in wepAttack:
						cards[playerClass][cardType][rarity][cost][attack] = {}
						for durability in wepDurab:
							cards[playerClass][cardType][rarity][cost][attack][durability] = []

# Fill out our tree
for card in cardsJSON:
	if "playerClass" not in card:
		playerClass = "Neutral"
	else:
		playerClass = str(card["playerClass"])
	cardType = str(card["type"])
	
	if card["set"] == "CORE":
		rarity = "Free"
	else:
		rarity = str(card["rarity"])
	
	cost = int(card["cost"])

	myCard = {"Name": str(card["name"]), "Set": str(card["set"])}
	if card["type"] == "Spell" or not usingAttributes:
		cards[playerClass][cardType][rarity][cost].append(myCard)
	elif card["type"] == "Minion":
		attack = int(card["attack"])
		health = int(card["health"])
		cards[playerClass][cardType][rarity][cost][attack][health].append(myCard)
	elif card["type"] == "Weapon":
		attack = int(card["attack"])
		durability = int(card["durability"])
		cards[playerClass][cardType][rarity][cost][attack][durability].append(myCard)

# Most confusing part. I'm just removing empty branches because there's no point keeping them
for playerClass in playerClasses:
	for cardType in cardTypes:
		for rarity in rarities:
			for cost in costs:

				if cardType == "Minion" and usingAttributes:
					for attack in minAttack:
						for health in minHealth:
							if len(cards[playerClass][cardType][rarity][cost][attack][health]) == 0:
								del cards[playerClass][cardType][rarity][cost][attack][health]
						if len(cards[playerClass][cardType][rarity][cost][attack].keys()) == 0:
							del cards[playerClass][cardType][rarity][cost][attack]
					if len(cards[playerClass][cardType][rarity][cost].keys()) == 0:
						del cards[playerClass][cardType][rarity][cost]

				elif cardType == "Weapon" and usingAttributes:
					for attack in wepAttack:
						for durability in wepDurab:
							if len(cards[palyerClass][cardType][rarity][cost][attack][durability]) == 0:
								del cards[playerClass][cardType][rarity][cost][attack][durability]
						if len(cards[playerClass][cardType][rarity][cost][attack].keys()) == 0:
							del cards[playerClass][cardType][rarity][cost][attack]
					if len(cards[playerClass][cardType][rarity][cost].keys()) == 0:
						del cards[playerClass][cardType][rarity][cost]
				else:
					if len(cards[playerClass][cardType][rarity][cost]) == 0:
						del cards[playerClass][cardType][rarity][cost]

			if len(cards[playerClass][cardType][rarity].keys()) == 0:
				del cards[playerClass][cardType][rarity]
		if len(cards[playerClass][cardType].keys()) == 0:
				del cards[playerClass][cardType]

# This last bit is just so I can get those nice stats on the size of this thing at the end.
maxLen = 0
longest = []
meanLen = 0
count = 0
allLens = []
for playerClass in playerClasses:
	for cardType in cards[playerClass].keys():
		for rarity in cards[playerClass][cardType].keys():
			for cost in cards[playerClass][cardType][rarity].keys():
				if cardType == "Minion" and usingAttributes:
					for attack in cards[playerClass][cardType][rarity][cost].keys():
						for health in cards[playerClass][cardType][rarity][cost][attack].keys():
							length = len(cards[playerClass][cardType][rarity][cost][attack][health])
							meanLen += length
							count += 1
							allLens.append(length)
							if length > maxLen:
								maxLenMin = length
								longest = [playerClass, cardType, rarity, cost, attack, health]
				elif cardType == "Weapon" and usingAttributes:
					for attack in cards[playerClass][cardType][rarity][cost].keys():
						for durability in cards[playerClass][cardType][rarity][cost][attack].keys():
							length = len(cards[playerClass][cardType][rarity][cost][attack][durability])
							meanLen += length
							count += 1
							allLens.append(length)
							if length > maxLen:
								maxLen = length
								longest = [playerClass, cardType, rarity, cost, attack, durability]
				else:
					length = len(cards[playerClass][cardType][rarity][cost])
					meanLen += len(cards[playerClass][cardType][rarity][cost])
					count += 1
					allLens.append(length)
					if length > maxLen:
						maxLen = length
						longest = [playerClass, cardType, rarity, cost]

meanLen = float(meanLen) / float(count)
print "There are " + str(count) + " collectible cards in hearthstone"
print "Most cards in one leaf: " + str(maxLen)
print "This is said leaf: " + str(longest)
print "Mean leaf length: " + str(meanLen)
print "Lengths of all leaves (sorted): "
print sorted(allLens)
print "Actual tree: "
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(cards)
