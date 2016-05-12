import Image
import numpy as np

def imgToBW(img, threshold, image=False):
	width, height = img.size
	imgBW = np.asarray(img.convert("L"))

	result = np.ones((height, width), dtype=np.uint8)

	for row in range(height):
		for col in range(width):
			if imgBW[row][col] > threshold:
				result[row][col] = 0xFF
			else:
				result[row][col] = 0x00
	if image:
		return Image.fromarray(result)
	return result

                # Druid
actualManas = [ 0, 0, 1, 1, 1, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 3, 3,
                3, 3, 3, 3, 4, 4, 4, 4,
                5, 5, 5, 6, 6, 6, 6, 6,
                7, 7, 8, 9,
                # Mage
                0, 1, 1, 1, 1, 1, 1, 1,
                1, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                3, 3, 3, 3, 3, 3, 3, 4,
                4, 4, 4, 5, 5, 5, 5, 6,
                7, 9,
                # Hunter
                1, 1, 1, 1, 1, 1, 1, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 4, 4,
                4, 4, 4, 4, 4, 4, 5, 5,
                5, 6, 6, 7,
                # Paladin
                1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1,
                2, 2, 2, 2, 2, 2, 3, 3,
                4, 4, 4, 4, 4, 5, 5, 5,
                3, 3, 3, 3, 3, 4, 4, 4,
                5, 5, 6, 7,
                # Priest
                0, 0, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 3, 3,
                3, 3, 3, 3, 4, 4, 4, 4,
                4, 4, 4, 5, 5, 5, 6, 6,
                7, 10,
                # Rogue
                0, 0, 1, 1, 1, 1, 1, 1,
                1, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 3,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 4, 4, 4, 4, 5, 5, 5,
                5, 5, 5, 6, 6, 7,
                # Shaman
                0, 0, 0, 1, 1, 1, 1, 1,
                1, 1, 1, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 3, 3,
                3, 3, 3, 3, 3, 4, 4, 4,
                4, 5, 5, 5, 6,
                # Warlock
                0, 0, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 3, 3, 3, 3,
                3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 5, 5, 5, 6, 6, 6,
                6, 6, 7, 9,
                #Warrior
                0, 1, 1, 1, 1, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                2, 3, 3, 3, 3, 3, 3, 3,
                3, 4, 4, 4, 4, 4, 4, 5,
                5, 6, 6, 6, 7, 7, 7,
                #Neutral
                0, 0, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                2, 2, 2, 2, 2, 2, 2, 2,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 3, 3,
                3, 3, 3, 3, 3, 3, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 4,
                4, 4, 4, 5, 5, 5, 5, 5,
                5, 5, 5, 5, 5, 5, 5, 5,
                5, 5, 5, 5, 5, 5, 5, 5,
                5, 5, 5, 5, 5, 5, 5, 5,
                5, 5, 6, 6, 6, 6, 6, 6,
                6, 6, 6, 6, 6, 6, 6, 6,
                6, 6, 7, 7, 7, 7, 7, 8,
                8, 8, 9, 9, 9, 20]
                # Druid
