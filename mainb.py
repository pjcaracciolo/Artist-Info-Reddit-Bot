import praw
import config
import time


# Artist class to store info on artists
class Artist(object):
    name = ''
    insta = ''
    twitter = ''
    img = ''
    wiki = ''
    discog = ''
    sub = ''
    def __init__(self, name, img, insta, twitter, wiki, discog, sub):
        self.name = name
        self.insta = insta
        self.twitter = twitter
        self.img = img
        self.wiki = wiki
        self.discog = discog
        self.sub = sub

    def printInfo(self):
        print(self.name + " Photo: " + self.img + " Insta: " + self.insta + " Twitter: " + self.twitter + " Wiki " + self.wiki + " Discog " + self.discog + " Sub " + self.sub)


def login():
    inst = praw.Reddit(username = config.username,password = config.password,client_id = config.client_id,client_secret = config.client_secret, user_agent = "hhh operating bot")
    return inst

def exec(inst):
    for s in inst.subreddit('hiphopheads').new(limit = 50):
        title = s.title.lower()
        id = s.id
        titleArtists = []
        output = 'Hello, I am a bot. My purpose is to deliver information about artists.\n\n'
        if not alreadyRepliedThread(id,inst) and '-' in title:
            for k in artistList:
                if k.name.lower() in title:
                    print('Found ' + k.name + ' in ' + title)
                    titleArtists.append(k)
            amt = len(titleArtists)
            if amt > 0:
                output += 'Identified ' + str(amt) + ' artist(s) in title\n\n'
                for i in titleArtists:
                    output +='---------------------\n\nArtist Name & Photo: [' + i.name +']('+i.img+')\n\n' +i.name + '\'s [Instagram](' + i.insta + ')\n\n' +i.name + '\'s [Twitter](' + i.twitter+')\n\n' + i.name +'\'s [Wiki Page](' + i.wiki + ') and [Discography](' + i.discog +')\n\n'
                    if not i.sub == 'null':
                        output += i.name + '\'s Subreddit /r/'+i.sub + '\n\n'
                try:
                    output += '---------------------\n\nI am currently in testing. In the interest of not spamming, I will only post for a small amount of artists and only on certain posts, for the time being. If you have any recommendations for improvement, please send me a message.\n\n'
                    s.reply(output)
                    storeID(id)
                    print('Posted')
                except:
                    print('EXCEPTION OCCURRED, SLEEPING FOR 10 MINUTES')
                    time.sleep(600)


def alreadyRepliedThread(thread,inst):
    replies = open("replied","r").read().splitlines()
    for i in replies:
        if thread == i:
            return True
    return False

def storeID(id):
    fileS = open("replied","a")
    fileS.write(id+'\n')

artistList = []

def loadList():
    file1 = open('artistlist','r').read().splitlines()
    for i in file1:
        if len(i) > 40:
            elems = i.split("~")
            artist = Artist(elems[0],elems[1],elems[2],elems[3],elems[4],elems[5],elems[6])
            artistList.append(artist)

def haveArtist(name):
    for i in artistList:
        if(name == i.name):
            return True
    return False

inst = login()
loadList()

while True:
    exec(inst)
    time.sleep(5)
