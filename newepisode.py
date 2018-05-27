import os
import json
import smtplib
import config #This file is used to import the user credentials.
import urllib.request
import hashlib
from bs4 import BeautifulSoup
class Email:
    sentFrom = config.EMAIL_ADDRESS
    to = ["stareye863@gmail.com"]
    subject = 'Anime Episode Update'
    body = "Hey what's up?\n"
    # msg="""
    # From: {0}
    # To: {1}
    # Subject{2}
    # {3}
    # """.format(sentFrom,to,subject,body)
    msg ="Hello, test test 123"
    server = None
    def __init__(self):
        pass
    
    def SendMail(self,subject,message):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_ADDRESS,config.PASSWORD)
            self.server.sendmail(config.EMAIL_ADDRESS,self.to,self.msg)
            self.server.quit()
            print("Success!")
        except:
            print("something went wrong")                               
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


myEmail = Email()
myEmail.SendMail(myEmail.subject,myEmail.msg)

target = Scrapper()
print("Latest One Piece Episode")
onepiece = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=One%20Piece")
OPlastUpload = target.GetLastUpdatedSince()
print("Latest Boruto Episode")
boruto = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Boruto%20-%20Naruto%20Next%20Generations")
borutoLastUpload = target.GetLastUpdatedSince()
print("Latest Food War Episode")
foodWars = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Food%20Wars%20-%20The%20Third%20Plate%202018")
foodWarsLastUpload = target.GetLastUpdatedSince()

target.episodeData = {
    "Anime" :
    [
        {
            "One Piece":onepiece,
            "Last uploaded":OPlastUpload
        },
        {
            "Boruto":boruto,
            "Last uploaded":borutoLastUpload
        },
        {
            "Food War":foodWars,
            "Last uploaded":foodWarsLastUpload
        }
    ]
}
jsonData = json.dumps(target.episodeData)
print(jsonData)
print("Checking Json File")

#TODO: Check if the file exists, if it does exist then just write inside it. Otherwise create it and write inside it.
with open('EpisodeData.json', 'w') as file:
        json.dump(target.episodeData,file)
#If the file does exist, FIRST check with the data stored inside. Any differences need to be noted and then stored in another object/list
#which will be used to send the E-Mail. After that overwrite the old data with the Up-to-date data.

#Now send an E-Mail.