actualTypes = [ "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Spell",  "Spell",  "Minion", "Minion", "Minion", "Spell",  "Spell",
                "Spell",  "Spell",  "Minion", "Minion", "Spell",  "Spell",  "Spell",  "Minion",
                "Spell",  "Minion", "Minion", "Spell",  "Spell",  "Spell",  "Spell",  "Minion",
                "Minion", "Minion", "Minion", "Minion",

                # Hunter
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Minion", "Minion",
                "Minion", "Weapon", "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Minion", "Minion",
                "Weapon", "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Spell",
                "Minion", "Minion", "Minion", "Spell",  "Minion", "Minion", "Minion", "Minion",
                "Weapon", "Minion",

                # Mage
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Spell",
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Minion", "Minion",
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Spell",  "Minion", "Minion", "Minion", "Minion", "Spell",  "Spell",
                "Spell",  "Spell",  "Minion", "Minion", "Minion", "Minion", "Spell",  "Spell",
                "Minion", "Spell",  "Spell",  "Spell",

                # Paladin
                "Weapon", "Weapon", "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Minion", "Weapon", "Spell",
                "Spell",  "Spell",  "Minion", "Minion", "Minion", "Spell",  "Spell",  "Minion",
                "Spell",  "Spell",  "Minion", "Minion", "Minion", "Weapon", "Spell",  "Spell",
                "Minion", "Minion", "Spell",  "Minion",

                #Priest
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Spell",  "Minion", "Minion", "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Spell",  "Minion", "Minion", "Minion", "Minion", "Spell",  "Spell",
                "Spell",  "Spell",  "Spell",  "Minion", "Spell",  "Spell",  "Spell",  "Minion",
                "Minion", "Minion", "Minion", "Spell",  "Spell",  "Minion", "Spell",  "Minion",
                "Minion", "Spell",

                # Rogue
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion",
                "Minion", "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion",
                "Minion", "Minion", "Minion", "Minion", "Minion", "Minion", "Minion", "Weapon",
                "Weapon", "Weapon", "Spell",  "Spell",  "Spell",  "Minion", "Minion", "Minion",
                "Minion", "Spell",  "Spell",  "Minion", "Minion", "Weapon", "Weapon", "Spell",
                "Minion", "Minion", "Minion", "Spell",  "Spell",  "Spell",

                # Shaman
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",
                "Minion", "Minion", "Minion", "Weapon", "Spell",  "Spell",  "Spell",  "Spell",
                "Spell",  "Minion", "Minion", "Minion", "Minion", "Minion", "Weapon", "Spell",
                "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Minion", "Minion", "Minion",
                "Minion", "Spell",  "Minion", "Minion", "Minion",
               
                # Warlock
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion",
                "Minion", "Minion", "Minion", "Spell",  "Spell",  "Spell",  "Spell",  "Minion",
                "Minion", "Minion", "Minion", "Minion", "Spell",  "Spell",  "Spell",  "Spell",
                "Minion", "Minion", "Minion", "Spell",  "Spell",  "Spell",  "Minion", "Minion",
                "Minion", "Minion", "Minion", "Minion", "Minion", "Spell",  "Minion", "Minion",
                "Minion", "Minion", "Minion", "Minion",

                # Warrior
                "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Weapon", "Spell",  "Spell",
                "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Minion",
                "Minion", "Weapon", "Spell",  "Spell",  "Spell",  "Spell",  "Minion", "Minion",
                "Minion", "Weapon", "Spell",  "Minion", "Minion", "Minion", "Minion", "Weapon",
                "Minion", "Minion", "Minion", "Minion", "Weapon", "Spell",  "Minion"]

            # Druid
