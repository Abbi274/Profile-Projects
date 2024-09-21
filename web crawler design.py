import os
import time 
import sys 
import whois # domain registration details - use to week out suspect sites 
            # by seeing how long the site has been active 
import datetime # used with whois
import redis # database storage 
import scrapy # base crawler fns - already handles TLS connection and ssl check for certs internally 
from scrapy.linkextractors import LinkExtractor #LinkExtractor class
# read metadata and extract links for us to add to queue 
from pathlib import Path #build paths/dir
from urllib.parse import urlparse #parse our urls into relevant pieces

class Quotes(scrapy.Spider): #inherits base crawler fns
    name = 'quotes' #our crawler's name - how scrapy will find it 
    def __init__(self):
        self.r = redis.Redis(host='localhost', port= 6379, db=0) #database
        self.hostname = '' 
        self.path = 'data' #dir name 
        self.le = LinkExtractor() #our extractor class 
        # ethical settings and transparency - obey robot txts and identify self 
        self.custom_settings = {
            'ROBOTSTXT_OBEY': True, 
            'user_agent': 'MyWebCrawler/1.0 (www.myportfoliowebsite.com)'
        }
    def start_requests(self): 
        self.r.rpush('task_queue', 'https://currentsite.com') #push the url into queue
        
        while True:
            item = self.r.lpop('task_queue') #pop first url

            if item is None: # try once more if none and break if empty but 
                             # still reading true (safety net to stop)
                time.sleep(1)
                item = self.r.lpop('task_queue')
                if item is None:
                    break

            url = item.decode("utf-8") # convert the binary rep of url to a str
            if self.hostname == '': #name hostname so we can find links to it
                self.hostname = urlparse(url).hostname
            yield scrapy.Request(url=url, callback=self.parse) #parse metadata


    def parse(self, response):
        content_type = response.headers.get('Content-Type', None).decode('utf-8')

        if 'text/html' not in content_type: #if not type text we want, ignore
            return
      
        domain_name = urlparse(response.url).netloc #get the domain and port
        domain_info = whois.whois(domain_name) #grabs domain's whois data
        creation_date = domain_info.creation_date #takes the date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]  # Take earliest date if > 1
        if isinstance(creation_date, str): #convert to format 
            creation_date = datetime.datetime.strptime(creation_date, '%m/%d/%Y')    
        
        if (datetime.datetime.now() - creation_date).days < 180:  
            print(f"{domain_name} is less than 300 days old; skipping.")
            return  #safety from newer sites that could be phishy
       
        filepath = urlparse(response.url).path #take the path
        if filepath[-1] == '/':
            filepath += 'index.html'  #if ends at dir add path ending(if a dir it will end with a slash) 
            # add the html ending and send it in so we can see if this path leads to more html docs  
            
        path = self.path + filepath #add to our dir and add parents or overwrite as needed
        Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f: # open the file with wb so we can write in binary to it
            f.write(response.body) # now write the body of the url in bin to the file 

        self.r.sadd('task_finished', response.url)#create set and add visited
        for link in self.le.extract_links(response): #get links
            url = link.url
            if urlparse(url).hostname != self.hostname:
                break
            # if same hostname we want to crawl (as long not in visited set)
            if self.r.sismember('task_finished', url):
                break

            self.r.rpush('task_queue', url) # queue it up 


# use scrapy crawl quotes within your terminal when ready. the base crawler in Spider will 
# automatically check the custom settings and adapt

