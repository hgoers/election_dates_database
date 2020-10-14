# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 18:45:30 2020

@author: hgoer
"""

def getElectionData():
    # import libraries
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from datetime import datetime
    
    # get URLs
    urls = []
    
    with open("elections_list_LDI_" + str(datetime.now().date()) + ".txt", "r") as filehandle:
        for line in filehandle:
            url = line[:-1]
            urls.append(url)
            
    # specify empty lists for variables
    country_list = []
    election_list = []
    date_list = []
    status_list = []
    
    # iterate over each election
    for url in urls:
        # fetch URLs one by one
        page = requests.get(url)
        
        # process data
        soup = BeautifulSoup(page.content, "html.parser")
        
        # get country
        country = soup.find("div", {"class": "titles"}).h3
        country_list.append(country.get_text().strip())
        
        # get election
        election = soup.find("div", {"class": "titles"}).h5
        election_list.append(election.get_text().strip())
        
        # get date
        date = soup.find("section", {"class": "box election-country"}).h3.span
        date_list.append(date.get_text().strip())
        
        # get status
        status = soup.find("section", {"class": "box election-country"}).h3.em
        status_list.append(status.get_text().strip())
    
    # create database
    df = pd.DataFrame.from_dict({'country': country_list,
                                 'election': election_list,
                                 'date': date_list,
                                 'status': status_list})
    
    # clean up dates
    df['date'] = pd.to_datetime(df['date'], errors='ignore')
    
    return
    df

# import libraries
from datetime import datetime
import pandas as pd

election_df = getElectionData()

# save to csv with LDI
election_df.to_csv("election_dates_LDI_" + str(datetime.now().date()) + ".csv", index=False)
