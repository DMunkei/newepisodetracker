from email.message import EmailMessage
import smtplib
import config #This file is used to import the user credentials.
class Email:
    contentString=""
    properAnimeNames = dict()
    reportMessage = EmailMessage()
    #Sets the body of the email, can also be used to read out of a file.
    #TODO: Make it so that it gets its content from the JSON file after doing the comparison.
    reportMessage.set_content("Here is a update for the latest episodes:\n ")

    reportMessage['Subject'] = "Anime Episode Update"
    reportMessage['From'] = config.EMAIL_ADDRESS
    # reportMessage['To']= mailingList
    reportMessage['BCC'] = config.mailingList

    def __init__(self):
        self.properAnimeNames["onePiece"] = "One Piece"
        self.properAnimeNames["boruto"] = "Boruto - Naruto Next Generations"
        self.properAnimeNames["cellsAtWork"] = "Cells at Work"
        self.properAnimeNames["howNotToSummon"] = "How NOT to Summon a Demon Lord"
        self.properAnimeNames["overlord"] = "Overlord 3rd Season"
        self.properAnimeNames["baki"]= "Baki"
        self.properAnimeNames["boku"] = "My Hero Academia 3"
        self.properAnimeNames["foodWars"] = "Food Wars!: Shokugeki no Soma"
        self.properAnimeNames["blackClover"] = "Black Clover"
    
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

    def SetEmailContent(self,content):
        self.contentString = "The new hot anime updates. :D\n\n"
        for showName,showInfo in content.items():
            if showInfo['Status'] == "Completed":
                self.contentString += "{0} is over for this season.\n\n".format(self.properAnimeNames[showName])    
            else:
                self.contentString +="{0} episode {1} is out. GO WATCH IT!!\n\n".format(self.properAnimeNames[showName],showInfo['Episode'])
        self.reportMessage.set_content(self.contentString)