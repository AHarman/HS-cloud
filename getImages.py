from HTMLParser import HTMLParser
import urllib
import json
import os

cards = []

def saveCard(name, url):
	print name
	filename = "./cardImages/" + name + ".png"
	urllib.urlretrieve(url, filename)

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.imageURL = None
		self.imageName = None
		self.inName = False

	def handle_starttag(self, tag, attrs):
		if tag == "img" and attrs[0] == ("class", "hscard-static"):
			for attr in attrs:
				if attr[0] == "data-imageurl":
					self.imageURL = attr[1]
			print self.imageURL
		elif self.imageURL != None and tag == "h3":
			self.inName = True;
		#elif inName and tag == "a":
		#	inName = True;
	def handle_endtag(self, tag):
		return

	def handle_data(self, data):
		if self.inName:
			saveCard(data, self.imageURL)
			self.inName = False
			self.imageURL = None
			self.imageName = None

parser = MyHTMLParser()
for i in range(1, 9):
	url = "http://www.hearthpwn.com/cards?display=2&filter-premium=1&page=" + str(i)
	html = urllib.urlopen(url).read()
	parser.feed(html)

with open("cards.collectible.json", "r") as f:
	cardsJSON = json.loads(f.read())

#print json.dumps(cardsJSON, sort_keys=True, indent=4, separators=(',', ': '))
jsonNames = []
for card in cardsJSON:
	jsonNames.append(str(card["name"]))

jsonNames = sorted(jsonNames)

imageNames = sorted([x[:-4] for x in os.listdir("./cardImages/")])


print "\nThese cards might be missing (or it might be a typo)"
for card in jsonNames:
	if card not in imageNames:
		print card

print "\nThese files we have, but aren't in the JSON"

for card in imageNames:
	if card not in jsonNames:
		print card