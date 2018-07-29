import json
import smtplib
import config #This file is used to import the user credentials.
class MyEncoder(json.JSONEncoder):            
    def encode(self,obj):
        return obj.__dict__  