import requests
from bs4 import BeautifulSoup
import nltk

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer 90fDPe_mgCL9gXyA9bZBge-mXZHZO4p-tyge9rByM0iSJDTULzVLYQpwawHnHecf'}


def lyrics_from_song_api_path(song_title,artist_name):
  search_url = base_url + "/search"
  data = {'q': song_title}
  response = requests.get(search_url, data=data, headers=headers)
  json = response.json()
  song_info = None
  for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower() or hit["result"]["primary_artist"]["name"].lower() in artist_name.lower() or artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
      song_info = hit
      break
  if song_info:
    song_api_path = song_info["result"]["api_path"]
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
    return lyrics
  else:
    return ""

def vocab(d):
    for i in range(len(d)):
        a=""
        for j in range (len(d[i])-1):
            a=a+lyrics_from_song_api_path(d[i][j+1],d[i][0]) #looks to the first item in the list for the artist name.
        print d[i][0]
        print len(set(nltk.word_tokenize(a)))
        print len(nltk.word_tokenize(a))


def list(s):
    last=0
    p=[]
    for n in range(len(s)):
        if s[n]=='\n':
            p=p+[s[last:n]]
            last=n+1
        if n==len(s)-1:
            p=p+[s[last:n+1]]            
    return p

#example use below:

kendrick="""Fuck Your Ethnicity
Hol' Up
A.D.H.D
No Make-Up (Her Vice)
Tammy's Song (Her Evils)
Chapter Six
Ronald Reagan Era (His Evils)
Poe Mans Dreams (His Vice)
The Spiteful Chant
Chapter Ten
Keisha's Song (Her Pain)
Rigamortus
Kush & Corinthians (His Pain)
Blow My High (Members Only)
Ab-Soul's Outro
HiiiPoWeR
Sherane A.K.A Master Splinter's Daughter
Bitch, Don't Kill My Vibe
Backseat Freestyle
The Art Of Peer Pressure
Money Trees
Poetic Justice
Good Kid
m.A.A.d City
Swimming Pools (Drank)
Sing About Me, I'm Dying Of Thirst
Real
Compton
The Recipe
Wesley's Theory
For Free? (Interlude)
King Kunta
Institutionalized
These Walls
u
Alright
For Sale? (Interlude)
Momma
Hood Politics
How Much A Dollar Cost
Complexion (A Zulu Love)
The Blacker The Berry
You Ain't Gotta Lie (Momma Said)
i
Mortal Man
BLOOD.
DNA.
YAH.
ELEMENT.
FEEL.
LOYALTY.
PRIDE.
HUMBLE.
LUST.
LOVE.
XXX.
FEAR.
GOD.
DUCKWORTH."""

vocab([["Kendrick Lamar"]+list(kendrick)]) #first item in the list is the artist name.