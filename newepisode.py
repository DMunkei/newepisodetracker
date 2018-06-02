import os
import json
import smtplib
from email.message import EmailMessage
import config #This file is used to import the user credentials.
import urllib.request
import hashlib
from bs4 import BeautifulSoup

class EpisodeData():        
    onePiece = {}
    boruto = {}
    foodWars = {}
    boku = {}
    def __init__(self):
        self.onePiece = {}
        self.boruto = {}
        self.foodWars = {}
        self.boku = {}
class MyEncoder(json.JSONEncoder):            
    def encode(self,obj):
        return obj.__dict__

class Email:
    reportMessage = EmailMessage()
    #Sets the body of the email, can also be used to read out of a file.
    #TODO: Make it so that it gets its content from the JSON file after doing the comparison.
    reportMessage.set_content("Here is a update for the latest episodes:\n WIP!!")

    reportMessage['Subject'] = "Anime Episode Update"
    reportMessage['From'] = config.EMAIL_ADDRESS
    reportMessage['To']= ["stareye863@gmail.com",config.EMAIL_ADDRESS,"qasimwarraich@gmail.com"]

    def __init__(self):
        pass
    
    def SendMail(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_ADDRESS,config.PASSWORD)
            server.send_message(self.reportMessage)
            server.quit()
            print("Success!")
        except:
            print("OH NO!! ABORT!!")                               
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
            episode= target.soup.find_all("div", class_="infoepboxmain",limit=1)
            episode =episode[0].text.split("\n")
            return episode[2]        
        def GetLastUpdatedSince(self):
            lastUpdate = target.soup.find_all("div", class_="infoepboxmain",limit=1)
            lastUpdate =lastUpdate[0].text.split("\n")
            return lastUpdate[3]
        #Invokes up all the method calls.
        def CheckCurrentEpisode(self,animeURL):
                self.GetWebsite(animeURL)
                self.CreateSoup()
                return self.GetLatestAnimeEpisode()
episodes = EpisodeData()
testEncoder = MyEncoder()
target = Scrapper()
print("Latest One Piece Episode")
episodes.onePiece['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=One%20Piece")
episodes.onePiece['Last Upload'] = target.GetLastUpdatedSince()
print("Latest Boruto Episode")
episodes.boruto['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Boruto%20-%20Naruto%20Next%20Generations")
episodes.boruto['Last Upload'] = target.GetLastUpdatedSince()
print("Latest Food War Episode")
episodes.foodWars['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Food%20Wars%20-%20The%20Third%20Plate%202018")
episodes.foodWars['Last Upload'] = target.GetLastUpdatedSince()
print("Latest Boku Episode")
episodes.boku['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=My%20Hero%20Academia%203")
episodes.boku['Last Upload'] = target.GetLastUpdatedSince()
print(episodes)
jsonData = testEncoder.encode(episodes)
print(jsonData)
print("Checking Json File")

#TODO: Check if the file exists, if it does exist then just write inside it. Otherwise create it and write inside it.
try:
    with open('EpisodeData.json', 'w') as file:
            json.dump(jsonData,file,indent=2)
except IOError as e:
    print(e)
#If the file does exist, FIRST check with the data stored inside. Any differences need to be noted and then stored in another object/list
#which will be used to send the E-Mail. After that overwrite the old data with the Up-to-date data.

#Now send an E-Mail.
# myEmail = Email()
# myEmail.SendMail()