import json
from imap_tools import MailBox, AND
import os
import dropbox
from io import BytesIO
from zipfile import ZipFile

def SaveFileToStorage(fileBytes, savePath):
    '''
    fileBytes = bytes content of the file to be saved
    savePath = dropbox save path including the file name to be saved under
    If file exists in location, it is overwritten, if directory does not exist, it is created 
    '''
    dbx = dropbox.Dropbox(configObj["dropboxToken"])
    dbx.files_upload(fileBytes, savePath, mute=True)
    return

#Load config
with open("config.json", "r") as reader:
    config = reader.read()
configObj = json.loads(config)

#open IMAP connection and process emails
fileTypes = configObj["targetTypes"] # get file types to be saved from config (now pdg, image)
with MailBox(configObj["imapServer"]).login(configObj["mailBox"],configObj["password"], initial_folder=configObj["initialFolder"]) as mails:
    toMove=[]
    for msg in mails.fetch(AND(seen=False)):  
        if len(msg.attachments) >0:   
            for att in msg.attachments:
                print(msg.subject + ", " + att.content_type + ", " + msg.uid)
                for fType in fileTypes:
                    if fType in att.filename.lower(): # check attachment against types
                        savePath = configObj["saveFilePath"] + "/" + att.filename
                        SaveFileToStorage(att.payload, savePath)
                    elif ".zip" in att.filename.lower(): #zip files processing to be added
                        with ZipFile(BytesIO(att.payload)) as myZip:
                            for containedFile in myZip.namelist():
                                savePath = configObj["saveFilePath"] + "/" + containedFile
                                SaveFileToStorage(myZip.open(containedFile).read(), savePath)     
            toMove.append(msg.uid) # adds msg.uid to list => processed by mails.move below
        else:
            print(msg.uid + " has no relevant attachments")
        mails.seen(msg.uid,False) #check as unseen (fetch flags as seeen, must be undone here)
    mails.move(toMove,configObj["processingFolder"]) #move emails to processing folder in bulk (could not make it work on one by one basis) POZOR: move email ZMĚNÍ uid, nelze dále použít!

