#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import requests

url = "http://www.espncricinfo.com/ci/engine/match/scores/live.html"
response = requests.get(url)

# Scraping Live matches page and getting the info for current series as a list
if response.status_code==200:
    soup = BeautifulSoup(response.text)
    for mainNav in soup.findAll("div" , attrs={"id" : "mainNav"}):
        for table in mainNav.findAll("table", attrs={"width":"270", "border":"0", "cellspacing":"0", "cellpadding":"0"}):
            urilist = [ uri.get("href") for uri in table.findAll("a") ]

# View the series to user for selection
for num, url in enumerate(urilist):
    print num+1, url.split("/")[1]
    