import urllib
import urllib2
from bs4 import BeautifulSoup

# resource
# http://stackoverflow.com/questions/29069444/returning-the-urls-from-a-youtube-search

def getYTLink(text):
    textToSearch = text
    query = urllib.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    
    id = soup.find(attrs={'class':'yt-lockup-video'}).get('data-context-item-id')
    url = "https://www.youtube.com/watch?v=" + str(id)

    return url

def main():
    print getYTLink("kurt cobain you know you're right")


if __name__ == '__main__':
    main()