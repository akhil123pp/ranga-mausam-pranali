#   Fetches data from http://mfd.gov.np/weather
#   Author : ayys
#   Date : Mon, sept. 26, 2016
#

import urllib
from bs4 import BeautifulSoup
import datetime


class Fetch:
    def __init__(self, url="http://mfd.gov.np/weather"):
        self.url = url
        self.htmlCode = ""
        self.BSObject = self.getBSObject()
        self.parsedData = self.getParsedData()

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
        # note : the webpage only has one table
        #
        # The data on the page is in two places, 
        # the (only) table on the webpage
        # and in the divs with class "weather-icon"
        #
        # Exctract data from the table
        trs = self.BSObject.find("table").findAll("tr")  # get tr form table
        trs = trs[1:len(trs)-1]
        out = []
        out_dict = dict()
        for tr in trs:
            subOut = []
            for _ in tr.findAll("td"):
                subOut.append(_.getText())
            out.append(subOut)
        self.parsedData = out
        for _ in out:
            out_dict[_[0].lower()] = {
                    "max_temp": _[1],
                    "min_temp": _[2],
                    "rainfall": _[3]}

        # extract data from the weather icon divs
        # sample dlw' :
        # <dl class="dl-horizontal">
        #       <dt>Sunrise</dt>
        #       <dd>05:55 </dd>
        #       <dt>Sunset</dt>
        #       <dd>17:55 </dd>
        #       <dt>Air Temperature</dt>
        #       <dd>19 C</dd>
        #       <dt>Relative Humidity</dt>
        #       <dd>95 %</dd>
        #   </dl>

        weatherIconDivs = self.BSObject.find_all(
                            "div",
                            attrs={
                                "class": "weather-icon"})
        for loc in weatherIconDivs:
            dataToParse = BeautifulSoup(loc.attrs['data-pop'], "lxml")
            dl = dataToParse.find("dl", attrs={"class": "dl-horizontal"})
            dtL = dl.find_all("dt")
            ddL = dl.find_all("dd")
            out_dict_sub = dict()
            print loc['time']

            # also deduce the season based on the month
            # this is done by the getSeason funciton
            for _ in dtL:
                out_dict_sub[_.getText()] = ddL[dtL.index(_)].getText()

            out_dict[loc["title"].lower()].update(out_dict_sub)

        return out_dict

    def getLocations(self):
        '''
        returns an array of locations frm the parsed data
        '''
        return [_.lower() for _ in self.parsedData.keys()]

    def getSeason(self):
        '''
        deduces the season based on a date, scraped from the page.
        The season deduction follows the following chart:

        Hindu season    Start           End
        Vasant          mid-March       mid-May
        Greeshm         mid-May         mid-July
        Varsha          mid-July        mid-September
        Sharad          mid-September   mid-November
        Hemant          mid-November    mid-January
        Shishir         mid-January     mid-March
        '''
        data = self.BSObject.find_all(
                            "div",
                            attrs={"class": "weather-icon"})
        date = data[0]['time']

        date = date.strip("Issued on ")
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M %Z")
        midMarch = datetime.datetime(date.year, 3, 15, 6, 0)
        midMay = datetime.datetime(date.year, 5, 15, 6, 0)
        midJuly = datetime.datetime(date.year, 7, 15, 6, 0)
        midSept = datetime.datetime(date.year, 9, 15, 6, 0)
        midNov = datetime.datetime(date.year, 11, 15, 6, 0)
        midJan = datetime.datetime(date.year, 1, 15, 6, 0)

        if date >= midMarch and date <= midMay:
            return "vasant"
        elif date >= midMay and date <= midJuly:
            return "greeshm"
        elif date >= midJuly and date <= midSept:
            return "varsha"
        elif date >= midSept and date <= midNov:
            return "sharad"
        elif date >= midNov and date <= midJan:
            return "hemant"
        else:
            return "shishir"
