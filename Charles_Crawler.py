from selenium import webdriver
import time, os
import pickle
from urllib.parse import urlsplit

done = 0


# Function to get all links in site tree
def recurse_get_sources(frame_array, video_array, visited, child_page):

    global done
    print("going to: " + child_page)
    # Go to site
    try:
        driver.get(child_page)
        visited.add(child_page)
    except:
        print("Cannot visit " + child_page)

    child_sources = []

    # Collect video and link info
    child_frames = driver.find_elements_by_xpath('//iframe[@src]')
    child_videos = driver.find_elements_by_xpath('//video[@src]')
    child_links = driver.find_elements_by_xpath('//a[@href]')

    for childLink in child_links:
        child_sources.append(childLink.get_attribute("href"))

    # Run links through filters (subject to change)
    for child_index, child_source in enumerate(child_sources):
        if "mailto" in child_source or "login" in child_source or "imdb" in child_source or "twitter" in child_source or "facebook" in child_source \
                or "google" in child_source or "png" in child_source or "jpg" in child_source or "gif" in child_source or "rottentomatoes" in child_source or child_source == topSite or child_source.endswith('#'):
            visited.add(child_source)
            del child_sources[child_index]

        elif child_source in alreadyVisited:
            del child_sources[child_index]

    # Add new video sources to list
    for child_frame in child_frames:
        frame_array.append(child_frame.get_attribute('src'))

    for child_video in child_videos:
        video_array.append(child_video.get_attribute('src'))

    # If still in the domain, continue collecting links, if not, return and continue traversing child pages
    if topSite not in child_page:
        return

    else:
        for childSrc in child_sources:

            if done == 1:
                return

            if time.time() - t >(30*60):
                to_pickle = {'iframe': iFrameSources, 'video': videoSources}
                site_split = urlsplit(topSite)
                newfile = (os.path.join(os.path.dirname(__file__), ("logs/" + site_split.hostname.replace('.', '_')) + "_sources.p"))
                of = open(newfile, "wb")
                pickle.dump(to_pickle, of)
                done = 1
                return

            elif childSrc not in alreadyVisited:
                recurse_get_sources(frame_array, video_array, visited, childSrc)

# Get list of top level URL's (hand compiled?) to be searched
with open("topURLs.txt") as f:
    topSites = f.readlines()

t = time.time()

# Set up WebDriver with Chromium Driver path
driver = webdriver.Chrome("C:\Python35-32\selenium\chromedriver.exe")

# Go through all top level domains
for topSite in topSites:

    done = 0

    # Init Lists
    sources = []
    links = []
    alreadyVisited = set([])
    iFrameSources = []
    videoSources = []

    # Go to top site
    driver.get(topSite)
    alreadyVisited.add(topSite)

    # Get top site's videos and child links
    iFrames = driver.find_elements_by_xpath('//iframe[@src]')
    videos = driver.find_elements_by_xpath('//video[@src]')
    links = driver.find_elements_by_xpath('//a[@href]')

    for link in links:
        sources.append(link.get_attribute("href"))

    # Run links through filters (subject to change)
    for index, link in enumerate(sources):
        if "mailto" in link or "login" in link or "imdb" in link or "twitter" in link or "facebook" in link \
                or "google" in link or link == topSite or link.endswith('#'):
            alreadyVisited.add(link)
            del sources[index]

        elif link in alreadyVisited:
            del sources[index]

    # Append src attributes to inclusive source list
    for iFrame in iFrames:
        iFrameSources.append(iFrame.get_attribute('src'))

    for video in videos:
        videoSources.append(video.get_attribute('src'))

    for child in sources:
        done = 0
        if child not in alreadyVisited:
            recurse_get_sources(iFrameSources, videoSources, alreadyVisited, child)
















