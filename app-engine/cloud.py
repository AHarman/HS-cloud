import cgi
from google.appengine.api import users
import webapp2
import lib.cloudstorage as gcs
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from cardReader import ScreenshotParser, Card
from PIL import Image

MAIN_PAGE_HTML = """\
<html>
  <meta charset="UTF-8"/>
  <body>
    <h1>Hearthstone analyser</h1>
    <form action="{0}" method="POST" enctype="multipart/form-data">
      <label for="title">Upload screenshots </label>
      <input type="file" name="screenshot" id="screenshot" multiple/>
      <input type="submit" name="upload" value="Upload">
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            upload_url = blobstore.create_upload_url('/upload')
            self.response.out.write(MAIN_PAGE_HTML.format(upload_url))
        else:
            self.redirect(users.create_login_url(self.request.uri))


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
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
            print user_upload.key
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

            self.redirect("/result/hereissometext")

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
            images = []
            p = ScreenshotParser()
            cards = 0
            if length > 0:
                for entry in res:
                    blob_key = entry.blob_key
                    blobstore.get(blob_key)
                    reader = blobstore.BlobReader(blob_key)
                    images.append(Image.open(reader))
                    entry.key.delete()
            cards = p.getCardsFromImages(images)
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
