import sys
import requests
import json 
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

class Element:
    __slots__ = ("Tag", "Attributes", "Children")

    def __init__(self, tag: str, attributes: dict, children: list) -> None:
        self.Tag = tag
        self.Attributes = attributes
        self.Children = children

    def __str__(self) -> str:
        return json.dumps(dict({"tag": self.Tag, "attr": self.Attributes, "children": [str(child) for child in self.Children]}), indent=2)
        
class ElementSeeker(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.CurrentElement: int = 0

        self.ElementStack: list = []
        self.SeekedElements: list = []
        self.ArbData: list = []
    
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        element = Element(tag, attrs, [])

        if (len(self.ElementStack) > 0):
            self.ElementStack[self.CurrentElement - 1].Children.append(element)
            self.CurrentElement += 1
    
        self.ElementStack.append(element)

    def handle_endtag(self, tag: str) -> None:
        if (tag == self.SeekElement):
            element = self.ElementStack[self.CurrentElement]
            if (element.Tag != tag):
                for child in filter(lambda elem : elem.Tag == tag, filter(lambda child : type(child) == Element, element.Children)):
                    self.SeekedElements.append(child)

            else:
                self.SeekElements.append(element)
            

        if (self.CurrentElement):
            self.CurrentElement -= 1

    def handle_data(self, data: str) -> None:
        if (len(self.ElementStack) > 0):
            self.ElementStack[self.CurrentElement].Children.append(data)
        else:
            self.ArbData.append(data) 

    def Seek(self, html: str, element: str) -> list[Element]:
        self.SeekElement: str = element
        self.feed(html)

        return self.SeekedElements
    
    def Reset(self) -> None:
        self.ArbData.clear()
        self.ElementStack.clear()
        self.SeekedElements.clear()
        self.CurrentElement = 0
        self.SeekElement = None

        return super().reset()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

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

