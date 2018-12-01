import tweepy #https://github.com/tweepy/tweepy
import json
import urllib
import requests
import sys
import io
import os
from google.cloud import vision
from google.cloud.vision import types
import pymongo


'''
dynamicly add collection
'''
def addTable(tablename):
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["mini3_mongo"]
    set = mydb["users"]
    set.insert({"username":tablename})



    

#Twitter API credentials
consumer_key =xxxxxxxxxxxxxxxxxxxx
consumer_secret = xxxxxxxxxxxxxxxx
access_key =xxxxxxxxxxxxxxxxxxxxxx
access_secret =xxxxxxxxxxxxxxxxxxx

def get_tweets_pic(screen_name):
    i=0

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    users_tweets = api.user_timeline(screen_name = screen_name,count=20)
    while (i<10):
        for pic in users_tweets:
            if "media" in pic.entities.keys():    
                urllib.request.urlretrieve(pic.entities["media"][0]["media_url"],'/home/ece-student/Desktop/Twitter_Get/Photo/%d.jpg'%(i+1))
                i=i+1
                if i==10:
                    break 
    
            


def addTag():
# Instantiates a client
    client = vision.ImageAnnotatorClient()

    for x in range(1,11):
# The name of the image file to annotate
        file_name = '/home/ece-student/Desktop/Twitter_Get/Photo/%d.jpg'%x

# Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

# Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        f = open("/home/ece-student/Desktop/Twitter_Get/Photo/%drecog.txt"%x, "w")
    #print(('pic%d_Labels:'%x+'\n'),file = f )
        for label in labels:
            print((label.description),file = f )
        print(('\n'),file = f)
        f.close()

def get_tweets_url(screen_name):
    i=1

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    users_tweets = api.user_timeline(screen_name = screen_name,count=20)
    
    for pic in users_tweets:
        if "media" in pic.entities.keys():
            f = open("/home/ece-student/Desktop/Twitter_Get/Photo/%durl.txt"%i, "w")
            print(pic.entities["media"][0]["media_url"],file = f )
            f.close()
            #urllib.request.urlretrieve(pic.entities["media"][0]["media_url"],'/home/ece-student/Desktop/Twitter_Get/Photo/%d.jpg'%(i+1))
            i=i+1
            if i==11:
                break   

def InsertTable(str1,str2):
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["mini3_mongo"]

    set = mydb["%s"%str1]

    for tag_name in range(1,11):
        try:
        
            fin = open(('/home/ece-student/Desktop/Twitter_Get/Photo/%drecog.txt'%tag_name),'r')
            print('%drecog.txt'%tag_name)
            tag = fin.read()
            fin.close()

            fin2 = open(('/home/ece-student/Desktop/Twitter_Get/Photo/%durl.txt'%tag_name),'r')
            print('%durl.txt'%tag_name)
            url = fin2.read()
            fin2.close()


        except IOError as e:
            print ("Error %d: %s" % (e.args[0],e.args[1]))
            sys.exit(1)
        
        f = open("/home/ece-student/Desktop/Twitter_Get/Photo/%drecog.txt"%tag_name,"rt") 
        content = f.readlines()
        for m in content:
            if m !='\n':
                tweets_content = {"hoster":str1,"url":repr(url),"tag":m} 
                set.insert_one(tweets_content)
        f.close()




if __name__ == '__main__':
    str1 = input("Enter your user name as the table name, please: ");
    addTable (str1)
    str2 = input("Enter the people's name with a @ ,please: ");
    get_tweets_pic(str2)
    addTag()
    get_tweets_url(str2)
    InsertTable(str1,str2)