import json

with open("cards.collectible.json", "r") as f:
	cardsJSON = json.loads(f.read())

# Levels: Hero, type, rarity, cost
playerClasses = ["Druid", "Hunter", "Mage", "Paladin", "Priest", "Rogue", "Shaman", "Warlock", "Warrior", "Neutral"]
cardTypes     = ["Minion", "Spell", "Weapon"]
rarities      = ["Free", "Common", "Rare", "Epic", "Legendary"]
costs         = range(11) + [12, 20]

cards = {}

minAttack = []
minHealth = []
wepAttack = []
wepDurab = []

# Get all the values to build up our card "database"
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

# Build the structure of our card "database"
for playerClass in playerClasses:
	cards[playerClass] = {}
	for cardType in cardTypes:
		cards[playerClass][cardType] = {}
		for rarity in rarities:
			cards[playerClass][cardType][rarity] = {}
			for cost in costs:
				if cardType == "Spell":
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

# Fill out our "database"
for card in cardsJSON:
	if "playerClass" not in card:
		playerClass = "Neutral"
	else:
		playerClass = str(card["playerClass"])
	cardType = str(card["type"])
	rarity = str(card["rarity"])
	cost = int(card["cost"])
	if card["type"] == "Spell":
		cards[playerClass][cardType][rarity][cost].append(str(card["name"]))
	elif card["type"] == "Minion":
		attack = int(card["attack"])
		health = int(card["health"])
		cards[playerClass][cardType][rarity][cost][attack][health].append(str(card["name"]))
	elif card["type"] == "Weapon":
		attack = int(card["attack"])
		durability = int(card["durability"])
		cards[playerClass][cardType][rarity][cost][attack][durability].append(str(card["name"]))

# Most confusing part. I'm just removing empty sections because there's no point keeping them
for playerClass in playerClasses:
	for cardType in cardTypes:
		for rarity in rarities:
			for cost in costs:
				if cardType == "Minion":
					for attack in minAttack:
						for health in minHealth:
							if len(cards[playerClass][cardType][rarity][cost][attack][health]) == 0:
								del cards[playerClass][cardType][rarity][cost][attack][health]
						if len(cards[playerClass][cardType][rarity][cost][attack].keys()) == 0:
							del cards[playerClass][cardType][rarity][cost][attack]
					if len(cards[playerClass][cardType][rarity][cost].keys()) == 0:
						del cards[playerClass][cardType][rarity][cost]
				elif cardType == "Weapon":
					for attack in wepAttack:
						for durability in wepDurab:
							if len(cards[playerClass][cardType][rarity][cost][attack][durability]) == 0:
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

# Just so I can see how long things are
maxLen = 0
longest = []
meanLen = 0
count = 0
allLens = []
for playerClass in playerClasses:
	for cardType in cards[playerClass].keys():
		for rarity in cards[playerClass][cardType].keys():
			for cost in cards[playerClass][cardType][rarity].keys():
				if cardType == "Minion":
					for attack in cards[playerClass][cardType][rarity][cost].keys():
						for health in cards[playerClass][cardType][rarity][cost][attack].keys():
							length = len(cards[playerClass][cardType][rarity][cost][attack][health])
							meanLen += length
							count += 1
							allLens.append(length)
							if length > maxLen:
								maxLenMin = length
								longest = [playerClass, cardType, rarity, cost, attack, health]
				elif cardType == "Weapon":
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
print maxLen
print longest
print meanLen
print sorted(allLens)

print cards