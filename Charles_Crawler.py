from selenium import webdriver
import pickle

# Get list of top level URL's (hand compiled?) to be searched
with open("topURLs.txt") as f:
    topSites = f.readlines()

# Set up WebDriver with Chromium Driver path
driver = webdriver.Chrome("C:\Python35-32\selenium\chromedriver.exe")

# Go through all top level domains
for topSite in topSites:

    # Init Lists
    links = []
    alreadyVisited = []
    iFrameSources = []
    videoSources = []

    # GOTO top site
    driver.get(topSite)

    # Get top site's videos and child links
    iFrames = driver.find_elements_by_xpath('//iframe[@src]')
    videos = driver.find_elements_by_xpath('//video[@src]')
    links = driver.find_elements_by_xpath('//a[@href]')

    # Run links through filters (subject to change)
    for index, link in enumerate(links):
        if "mailto" in link.get_attribute('href') or "login" in link.get_attribute("href"):
            del links[index]

    for iFrame in iFrames:
        print(iFrame.get_attribute('src'))

    for video in videos:
        print(video.get_attribute('src'))

        #href -> with id contains '#' click()










