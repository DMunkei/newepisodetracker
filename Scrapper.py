from bs4 import BeautifulSoup
import urllib.request

class Scrapper:
        soup = None
        url = ""
        httpResponse = None
        websiteContent = ""
        episodeData = {}

        def __init__(self):
                pass
        
        #This sends a get request to the website and opens it
        def GetWebsite(self, targetURL):
                self.url = targetURL
                self.httpResponse = urllib.request.Request(self.url,data=None,headers={"User Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"})
                self.websiteContent=urllib.request.urlopen(self.httpResponse)           
        #Creates the HTML Document Tree, so we can parse it
        def CreateSoup(self):
                self.soup = BeautifulSoup(self.websiteContent.read(), "html.parser")
        #Formats the DOM
        def PrettifyDOMTree(self):
                print(self.soup.prettify())
        #Don't know where I can use that yet...
        def FindAttribute(self, tags):
                targetAttribute=""
                for tag in tags:
                        targetAttribute += tag + " "
                targetAttribute = targetAttribute.rstrip()
                print("Searching for Tag...")
                for tag in self.soup.select(targetAttribute):
                        print(tag)
        #Finds the latest anime episode.From the Soup object 
        def GetLatestAnimeEpisode(self):
            episode= self.soup.find_all("div", class_="infoepboxmain",limit=1)
            episode =episode[0].text.split("\n")
            return episode[2]        
        def GetLastUpdatedSince(self):
            lastUpdate = self.soup.find_all("div", class_="infoepboxmain",limit=1)
            lastUpdate =lastUpdate[0].text.split("\n")
            return lastUpdate[3]
        #Invokes up all the method calls.
        def CheckCurrentEpisode(self,animeURL):
                self.GetWebsite(animeURL)
                self.CreateSoup()
                return self.GetLatestAnimeEpisode()