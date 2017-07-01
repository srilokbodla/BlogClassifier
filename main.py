import urllib2
from bs4 import BeautifulSoup


def getAllDoxyDonkeyPosts(url, links):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response)
    for a in soup.findAll('a'):
        try:
            url = a['href']
            title = a['title']
            if title == 'Older Posts':
                print title, url
                links.append(url)
                getAllDoxyDonkeyPosts(url, links)
        except:
            title = ''
    return


blogUrl = 'http://doxydonkey.blogspot.in'
links = []
getAllDoxyDonkeyPosts(blogUrl, links)


def getDoxyDonkeyText(testUrl):
    request = urllib2.Request(testUrl)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response)
    mydivs = soup.findAll("div", {"class": 'post-body'})

    post = []
    for div in mydivs:
        post += map(lambda p: p.text.encode('ascii', errors='replace').replace("?", " "), div.findAll('li'))
    return post


doxyDonkeyPosts = []

for link in links:
    doxyDonkeyPosts += getDoxyDonkeyText(link)
print doxyDonkeyPosts

from sklearn.feature_extraction.text import TfidfVectorizer

vector = TfidfVectorizer(max_df=0.5,min_df=2,stop_words='english')
x=vector.fit_transform(doxyDonkeyPosts)

print x

from sklearn.cluster import KMeans

km=KMeans(n_clusters=3 , init='k-means++' , max_iter=100 , n_init=1 , verbose=True)

km.fit(x)

import numpy as np
np.unique(km.labels_,return_counts=True)

text={}
for i , cluster in enumerate(km.labels_):
    oneDocument=doxyDonkeyPosts[i]
    if cluster not in text.keys():
        text[cluster]=oneDocument
    else:
        text[cluster]+=oneDocument
