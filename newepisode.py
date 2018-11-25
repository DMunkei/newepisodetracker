import json
from pathlib import Path
from Scrapper import Scrapper
from MyEncoder import MyEncoder
from EpisodeData import EpisodeData
from Email import Email
from pprint import pprint

sendEmail = False
jsonFileExists = False
jsonFileName = "EpisodeData.json"
jsonFilePath = Path(jsonFileName)
oldEpisodes = ""
emailEpisodeData = {}
showEpisodeAndStatus = {}


if jsonFilePath.is_file():
    jsonFileExists = True
    with open(jsonFileName) as oldInformation:
        oldEpisodes = json.load(oldInformation)

episodes = EpisodeData()
testEncoder = MyEncoder()
#Create the scrapping object
target = Scrapper()
#start scrapping all the episodes information
#print("Latest One Piece Episode")
episodes.onePiece['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=One%20Piece")
episodes.onePiece['Last Upload'] = target.GetLastUpdatedSince()
episodes.onePiece['Status'] = target.GetAnimeStatus()


#print("Latest Boruto Episode")
episodes.boruto['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Boruto%20-%20Naruto%20Next%20Generations")
episodes.boruto['Last Upload'] = target.GetLastUpdatedSince()
episodes.boruto['Status'] = target.GetAnimeStatus()
#print("Latest Food War Episode")
episodes.foodWars['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Food%20Wars%20-%20The%20Third%20Plate%202018")
episodes.foodWars['Last Upload'] = target.GetLastUpdatedSince()
episodes.foodWars['Status'] = target.GetAnimeStatus()
#print("Latest Boku Episode")
episodes.boku['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=My%20Hero%20Academia%203")
episodes.boku['Last Upload'] = target.GetLastUpdatedSince()
episodes.boku['Status'] = target.GetAnimeStatus()
#print("Latest Cells At Work Episode")
episodes.cellsAtWork['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Cells%20at%20Work")
episodes.cellsAtWork['Last Upload'] = target.GetLastUpdatedSince()
episodes.cellsAtWork['Status'] = target.GetAnimeStatus()
#print("Latest How NOT to summon a Demon Lord Episode")
episodes.howNotToSummon['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=How%20NOT%20to%20Summon%20a%20Demon%20Lord%20Uncensored")
episodes.howNotToSummon['Last Upload'] = target.GetLastUpdatedSince()
episodes.howNotToSummon['Status'] = target.GetAnimeStatus()

episodes.overlord['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Overlord%203rd%20Season")
episodes.overlord['Last Upload'] = target.GetLastUpdatedSince()
episodes.overlord['Status'] = target.GetAnimeStatus()


episodes.baki['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Baki")
episodes.baki['Last Upload'] = target.GetLastUpdatedSince()
episodes.baki['Status'] = target.GetAnimeStatus()

episodes.blackClover['Episode'] = target.CheckCurrentEpisode("http://animeheaven.eu/i.php?a=Black%20Clover")
episodes.blackClover['Last Upload'] = target.GetLastUpdatedSince()
episodes.blackClover['Status'] = target.GetAnimeStatus()


#print(episodes)

#Serialize the information
currentEpisodes = testEncoder.encode(episodes)

#if a file already exists, we start checking the differences here. If there are any, then we send an email with the differences. Otherwise, we just do nothing
if(jsonFileExists == True):
    # The enumerate function makes it so we can add a counter to the forloop
    for episodeLooper, episode in enumerate(oldEpisodes.values()):
        k = list(currentEpisodes.items())
        showName = k[episodeLooper][0]
        currentEpisodeInfo = list(k[episodeLooper][1].items())
        freshEpisode = currentEpisodeInfo[0][1]
        episodeStatus = currentEpisodeInfo[2][1]
        if (freshEpisode == episode['Episode'] and episodeStatus == episode['Status']):
            pass
        else:
            #add the information that will be sent later to the people
            showEpisodeAndStatus["Episode"] = freshEpisode
            showEpisodeAndStatus["Status"] = episodeStatus
            emailEpisodeData[showName] = showEpisodeAndStatus
            sendEmail = True
try:
    with open('EpisodeData.json', 'w') as file:
            json.dump(currentEpisodes, file, indent=2)
except IOError as e:
    print(e)
    #If the file does exist, FIRST check with the data stored inside. Any differences need to be noted and then stored in another object/list
    #which will be used to send the E-Mail. After that overwrite the old data with the Up-to-date data.

#Now send an E-Mail.
if sendEmail:
    myEmail = Email()
    myEmail.SetEmailContent(emailEpisodeData)
    myEmail.SendMail()
