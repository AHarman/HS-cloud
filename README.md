#A tool to analyse a [Hearthstone](playhearthstone.com) card collection

When I first created this there was no existing tool to analyse a Hearthstone card collection automatically, the only methods available required manually entering cards one-by-one which is tedious, error-prone and will have to be repeated as cards are gained and disenchanted.

Instead I created a tool to use computer vision to try and recognise cards and provide insight into a player's collection, as well as a list of the cards they own, from screenshots of their collection. It was then adapted for a project on cloud computing. As this is built for Google App Engine it can't use any C-backed libraries such as OpenCV unsupported by Google App Engine.

A live version of this project can be found [here](https://cloud-1178.appspot.com). Using this requires a Google account. Simply upload a set of screenshots of your collection as prompted and wait a minute or two to see the results. Unfortunately it currently only supports 1920x1080 screenshots.

To create a set of screenshots, start up the game and enter the collection screen. Ensure the mouse is not over any important information or any cards (I recommend keeping it placed over the "next page" button) and hit the "print screen" key. Hearthstone will save the screenshot, ignoring any "screenshot saved as..." text that may appear on the screen. Repeat this for every page.

Hearthstone may have changed their layout since this project was last updated, causing inaccurate results for new screenshots. 

Built using data from [HearthstoneJSON](https://hearthstonejson.com/).

Note: if you want a more convenient tool to use (that doesn't rely on uploading a few dozen images) [Innkeeper](http://www.innkeeper.com/) has since been created by another group.
