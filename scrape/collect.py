#   Fetches data from http://mfd.gov.np/weather
#   Author : ayys
#   Date : Mon, sept. 26, 2016
#

import urllib
from bs4 import BeautifulSoup


class Fetch:
    def __init__(self, url="http://mfd.gov.np/weather"):
        self.url = url
        self.htmlCode = ""

    def generateHtml(self):
        '''
            fetches the source code of the webpage on addr self.url
            and returns the output, and saves a copy in self.htmlCode
        '''
        self.htmlCode = "".join(urllib.urlopen(self.url).readlines())
        return self.htmlCode

    def getData(self):
        '''
            returns a beautifulsoup object of the html
        '''
        bs4Data = BeautifulSoup(self.htmlCode, "lxml")
        return bs4Data

    def getBSObject(self):
        '''
        returns a beautiful soup object for parsing
        '''
        self.generateHtml()
        return self.getData()
 
    def getParsedData(self):
        '''
        parses the data form the beautiful soup object and
        returns a list of scraped data
        '''
        bsObj = self.getBSObject()
        # note : the webpage only has one table
        trs = bsObj.find("table").findAll("tr") # get tr form table
        trs = trs[1:len(trs)-1]
        out = []
        for tr in trs:
            subOut = []
            for _ in tr.findAll("td"):
                subOut.append(_.getText())
            out.append(subOut)
        return out