rarities = ["Free",      "Free",      "Free",      "Free",      "Common",    "Free",      "Free",      "Common",
            "Free",      "Free",      "Common",    "Common",    "Common",    "Common",    "Free",      "Free",  
            "Common",    "Free",      "Common",    "Common",    "Common",    "Common",    "Free",      "Common",  
            "Rare",      "Common",    "Common",    "Epic",      "Rare",      "Rare",      "Free",      "Rare",
            "Epic",      "Epic",      "Free",      "Rare",

            # Hunter
            "Free",      "Free",      "Free",      "Free",      "Free",      "Common",    "Free",      "Free",  
            "Common",    "Common",    "Common",    "Rare",      "Rare",      "Common",    "Epic",      "Rare",
            "Rare",      "Common",    "Common",    "Epic",      "Common",    "Common",    "Common",    "Epic",
            "Rare",      "Free",      "Common",    "Free",      "Rare",      "Common",    "Rare",      "Free",  
            "Rare",      "Free",      "Free",      "Common",    "Rare",      "Free",      "Free",      "Rare",
            "Epic",      "Legendary",

            # Mage
            "Epic",      "Free",      "Free",      "Common",    "Free",      "Free",      "Common",    "Free",  
            "Free",      "Common",    "Free",      "Free",      "Rare",      "Rare",      "Common",    "Common",
            "Free",      "Free",      "Rare",      "Common",    "Common",    "Free",      "Free",      "Common",
            "Common",    "Rare",      "Rare",      "Rare",      "Rare",      "Rare",      "Common",    "Epic",
            "Free",      "Free",      "Common",    "Rare",      "Rare",      "Free",      "Common",    "Common",
            "Common",    "Rare",      "Rare",      "Free",

            # Paladin
            "Free",      "Free",      "Common",    "Free",      "Common",    "Rare",      "Common",    "Free",
            "Free",      "Free",      "Free",      "Common",    "Common",    "Common",    "Common",    "Common",
            "Rare",      "Free",      "Free",      "Common",    "Common",    "Common",    "Epic",      "Rare",
            "Rare",      "Common",    "Rare",      "Rare",      "Common",    "Free",      "Free",      "Free",
            "Free",      "Free",      "Common",    "Common",    "Common",    "Rare",      "Common",    "Rare",
            "Rare",      "Epic",      "Epic",      "Free",

            # Priest
            "Common",    "Common",    "Common",    "Free",      "Free",      "Common",    "Rare",      "Free",
            "Common",    "Free",      "Free",      "Common",    "Free",      "Free",      "Free",      "Free",
            "Rare",      "Free",      "Rare",      "Rare",      "Common",    "Rare",      "Free",      "Epic",
            "Common",    "Common",    "Common",    "Common",    "Rare",      "Epic",      "Rare",      "Common",
            "Common",    "Common",    "Rare",      "Rare",      "Free",      "Rare",      "Rare",      "Common",
            "Legendary", "Free",

            # Rogue
            "Free",      "Common",    "Common",    "Common",    "Free",      "Free",      "Free",      "Common",
            "Common",    "Common",    "Rare",      "Common",    "Common",    "Free",      "Free",      "Rare",
            "Common",    "Common",    "Common",    "Common",    "Rare",      "Epic",      "Common",    "Epic",
            "Rare",      "Rare",      "Epic",      "Free",      "Free",      "Rare",      "Rare",      "Rare",
            "Rare",      "Epic",      "Common",    "Common",    "Rare",      "Free",      "Free",      "Free",
            "Rare",      "Rare",      "Common",    "Free",      "Free",      "Free",

            # Shaman
            "Free",      "Free",      "Free",      "Common",    "Common",    "Free",      "Common",    "Free",
            "Common",    "Common",    "Common",    "Common",    "Rare",      "Common",    "Rare",      "Common",
            "Free",      "Free",      "Common",    "Rare",      "Rare",      "Common",    "Rare",      "Rare",
            "Rare",      "Free",      "Rare",      "Rare",      "Common",    "Rare",      "Common",    "Common",
            "Free",      "Free",      "Epic",      "Rare",      "Free",

            # Warlock
            "Free",      "Free",      "Free",      "Free",      "Common",    "Common",    "Free",      "Common",
            "Common",    "Rare",      "Free",      "Common",    "Common",    "Common",    "Common",    "Common",
            "Rare",      "Free",      "Rare",      "Common",    "Rare",      "Free",      "Common",    "Free",
            "Rare",      "Common",    "Rare",      "Free",      "Rare",      "Rare",      "Rare",      "Epic",
            "Common",    "Common",    "Rare",      "Common",    "Common",    "Rare",      "Epic",      "Free",
            "Free",      "Rare",      "Common",    "Legendary",

            # Warrior
            "Common",    "Free",      "Rare",      "Free",      "Common"   , "Free",      "Common",    "Common",
            "Free",      "Free",      "Free",      "Rare",      "Common",    "Common",    "Rare",      "Common",
            "Rare",      "Common",    "Free",      "Free",      "Free",      "Free",      "Common",    "Common",
            "Free",      "Common",    "Rare",      "Common",    "Common",    "Free",      "Rare",      "Free",
            "Rare",      "Epic",      "Rare",      "Rare",      "Epic",      "Epic",      "Common",

            # Neutral
            "Rare",      "Common",    "Common",    "Common",    "Rare",      "Common",    "Common",    "Rare",
            "Free",      "Common",    "Free",      "Free",      "Rare",      "Common",    "Rare",      "Free",
            "Rare",      "Rare",      "Common",    "Common",    "Free",      "Common",    "Common",    "Free",
            "Common",    "Common",    "Common",    "Free",      "Common",    "Common",    "Rare",      "Free",
            "Common",    "Free",      "Common",    "Common",    "Epic",      "Common",    "Common",    "Common",
            "Common",    "Free",      "Common",    "Common",    "Common",    "Common",    "Common",    "Rare",
            "Free",      "Common",    "Common",    "Common",    "Common",    "Rare",      "Rare",      "Rare",
            "Common",    "Common",    "Common",    "Free",      "Common",    "Rare",      "Free",      "Rare",
            "Common",    "Epic",      "Free",      "Common",    "Common",    "Rare",      "Common",    "Common",
            "Common",    "Rare",      "Rare",      "Common",    "Common",    "Epic",      "Legendary", "Rare",
            "Rare",      "Free",      "Common",    "Rare",      "Rare",      "Common",    "Common",    "Rare",
            "Common",    "Common",    "Common",    "Rare",      "Rare",      "Common",    "Common",    "Rare",
            "Rare",      "Rare",      "Free",      "Free",      "Common",    "Rare",      "Free",      "Rare",
            "Common",    "Common",    "Rare",      "Common",    "Free",      "Free",      "Rare",      "Common",
            "Epic",      "Free",      "Common",    "Common",    "Free",      "Epic",      "Epic",      "Common",
            "Common",    "Common",    "Common",    "Common",    "Legendary", "Free",      "Common",    "Rare",
            "Rare",      "Rare",      "Rare",      "Rare",      "Legendary", "Common",    "Free",      "Common",
            "Common",    "Rare",      "Common",    "Free",      "Common",    "Common",    "Common",    "Free",
            "Common",    "Rare",      "Rare",      "Common",    "Common",    "Common",    "Common",    "Free",
            "Free",      "Common",    "Common",    "Free",      "Common",    "Common",    "Free",      "Common",
            "Common",    "Rare",      "Rare",      "Common",    "Common",    "Rare",      "Common",    "Rare",
            "Free",      "Common",    "Free",      "Epic",      "Epic",      "Legendary", "Free",      "Rare",
            "Free",      "Common",    "Legendary", "Rare",      "Rare",      "Common",    "Free",      "Common",
            "Common",    "Common",    "Rare",      "Common",    "Common",    "Legendary", "Free",      "Common",
            "Rare",      "Common",    "Free",      "Free",      "Common",    "Legendary", "Common",    "Legendary",
            "Free",      "Legendary", "Epic",      "Common",    "Free",      "Legendary", "Legendary", "Legendary",
            "Common",    "Common",    "Free",      "Rare",      "Legendary", "Free",      "Free",      "Legendary",
            "Common",    "Legendary", "Legendary", "Legendary", "Common",    "Epic"]
                  # Druid
