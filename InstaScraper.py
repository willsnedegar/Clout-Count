import urllib.request
from twython import Twython
import json
import re
import math
import random
import time
from bs4 import BeautifulSoup
from statistics import mean
import requests
from selenium import webdriver

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from pymongo import MongoClient

client = MongoClient("mongodb+srv://willsned:Cardinals1@cluster0-lcapt.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.pymongo_test


#compiled insta likes, comments, followers, following, and instaPosts 0-10, 10-50 50-200 200+
#avg lkes + 2*avg comments + + followers/following 1/3 to 3 + postsMultiplier
#compiled twitter followers count, tweet count, tweet favorites and retweets
#favorites + 4 rewteets + followers/500 + tweet count
#youtube views count, comment count, subscriber count, video Count,
# total views + 1000 * subscribers + 500 * comment count
#facebook likes and talking about number

def main():
    driver = webdriver.Chrome('./chromedriver.exe')
    top = {'username':"", 'topScore':0}
    userDatabase = db.instaUsers
    allUsers = userDatabase.find({})
    try:
        for user in allUsers:
            instaScore = scrapeInstaAccount(driver, user)
            user['instaScore'] = instaScore
            result = userDatabase.update_one({'_id': user['_id']}, {'$set': {'instaScore':user['instaScore']}})
            print(instaScore)

            if instaScore >= top['topScore'] or user['username'] == top['username']:
                top['topScore'] = instaScore
                top['username'] = user['username']
                top['fullName'] = user['fullName']
        userDatabase.insert_one(top)

    except ConnectionError as e:
        print(e)
    print(top)

    #scrapeYoutubeAccount(driver,'dog')
    #scrapeFacebook('dog')

    # python_tweets = Twython("IuVdTEmT07uWCvq9xcFQq9BfX", "xMHDCrwWggo9L439Mggn7sTDT5y4lipcVHwZ0xLALJzGrroyrS")
    #
    # with open('twitterHandles.txt') as f:
    #     twitterHandles = f.read().splitlines()
    # print(twitterHandles)
    # for handle in twitterHandles:
    #     scrapeTwitterAccount(handle)



def scrapeInstaAccount(driver, user):
    print(user['username'])

    url = 'https://www.instagram.com/' + user['username'] + '/'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    results = getInstaFollowPostCounts(soup)
    instaFollowers = results[0]
    instaFollowing = results[1]
    instaPosts = results[2]

    instaRatio = min(max(instaFollowers/(instaFollowing or 1), 1/3), 3)
    if instaPosts>=200:
        instaPostMultiplier = 1.1
    elif instaPosts>=50:
        instaPostMultiplier = 1
    elif instaPosts >=10:
        instaPostMultiplier = .75
    else:
        instaPostMultiplier = .5

    instaScore=0
    #check if Private
    private = bool(driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2'))

    if private or instaPosts==0:
        print('is private')
        instaScore = math.log(instaFollowers *.1875 * instaRatio * instaPostMultiplier)
        #time.sleep(random.uniform(3,10))

    else:
        #time.sleep(random.uniform(2,5))
        pageSource = driver.page_source
        instaLikes = getDataFromObjectString(pageSource,'edge_liked_by":{"count":', '}')
        instaComments = getDataFromObjectString(pageSource,'edge_media_to_comment":{"count":', '}')

        instaScore = math.log((mean(instaLikes) + 2*mean(instaComments or [0])) * instaRatio * instaPostMultiplier)

        #clickInstaPictures(driver)


    return instaScore

def getInstaFollowPostCounts(soup):
    temp = soup.find("meta", attrs={"property": "og:description"})
    description = []
    if temp:
        description = temp.get('content').split()
    else:
        raise ConnectionError('Access Blocked')

    if 'm' in description[0]:
        instaFollowers = float(description[0][:-1]) * 1000000
    elif 'k' in description[0]:
        instaFollowers = float(description[0][:-1]) * 1000
    else:
        instaFollowers = int(description[0].replace(',', ''))

    if 'm' in description[2]:
        instaFollowing = float(description[2][:-1]) * 1000000
    elif 'k' in description[2]:
        instaFollowing = float(description[2][:-1]) * 10000
    else:
        instaFollowing = int(description[2].replace(',', ''))

    if 'm' in description[4]:
        instaPosts = float(description[4][:-1]) * 1000000
    if 'k' in description[4]:
        instaPosts = float(description[4][:-1]) * 1000
    else:
        instaPosts = int(description[4].replace(',', ''))
    return (instaFollowers, instaFollowing, instaPosts)


def getDataFromObjectString(pageSource, key, endChar):
    values = []
    for m in re.finditer(key, pageSource):
        endIndex = m.end()
        startIndex = m.end()
        while(pageSource[endIndex]!=endChar):
            endIndex+=1
        values.append(int(pageSource[startIndex: endIndex]))
    return values


def clickInstaPictures(driver):
    #if not priate click on a few pictures
    #get rid of login popup
    popup = driver.find_elements_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/div/button')
    if len(popup)==1:
        popup[0].click()

    posts = []
    for link in driver.find_elements_by_tag_name('a'):
        if 'https://www.instagram.com/p/' in link.get_attribute('href'):
            posts.append(link)

    for x in range(random.randint(0,3)):
        random.choice(posts).click()
        time.sleep(random.uniform(3,10))
        driver.find_element_by_xpath("//button[text()='Close']").click()
        time.sleep(random.uniform(2,5))


def scrapeTwitterAccount(handle):
    #print(python_tweets.show_user(screen_name="Beyonce")['listed_count'])

    twitterFollowers = python_tweets.show_user(screen_name=handle)['followers_count']
    twitterTweetCount = python_tweets.show_user(screen_name=handle)['statuses_count']
    timeline = python_tweets.get_user_timeline(screen_name=handle, include_rts='false')
    tweetReception = [(tweet['favorite_count'], tweet['retweet_count']) for tweet in timeline]
    twitterAvgFavorite = sum([reception[0] for reception in tweetReception])/(len(tweetReception) or 1)
    twitterAvgRetweet = sum([reception[1] for reception in tweetReception])/(len(tweetReception) or 1)

    if twitterTweetCount>=20000:
        twitterTweetMultiplier = 1.2
    elif twitterTweetCount>=5000:
        twitterTweetMultiplier = 1.1
    elif twitterTweetCount>=500:
        twitterTweetMultiplier = 1
    elif twitterTweetCount >=100:
        twitterTweetMultiplier = .75
    else:
        twitterTweetMultiplier = .5

    #favorites + 4 rewteets + followers/500 + tweet count
    twitterScore = math.log((twitterAvgFavorite + 4*twitterAvgRetweet + twitterFollowers/500) * twitterTweetMultiplier)
    print("twitterScore")
    print(twitterScore)


def scrapeYoutubeAccount(driver, user):
    driver.get("https://www.youtube.com/user/200000028/about")
    subscriberCount = driver.find_element_by_id('subscriber-count').get_attribute('innerHTML').split()[0]
    subscriberCount = int(subscriberCount.replace(',', ''))
    print(subscriberCount)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    description = soup.find_all("yt-formatted-string", class_="style-scope ytd-channel-about-metadata-renderer")

    for tag in description:
        if 'views' in (tag.string or " "):
            youtubeViews = tag.string.split()[0]
            youtubeViews = int(youtubeViews.replace(',', ''))
            print(youtubeViews)
            break

    youtubeScore = math.log(youtubeViews + 1000* subscriberCount)
    print(youtubeScore)


def scrapeFacebookAccount(user):
    with urllib.request.urlopen('https://www.facebook.com/beyonce/') as html:
        read = html.read()
        soup = BeautifulSoup(read, 'html.parser')
        description = soup.find("meta", attrs={"name": "description"}).get('content').split()
        facebookLikes = description[1]
        print(facebookLikes)
        facebookTalkingAbout = description[4]
        print(facebookTalkingAbout)


def getHandleFromName(user):
    if user['fullName']:
        temp = user['fullName'].replace(' ', '%20')
        url = 'https://twitter.com/search?f=users&vertical=default&q=' + temp
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        temp = soup.find("b", class_="u-linkComplex-target")

        if temp:
            print(temp.text)
            user['twitterHandle'] = temp.text
        else:
            print(user['username'] + " has no handle")

if __name__ == "__main__":
    main()
