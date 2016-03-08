'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def get_similar_artists(artist, tags):
    # construct search url
    url = "http://musicbrainz.org/ws/2/artist?query="
    for tag in tags:
        url += "+tag:"+tag.replace(' ','%')

    # get response
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")

    # parse response
    artist_names = list()
    for element in soup.find_all("artist"):
        _name = element.find("name").text
        if _name.lower() != artist.lower():
            artist_names.append(_name)

    return artist_names

def get_artist_info():

    artist_dict = dict()
    #query user for the artist, and make sure it is url friendly
    artist = str(raw_input('Which artist would you like to search: '))
    artist_dict['artist_name'] = artist

    # create the new url for query
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=artist:\""+artist.replace(' ','%')+"\"").read()
    soup = BeautifulSoup(r, "lxml")

    # grab artist id from the query page
    artist_dict['artist_id'] = soup.find("artist-list").find("artist").get("id")

    # grab tags from query
    tags = list()
    for tag in soup.find_all("tag"):
        tags.append(tag.find("name").text)
    artist_dict['tags'] = tags

    # grab the similar artists
    artist_names = get_similar_artists(artist_dict['artist_name'], artist_dict['tags'])
    artist_dict['similar artists'] = artist_names

    return artist_dict

def main():
    '''This is our main function!'''

    print "starting music app...\n"

    while True:
        print '\n'
        print "\nOptions:\n1. Get Artist Info"
        user_input = input("Choose a function: ")
        if (user_input == 1):
            artist_info = get_artist_info()
            print artist_info
        else:
            print "Invalid choice\n"

    return


if __name__ == '__main__':
    main()