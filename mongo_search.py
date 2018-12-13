import sys

import pymongo

#def connect():

    

def lookup(tag):
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = myclient["mini3_mongo"]
    users = db.list_collection_names()
    
    x = 0

    session_info = {} 
    for u in users:
        results = []
        user = u[0]
        if user != 'users':
            user_profile= db["%s"%user]
            user_profile = user_profile.find()
           
            for tags in user_session:
                if tags != () and tags[2] == tag:
                    for i in results:
                        if tags[0] == i:
                            x = x+1
                    if x == 0:
                        results.append(tags[0])
                    x = 0
            session_info[user] = results

    return session_info


def hot_tag():
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = myclient["mini3_mongo"]
    users = db.list_collection_names()
    tag_info = {}
    
    for t in tables:
        if t[0]!='users':
            table = db["%s"%table]
            tags = table.find()
   
            x = 0
            for a in tags:               
                keys = tag_info.keys()
                for k in keys:
                    if(k == a[0]):
                        tag_info[k] = tag_info[k]+1
                        x = 1
                if x == 0:
                    tag_info[a[0]] = 0
                x = 0
    values = tag_info.values()
    value = []
    for x in values:
        value.append(x)
    maxm = max(value)
    hottest = value.index(maxm)
    keys = tag_info.keys()
    x = 0
    for k in keys:
        if x == hottest:
            return k
        x = x+1


if __name__ == '__main__':
    print("The hottest tag in database is %s."%hot_tag())
    x = 0
    sess = input('enter what you are looking for:')
    for m in lookup(sess):
        if lookup(sess)[m]!=[]:
            for n in lookup(sess)[m]:
                print("user's name: %s, search keywords:%s"%(m,n))
            x = 1
    if x == 0:
        print("this tag does not exist.")