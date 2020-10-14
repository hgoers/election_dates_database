# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 18:22:11 2020

@author: hgoer
"""

def getElectionURLs():
    """ Gets the unique URLs for each election identified by IFES.
    
    """
    
    # import libraries
    import requests
    from bs4 import BeautifulSoup
    
    # request URL of URLs
    page = requests.get("https://www.electionguide.org/sitemap-election.xml")
    
    # fetch webpage
    soup = BeautifulSoup(page.content, "xml")
    
    # get data
    content = soup.find_all("loc")
    
    # create repository for URLs
    urls = []
    
    # get URLs
    for url in content:
        urls.append(url.get_text())
        
    return urls
    
from datetime import datetime

urls = getElectionURLs()

with open("elections_list_LDI_" + str(datetime.now().date()) + ".txt", "w") as filehandle:
    for listitem in urls:
        filehandle.write("%s\n" % listitem)