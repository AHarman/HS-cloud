import cgi
import webapp2
import jinja2
import os
import ast
import lib.cloudstorage as gcs
from google.appengine.api import users
from google.appengine.api import taskqueue
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from PIL import Image
from cardReader import ScreenshotParser, Card
from collectionAnalyser import Analyser

# Should probably do this a better way, but then I'm not using CSS or any proper layouts
MAIN_PAGE_HTML = """\
	<script src="scripts/upload.js"></script> 
	<body>
		<h1>Hearthstone analyser</h1>
		<form method="POST" action={0} enctype="multipart/form-data">
			<label for="title">Upload screenshots </label>
			<input type="file" name="screenshot" id="files" multiple/>
			<button type="button" onclick="upload()">Upload</button>
		</form>
		<br/><br/>
		<div id="uploadStatus">
			<p>You can access your previous results <a href="/results">here</a></p>
		</div>
	</body>
</html>
"""

PROCESSING_PAGE_HTML = """\
<!DOCTYPE html>
<html>
	<meta charset="UTF-8"/>
	<script src="scripts/processing.js"></script>
	<body>
		<div id="waitingText">
			<p>Currently waiting for results. This should take less than a minute.</p>
		</div>
	</body>
</html>
"""

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			
			# Make sure we've cleared the datastore of a users old stuff, or we get blobstore errors
			collectionQuery = UserCollection.query(UserCollection.user == user.user_id())
			collectionResults = collectionQuery.fetch(1, keys_only=True)
			if collectionResults:
				screenshotQuery = UserScreenshot.query(UserScreenshot.user == user.user_id())
				ssResults = screenshotQuery.fetch(None)
				for entry in ssResults:
					#print "Deleting old data"
					blobstore.delete(entry.blob_key)
					entry.key.delete()
			else:
				userCollection = UserCollection(user=user.user_id(),
					parent=ndb.Key('UserCollection', user.user_id()))
				userCollection.put()

			# There's less than 800 cards, 1600 incl. golden, 8 per page, + 10 for half full pages
			# 200 is above what we need.
			html = "<!DOCTYPE html>\n<html>\n  <meta charset=\"UTF-8\"/>\n"
			for i in range(200):
				upload_url = blobstore.create_upload_url("/upload")
				html += "  <meta class=\"uploadLink\" upload=\"" + upload_url + "\">\n"
			self.response.out.write(html + MAIN_PAGE_HTML)
		else:
			self.redirect(users.create_login_url(self.request.uri))
		return


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, webapp2.RequestHandler):
	def post(self):
		try:
			user = users.get_current_user()
			uploads = self.get_uploads()
			user_upload = UserScreenshot(
				user=user.user_id(),
				blob_key=uploads[0].key(),
				filename=uploads[0].filename,
				index=0,
				processed=False,
				parent=ndb.Key('UserCollection', user.user_id()))
			user_upload.put()
			self.response.write("uploaded")

		except Exception as e:
			print e
			self.error(500)
		return

class ProcessingHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			try:
				query = UserScreenshot.query(ancestor=ndb.Key('UserCollection', user.user_id()))
				results = query.fetch(None)
			
				length = len(results)
				if length == 0:
					self.redirect("/")
				else:
					results = self.reorderImages(results)
					for i in range(len(results)):
						entry = results[i]
						entry.index = i;
						entry.put()
					for i in range(0, len(results), 5):
						taskqueue.add(queue_name="imageprocessing",
						              url='/worker', params={"userID": user.user_id(),
							                                 "minIndex": i,
							                                 "maxIndex": min(i + 5, len(results))})
					self.response.out.write(PROCESSING_PAGE_HTML)
			except Exception as e:
				print e
				print type(e)
				html = "<!DOCTYPE html><html><meta charset=\"UTF-8\"/>"
				html += "<h1>Something went wrong :(</h1>"
				html += "<p>Please return to our <a href=\"/\">homepage</a>.</p>"
				html += "<p>If this issue persists, please raise an issue <a href=\"https://github.com/AHarman/HS-cloud\">here</a>.</p>"
				html += "</html>"
				self.response.write(html)


		return

	def reorderImages(self, userScreenshots):
		userScreenshots.sort(key=lambda x: x.filename)
		sortedUserScreenshots = []
		i = 0
		while i < len(userScreenshots):
			blob = userScreenshots[i]
			if blob.filename[-6:-5] == " ":
				sortedUserScreenshots.append(userScreenshots[i+1])
				i += 1
			sortedUserScreenshots.append(blob)
			i += 1
		return sortedUserScreenshots

	# Because I can't get CORS to work, we're going to stick this in here as a POST.
	def post(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			query = UserScreenshot.query(UserScreenshot.processed == False,
				                         ancestor=ndb.Key('UserCollection', user.user_id()))
			results = query.fetch()
			if len(results) != 0:
				self.response.write(len(results))
			else:
				self.collateResults(user)
				self.response.write(len(results))
		return

	def collateResults(self, user):
		screenshotQuery = UserScreenshot.query(ancestor=ndb.Key('UserCollection', user.user_id()))
		screenshots = screenshotQuery.fetch(None)

		collectionQuery = UserCollection.query(UserCollection.user == user.user_id())
		collection = collectionQuery.fetch(1)[0]
		collection.collection = ""

		for screenshot in screenshots:
			collection.collection += screenshot.cards + "\n"
			screenshot.key.delete()
		collection.collection = collection.collection[:-1]
		collection.put()
		return


class ResultHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			collectionQuery = UserCollection.query(ancestor=ndb.Key('UserCollection', user.user_id()))
			collection = collectionQuery.fetch(1)
			if len(collection) == 0:
				self.shouldntBeHere()
				return
			collection = collection[0]
			if not collection.collection:
				self.shouldntBeHere()
				return
			if len(collection.collection) == 0:
				self.shouldntBeHere()
				return

			analyser = Analyser(collection.collection, stringDicts=True)
			template = JINJA_ENVIRONMENT.get_template('result.html')
			self.response.write(template.render({'analyser': analyser}))
		return

	def post(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			collectionQuery = UserCollection.query(ancestor=ndb.Key('UserCollection', user.user_id()))
			collection = collectionQuery.fetch(1)
			if len(collection) == 0:
				self.shouldntBeHere()
				return
			collection = collection[0]
			if not collection.collection:
				self.shouldntBeHere()
				return
			if len(collection.collection) == 0:
				self.shouldntBeHere()
				return
			analyser = Analyser(collection.collection, stringDicts=True)
			self.response.headers['Content-Type'] = 'application/csv'
			self.response.write(analyser.potentialCardsToCSV())
		return

	def shouldntBeHere(self):
		html = "<!DOCTYPE html><html><meta charset=\"UTF-8\"/>"
		html += "<h1>It appears we have no data for you.</h1>"
		html += "<p>Please return to our <a href=\"/\">homepage</a>.</p>"
		html += "</html>"
		self.response.write(html)
		return


class ImageProcessingWorker(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		minIndex = int(self.request.get("minIndex"))
		maxIndex = int(self.request.get("maxIndex"))
		userID = self.request.get("userID")
		query = UserScreenshot.query(UserScreenshot.index >= minIndex,
			                         UserScreenshot.index <  maxIndex,
			                         ancestor=ndb.Key('UserCollection', userID)
			                         ).order(UserScreenshot.index)

		results = query.fetch(None)
		images = []
		for entry in results:
			blob_key = entry.blob_key
			blobstore.get(blob_key)
			reader = blobstore.BlobReader(blob_key)
			image = Image.open(reader)
			image.load()
			images.append(image)

		p = ScreenshotParser()
		cards = p.getCardsFromImages(images)
		for i in range(0, len(results)):
			# Bit of a fudge here, could get the ScreenshotParser to give us how many cards per image
			results[i].cards = ""
			for j in range(i * 8, min(i*8 + 8, len(cards))):
				results[i].cards += str(cards[j].toDict()) + "\n"
			results[i].cards = results[i].cards[:-1]    # Remove last newline
			blobstore.delete(results[i].blob_key)
			results[i].processed = True
			results[i].put()
		return

class UserScreenshot(ndb.Model):
	user       = ndb.StringProperty(indexed=True)
	blob_key   = ndb.BlobKeyProperty(indexed=False)
	filename   = ndb.StringProperty(indexed=False)
	index      = ndb.IntegerProperty(indexed=True)
	processed  = ndb.BooleanProperty(indexed=True)
	cards      = ndb.TextProperty(indexed=False)

class UserCollection(ndb.Model):
	user = ndb.StringProperty()
	collection = ndb.TextProperty()

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/upload', UploadHandler),
	('/worker', ImageProcessingWorker),
	('/processing', ProcessingHandler),
	('/results', ResultHandler)
], debug=True)
