#!/usr/bin/env python

import sys

from BeautifulSoup import BeautifulSoup
import requests

htmlclient = {
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
}
urilist = []
espnurl = "http://www.espncricinfo.com"

def prompt():
    '''
    Returns esponse from the user
    '''
    try:
        return int(raw_input("Select series: "))
    except ValueError:
        print "Seems you are good @English. Use the index number left side."
        scrapresults(prompt())

def scrapresults(choice):
    try:
        global htmlclient, urilist, espnurl
        url = espnurl + urilist[choice-1].replace("content/current/", "engine/")
        response = requests.get(url, headers=htmlclient)

        # Scraping Results page for the selected series
        if response.status_code==200:
            soup = BeautifulSoup(response.text)
            print soup.title.text + "\n"
            for matchestable in soup.findAll("div", attrs={"class":"div630Pad"}):
                scores = [ score.text for score in matchestable.findAll("p", attrs={"class":"potMatchText mat_scores"}) ]
                status = [ status.text for status in matchestable.findAll("p", attrs={"class":"potMatchText mat_status"}) ]
                for matches in matchestable.findAll("p", attrs={"class":"potMatchHeading"}):
                    print matches.text
                    print scores.pop(0)
                    print status.pop(0) + "\n"
        else:
            print "Network Error. Try again later."
    except IndexError:
        print "Use the index number left side. Try again."
        scrapresults(prompt())

def main():
    global htmlclient, urilist, espnurl
    url = espnurl + "/ci/engine/match/scores/live.html"
    response = requests.get(url, headers=htmlclient)
    
    # Scraping Live matches page and getting the info for current international series as a list
    if response.status_code==200:
        soup = BeautifulSoup(response.text)
        for mainNav in soup.findAll("div", attrs={"id":"mainNav"}):
            for table in mainNav.findAll("table", attrs={"width":"270", "border":"0", "cellspacing":"0", "cellpadding":"0"}):
                urilist = [ uri.get("href") for uri in table.findAll("a") ]
    else:
        print "Network Error. Try again later."

    # Removing unnecessary 'ci' entry from list
    del urilist[-1]
    
    # View the series to user for selection
    for num, url in enumerate(urilist):
        print num+1, url.split("/")[1]

    scrapresults(prompt())

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)