minionAttacks = [ 2, 2, 2,
                  2, 3, 4,
                  4, 4, 7,
                  5, 5, 8, 7,
                  2, 1, 1,
                  # Hunter
                  1,
                  3, 2, 2,
                  3,
                  4, 4, 4, 2, 3, 2, 6,
                  8,
                  1,
                  3, 2, 3,
                  2, 4, 3, 3,
                  3, 3, 5, 3, 6,
                  # Paladin
                  2, 2,
                  4, 4, 2,
                  3, 3, 3, 6,
                  5, 2, 5,
                  # Priest
                  1, 2,
                  0, 2, 3, 1,
                  3, 3,
                  0, 0, 5, 5, 6,
                  7,
                  # Rogue
                  2,
                  2, 2,
                  2, 2, 3, 3, 4, 1, 3,
                  2, 4, 3,
                  3, 5, 4,
                  4, 6, 3,
                  # Shaman
                  3, 3, 1,
                  0, 3, 0, 0, 3,
                  2, 5, 3, 2,
                  3, 7, 3, 6,
                  0,
                  3, 1, 1, 2,
                  1, 4, 3, 4,
                  3, 2, 3, 3, 5,
                  0, 3, 5, 4, 4, 9, 6,
                  6, 5, 6, 9,
                  # Warrior
                  1,
                  1, 2,
                  3, 3, 3,
                  2, 3, 2, 4, 2,
                  5, 6, 5, 5, 7,
                  #Neutral
                  0, 1, 2, 1, 1, 2, 1, 0,
                  1, 1, 1, 1, 2, 2, 1, 2,
                  1, 1, 0, 2, 1, 2, 1, 2,
                  2, 1, 2, 3, 2, 1, 2, 3,
                  2, 2, 3, 2, 1, 1, 1, 3,
                  2, 2, 2, 2, 1, 2, 1, 3,
                  2, 1, 2, 3, 2, 1, 2, 1,
                  2, 2, 1, 2, 1, 0, 1, 2,
                  3, 3, 2, 2, 2, 2, 1, 3,
                  1, 0, 4, 2, 2, 3, 2, 2,
                  2, 1, 4, 2, 1, 3, 3, 2,
                  2, 1, 1, 3, 2, 2, 5, 2,
                  1, 4, 2, 3, 4, 4, 5, 3,
                  4, 4, 2, 3, 2, 2, 4, 3,
                  2, 3, 2, 3, 1, 3, 3, 3,
                  1, 2, 2, 3, 3, 3, 5, 2,
                  7, 2, 5, 5, 1, 3, 4, 4,
                  4, 2, 3, 2, 3, 5, 2, 2,
                  5, 1, 4, 5, 2, 4, 1, 2,
                  4, 4, 3, 3, 3, 4, 2, 3,
                  1, 3, 3, 3, 4, 4, 5, 3,
                  5, 5, 4, 4, 3, 4, 4, 3,
                  2, 4, 5, 5, 5, 4, 4, 5,
                  7, 4, 3, 4, 4, 7, 4, 5,
                  0, 7, 4, 6, 6, 5, 5, 3,
                  6, 2, 6, 5, 5, 4, 4, 5,
                  6, 4, 9, 7, 8, 6, 7, 6,
                  7, 6, 9, 8, 9, 8]

minionHealths = []

frees   = len([x for x in rarities if x == "Free"])
commons = len([x for x in rarities if x == "Common"])
rares   = len([x for x in rarities if x == "Rare"])
epics   = len([x for x in rarities if x == "Epic"])
legendaries = 1