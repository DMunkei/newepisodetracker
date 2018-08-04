from email.message import EmailMessage
import smtplib
import config #This file is used to import the user credentials.
class Email:
    contentString=""
    mailingList =["stareye863@gmail.com",
    config.EMAIL_ADDRESS,
    "qasimwarraich@gmail.com",
    "saif.roshdy.h@gmail.com",
    "dawn_wanderer@hotmail.com",
    "joehedington@gmail.com",
    "burhan.erdogrul@live.nl"]
    reportMessage = EmailMessage()
    #Sets the body of the email, can also be used to read out of a file.
    #TODO: Make it so that it gets its content from the JSON file after doing the comparison.
    reportMessage.set_content("Here is a update for the latest episodes:\n WIP!!")

    reportMessage['Subject'] = "Anime Episode Update"
    reportMessage['From'] = config.EMAIL_ADDRESS
    reportMessage['To']= mailingList

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

    def SetEmailContent(self,content):
        self.contentString = "The new hot anime updates. :D\n\n"
        for showName,episode in content.items():    
            self.contentString +="{0} episode {1} is out!!GO WATCH IT!!\n\n".format(showName,episode)
        self.reportMessage.set_content(self.contentString)