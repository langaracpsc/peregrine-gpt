import sys
import requests
from typing import Any
from html.parser import HTMLParser

def FetchPage(url: str) -> str:
    response: requests.Response = None
    
    try:
        response = requests.get(url)
    except BaseException as e:
        print(f"Failed to fetch the page. {e.args[0]}")

    return response.text

class DataParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.Data: list = []
        self.Links: list = []
    def handle_data(self, data: str) -> None:
        self.Data.append(data)
        return

class DataScraper:
    def __init__(self, url: str = None):
        self.URL: str = url
        self.Parser: DataParser = DataParser()
        self.Data: list[str] = []

    def Scrape(self, url: str = None) -> list[str]:
        if (url == None and self.URL == None):
            raise BaseException("No url provided to scrape")
        
        page: str = FetchPage(url)
        
        if (page == None):
            print(f"No page provided to scrape")
            return None

        self.Parser.feed(page)

        for data in self.Parser.Data:
            self.Data.append(data)

        return self.Data

    def GetDataStr(self):
        return str().join(data for data in self.Data)

    def Save(self, outputFile: str) -> bool:
        try:
            with open(outputFile, 'w') as fp:
                fp.write(self.GetDataStr())
        except:
            return False
 
        return True

 
