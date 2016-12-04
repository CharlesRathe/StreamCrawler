from selenium import webdriver
from urllib.parse import urlsplit
import time, os
from Helper import recurse_get_sources
import pickle

# Get list of top level URL's (hand compiled?) to be searched
with open("SiteList.txt") as f:
    topSites = f.readlines()

try:
    # Set up WebDriver with Firefox
    driver = webdriver.Chrome("C:\Python35-32\selenium\chromedriver.exe")
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
except:
    print("Couldn't load webdriver")


# Go through all top level domains
for topSite in topSites:

    # Set variables
    done = 0
    t = time.time()

    try:
        # Init Lists
        sources = []
        links = []
        alreadyVisited = set([])
        iFrameSources = []
        videoSources = []
        errors = 0
    except:
        print("Clearing resources")
        del videoSources
        del links
        del iFrameSources
        del alreadyVisited
        del sources
        errors = 0
        sources = []
        links = []
        alreadyVisited = set([])
        iFrameSources = []
        videoSources = []

    recurse_get_sources(driver, done, topSite, errors, iFrameSources, videoSources, alreadyVisited, t, topSite)

    print("Done with " + topSite)
    if time.time() - t < (500 * 60):
        to_pickle = {'iframe': iFrameSources, 'video': videoSources, 'error': errors}
        site_split = urlsplit(topSite)
        newfile = (
        os.path.join(os.path.dirname(__file__), ("logs/" + site_split.hostname.replace('.', '_')) + "_sources.p"))
        of = open(newfile, "wb")
        pickle.dump(to_pickle, of)














