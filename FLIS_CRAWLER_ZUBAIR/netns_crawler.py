#Author: M. Zubair Rafique

#Permission  to  freely  reproduce  all  or  part  of  this  code  for  noncommercial
#purposes is granted provided that copies bear this notice and the full citation
#of our NDSS 2016 paper.  
#https://zubairrafique.wordpress.com/2015/10/28/ndss-2016-its-free-for-a-reason-exploring-the-ecosystem-of-free-live-streaming-services/

# Reproduction for commercial purposes is strictly prohibited without the prior written consent from 
# the KU Leuven, the Internet Society, and the first author: M Zubair Rafique

#Comments and Suggestions: <zubair.rafique@cs.kuleuven.be> <rafique.zubair@gmail.com>
# ======================================================================================

from optparse import OptionParser
from subprocess import Popen
from urlparse import urlparse
import os
from time import sleep

def launch_crawlers(url,domain,dir):
    
    """ Launch browser in seperate namespaces """
    
    botid              = 16
    count              = 0
    wait_time          = 60
    browser_folders    = ['chrome','firefox','mac','ie','mobile']
    browser_useragents = ["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",\
    "Mozilla/5.0 (Windows NT 6.1;  rv:46.0) Gecko/20100101 Firefox/46.0",\
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",\
    "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",\
    "Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>"]

    for folder in browser_folders:
        
        trace_cmd = "sudo ip netns exec bot"+str(botid+count)+" tcpdump -i veth-a"+str(botid+count)+" -s 0 -w "+dir+"/"+domain+"/"+folder+"/trace.pcap"
        py =Popen(trace_cmd, shell=True)
        
        cmd = "sudo ip netns exec bot"+str(botid+count)+" python crawler.py -u \'"+url+"\' -d "+dir+"/"+domain+"/"+folder+"/ -a \'"+browser_useragents[count]+"\'"
        pr = Popen(cmd, shell=True)
        
        count+=1
        
    sleep(wait_time)    #wait 1 minute
    
    #kill tcpdump, and browsers (if alive)
    os.system("sudo killall chrome -s 9")
    os.system("sudo killall chromium-browser -s 9")	
    os.system("sudo killall chromedriver -s 9")
    os.system("sudo killall tcpdump -s 9")
    
def scrapper(dir,file):
    
    urls = open(file)
    
    for url in urls:
        url    = url.strip("\n")    
        domain = '{uri.netloc}'.format(uri=urlparse(url))
        print domain
        
        #
        if not os.path.isdir(dir):
            os.system("mkdir "+dir)
            
        #making domain director
        if not os.path.isdir(dir+"/"+domain+"/"):
            os.system("mkdir "+dir+"/"+domain+"/") 
            
        #making UA specific direcories    
        if not os.path.isdir(dir+"/"+domain+"/chrome/"):
            os.system("mkdir "+dir+"/"+domain+"/chrome/");
           
        if not os.path.isdir(dir+"/"+domain+"/mac/"):
                os.system("mkdir "+dir+"/"+domain+"/mac/");
                
        if not os.path.isdir(dir+"/"+domain+"/mobile/"):
            os.system("mkdir "+dir+"/"+domain+"/mobile/");
              
        if not os.path.isdir(dir+"/"+domain+"/firefox/"):
            os.system("mkdir "+dir+"/"+domain+"/firefox/");
               
        if not os.path.isdir(dir+"/"+domain+"/ie/"):
            os.system("mkdir "+dir+"/"+domain+"/ie/");
            
        #launching crawlers
        launch_crawlers(url,domain,dir)            


  
    urls.close()            


if __name__ == '__main__':
    
    usage = "usage: %prog -f FILE_URLS_PER_LINE -d Directory [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--urls_file", dest="url", action="store", type="string",
                  help="URLs to crawl", metavar="URL_FILE")
    parser.add_option("-d", "--dir", dest="dir", action="store", type="string",
                  help="Directory to store data", metavar="DIR")
                
    (options, args) = parser.parse_args()

    print options.url, options.dir            
    scrapper(options.dir, options.url)