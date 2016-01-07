import cgi
from google.appengine.api import users
import webapp2
import lib.cloudstorage as gcs
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from cardReader import ScreenshotParser, Card
from PIL import Image

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
      <button type="button" onclick="doSomething()">Enter</button>
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

#class oneUploadHandler(blobstore_handlers.BlobstoreUploadHandler):

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, webapp2.RequestHandler):
	def post(self):
		try:
			user = users.get_current_user()
			uploads = self.get_uploads()
			uploads = self.reorderImages(uploads);
			
			user_upload = UserScreenshot(
				user=user.user_id(),
				blob_key=uploads[0].key(),
				number=0)
			user_upload.put()
			previous = user_upload.key
			for i in range(1, len(uploads)):
				upload = uploads[i]
				user_upload = UserScreenshot(
					user=user.user_id(),
					blob_key=upload.key(),
					number=i,
					parent=previous)
				user_upload.put()
				previous=user_upload.key
			print "Over here"

			self.response.write("uploaded")

			#self.redirect("/result/hereissometext")

		except Exception as e:
			print e
			self.error(500)

	def reorderImages(self, blobs):
		blobs.sort(key=lambda x: x.filename)
		sortedBlobs = []
		i = 0
		while i < len(blobs):
			blob = blobs[i]
			if blob.filename[-6:-5] == " ":
				sortedBlobs.append(blobs[i+1])
				i += 1
			sortedBlobs.append(blob)
			i += 1
		return sortedBlobs

class ResultHandler(webapp2.RequestHandler):
	def get(self, thething):
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			query = UserScreenshot.query(UserScreenshot.user == user.user_id())

			res = query.fetch(None)
			length = len(res)
			p = ScreenshotParser()
			cards = []
			if length > 0:
				for entry in res:
					blob_key = entry.blob_key
					blobstore.get(blob_key)
					reader = blobstore.BlobReader(blob_key)
					images = Image.open(reader)

					cards += p.getCardsFromImages([images])
					entry.key.delete()
					blobstore.delete(blob_key)
			
			self.response.write("You have " + str(len(cards)) + " cards")



class UserScreenshot(ndb.Model):
	user = ndb.StringProperty(indexed=True)
	blob_key = ndb.BlobKeyProperty(indexed=False)
	number = ndb.IntegerProperty(indexed=False)

class UserCollection(ndb.Model):
	user = ndb.StringProperty()
	collection = ndb.StringProperty()

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/upload', UploadHandler),
	('/result/([^/]+)?', ResultHandler),
], debug=True)
