import pickle
import os
from urllib.parse import urlsplit

topSite = "http://hdmovie2k.co/"
url_stuff = urlsplit(topSite)

file = (os.path.join(os.path.dirname(__file__), ("logs/" + url_stuff.hostname.replace('.', '_')) + "_sources.p"))
print(file)
array = ["pickle", "dickle"]

newfile = open(file, "wb")
pickle.dump(array, newfile)
newfile.close()

newread = open(file, "rb")
newarray = pickle.load(newread)

for thing in newarray:
    print(thing)