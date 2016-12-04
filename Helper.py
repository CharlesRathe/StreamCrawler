import os, time, pickle
from urllib.parse import urlsplit


# Function to get all links in site tree
def recurse_get_sources(driver, done, site_to_crawl, errors, frame_array, video_array, visited, t, topSite):

    # Go to site
    try:
        driver.get(site_to_crawl)

    except TimeoutError:
        print("TIMEOUT")
        return
    except:
        print("Couldn't visit site: " + site_to_crawl)
        return


    visited.add(site_to_crawl)
    child_sources = []

    # Collect video and link info
    child_frames = driver.find_elements_by_xpath('//iframe[@src]')
    child_videos = driver.find_elements_by_xpath('//video[@src]')
    child_links = driver.find_elements_by_xpath('//a[@href]')
    error_links = driver.find_elements_by_xpath('//*[contains(text(), "error")]')

    for childLink in child_links:
        child_sources.append(childLink.get_attribute("href"))
        print("Adding: " + childLink.get_attribute("href") + " to children")

    # Run links through filters (subject to change)
    for child_index, child_source in enumerate(child_sources):
        if "mailto" in child_source or "login" in child_source or "imdb" in child_source or "twitter" in child_source or "facebook" in child_source \
                or "search" in child_source or "google" in child_source or "png" in child_source or "jpg" in child_source or "gif" in child_source \
                or "rottentomatoes" in child_source or child_source == site_to_crawl or child_source.endswith('#') \
                or "genre" in child_source:
            visited.add(child_source)
            del child_sources[child_index]

        elif child_source in visited:
            del child_sources[child_index]

    # Add new video sources to list
    for child_frame in child_frames:
        if "facebook" not in child_frame:
            frame_array.append(child_frame.get_attribute('src'))
            print("Adding frame: " + child_frame.get_attribute('src'))

    for child_video in child_videos:
        video_array.append(child_video.get_attribute('src'))
        print("Adding source: " + child_video.get_attribute('src'))

    for error_link in error_links:
        errors += 1
        print ("Adding error!!")

    # If still in the domain, continue collecting links, if not, return and continue traversing child pages
    if topSite not in site_to_crawl:
        return

    else:
        for childSrc in child_sources:

            if done == 1:
                return

            if time.time() - t >(500*60):
                to_pickle = {'iframe': frame_array, 'video': video_array}
                site_split = urlsplit(site_to_crawl)
                newfile = (os.path.join(os.path.dirname(__file__), ("logs/" + site_split.hostname.replace('.', '_')) + "_sources.p"))
                of = open(newfile, "wb")
                pickle.dump(to_pickle, of)
                done = 1
                return

            elif childSrc not in visited:
                recurse_get_sources(driver, done, childSrc, errors, frame_array, video_array, visited, t, topSite)
