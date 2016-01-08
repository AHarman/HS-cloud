import cgi

import webapp2
import lib.cloudstorage as gcs
from google.appengine.api import users
from google.appengine.api import taskqueue
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from PIL import Image
from cardReader import ScreenshotParser, Card


#<!DOCTYPE html>
#<html>
#  <meta charset=UTF-8/>
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
    <div id="uploadStatus"></div>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
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

#class oneUploadHandler(blobstore_handlers.BlobstoreUploadHandler):

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, webapp2.RequestHandler):
	def post(self):
		try:
			user = users.get_current_user()
			uploads = self.get_uploads()
			print uploads[0].filename
			user_upload = UserScreenshot(
				user=user.user_id(),
				blob_key=uploads[0].key(),
				filename=uploads[0].filename,
				index=0,
				processed=False)
			user_upload.put()
			self.response.write("uploaded")

		except Exception as e:
			print e
			self.error(500)
		return

class ResultHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			query = UserScreenshot.query(UserScreenshot.user == user.user_id())
			results = query.fetch(None)
			
			length = len(results)
			if length == 0:
				self.redirect("/")
			else:
				userCollection = UserCollection(
					user=user.user_id(),
					collection="")
				userCollection.put()

				results = self.reorderImages(results)
				for i in range(len(results)):
					entry = results[i]
					entry.index = i;
					entry.put()
				for i in range(0, len(results), 5):
					taskqueue.add(url='/worker', params={"userID": user.user_id(),
						                                 "minIndex": i,
					 	                                 "maxIndex": min(i + 5, len(results))})

				#self.response.write("You have " + str(cards) + " cards")
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


class ImageProcessingHandler(webapp2.RequestHandler):
	def post(self):
		minIndex = int(self.request.get("minIndex"))
		maxIndex = int(self.request.get("maxIndex"))
		userID = self.request.get("userID")
		query = UserScreenshot.query(UserScreenshot.user  == userID,
			                         UserScreenshot.index >= minIndex,
			                         UserScreenshot.index <  maxIndex
			                         ).order(UserScreenshot.index)

		results = query.fetch(None)
		images = []
		for entry in results:
			try:
				blob_key = entry.blob_key
				blobstore.get(blob_key)
				reader = blobstore.BlobReader(blob_key)
				image = Image.open(reader)
				image.load()
				images.append(image)
				blobstore.delete(blob_key)
				entry.key.delete()
			except Exception as e:
				print "Database exception"
				print e
				return

		p = ScreenshotParser()
		cards = p.getCardsFromImages(images)
		print str(len(cards)) + " cards in " + str(maxIndex - minIndex) + " images"
		return

class UserScreenshot(ndb.Model):
	user      = ndb.StringProperty(indexed=True)
	blob_key  = ndb.BlobKeyProperty(indexed=False)
	filename  = ndb.StringProperty(indexed=False)
	index     = ndb.IntegerProperty(indexed=True)
	processed = ndb.BooleanProperty(indexed=False)

class UserCollection(ndb.Model):
	user = ndb.StringProperty()
	collection = ndb.TextProperty()

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/upload', UploadHandler),
	('/worker', ImageProcessingHandler),
	('/result', ResultHandler),
], debug=True)
