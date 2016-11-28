
Author : M. Zubair Rafique
Contact: <zubair.rafique@cs.kuleuven.be> <rafique.zubair@gmail.com>

Tested on Ubuntu 16.04 (should work on 14+)
===========================================================================================================

1. Download webdriver, from https://chromedriver.storage.googleapis.com/index.html?path=2.25/
   (look for system architecture 32 or 64 bit, download and unzip in same directory)

2. prerequisites: 
        sudo apt-get install chromium-browser
        sudo apt-get install python
	sudo apt-get install lynx
	sudo apt-get install python-pip
	sudo pip install selenium



=================================Simple Usage===============================================================
Usage: python crawler.py -u URL -d Directory [options]

Options:
  -h, --help             show this help message and exit
  -u URL, --url=URL      URL to crawl
  -d DIR, --dir=DIR      Directory to store data
  -a UA, --useragent=UA  User Agent value
  -p CP, --driverpath=CP Chrome dirver path, default is current directory


Example:  python crawler.py -u http://ifirstrow.eu -d test/ (will dump the data in the test directory)

=============================================Advance Usage=====================================================
1. Features
	-Log network traffic
	-Five browsers in parallel with different user agents

2. prerequisites:
	sudo apt-get install tcpdump
        sudo pip install tldextract

3. run the code namespace.sh (make sure to which network interface you are using)
        sudo ./namespace.sh
        (for debugging, http://stackoverflow.com/questions/27720529/how-to-use-linux-network-namespaces-for-per-processes-routing/27751532)

4. Usage: netns_crawler.py -f FILE_URLS_PER_LINE -d Directory [options]

Options:
  -h, --help            show this help message and exit
  -f URL_FILE, --urls_file=URL_FILE  File containg URLs to crawl, one per line
  -d DIR, --dir=DIR     Directory to store data

Example: sudo python netns_crawler.py -f urls.txt -d test/


