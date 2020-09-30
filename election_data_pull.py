# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:57:55 2020

@author: hgoer
"""

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict

# Request URL
page = requests.get("https://www.electionguide.org/sitemap-election.xml")

# Fetch webpage
soup = BeautifulSoup(page.content, "html.parser")

# Get URLs
content = soup.find_all("loc")

urls = []

for i in range(len(content)):
    temp = str(content[i]).strip('<loc>')[:-2]
    urls.append(temp)

# Create list to store information
election_info = []

# Iterate over each election
for url in urls:
    d = OrderedDict()

    # Fetch URLs one by one
    request = requests.get(url)

    # Data processing
    content = request.content
    soup = BeautifulSoup(content,"html.parser")

    # Scraping Data
    info = soup.find_all('section')[11]

    d['date'] = info.find('span').get_text().strip()    
    d['status'] = info.find('em').get_text().strip()
    d['country'] = info.find('a').get_text().strip()
    d['election'] = info.find('h5').get_text().strip()

    # Append dictionary to list 
    election_info.append(d)

# Create DataFrame
df = pd.DataFrame(election_info)    

# Clean up dates
df['date'] = pd.to_datetime(df['date'], errors='ignore')

# Save to csv
df.to_csv('Election_dates.csv', index=False)
