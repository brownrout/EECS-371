'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def get_artist_info(dct):

    #query user for the artist, and make sure it is url friendly
    artist = str(raw_input('Which artist would you like to search: '))
    dct['artist_name'] = artist
    artist.replace(' ', '%')
    
    # create the new url for query
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=artist:\""+artist+"\"").read()
    soup = BeautifulSoup(r, "lxml")
    
    #grab artist id from the query page
    tag = soup.find("artist-list").find("artist")
    artistID = tag.get('id')
    dct['artist_id'] = tag.get('id')

    # create the new url for querying artist by id
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=arid:"+dct['artist_id']).read()
    soup = BeautifulSoup(r, "lxml")

    # grab the tags
    dct['tags'] = []
    tags = soup.find_all("tag")
    for element in tags:
        for child in element.children:
            dct['tags'].append(child.text.replace(' ', "%"))

    url = "http://musicbrainz.org/ws/2/artist?query="
    for x in dct['tags']:
        url += "+tag:"+x

    # grab the similar artists
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    artist_names = list()
    for element in soup.find_all("artist"):
        _name = element.find("name").text
        if _name.lower() != dct["artist_name"].lower():
            artist_names.append(_name)
    dct['similar artists'] = artist_names


    return

def main():
    '''This is our main function!'''

    print "starting music app...\n"

    while True:
        answers = {}
        print '\n'
        print "\nOptions:\n1. Get Artist Info"
        user_input = input("Choose a function: ")
        if (user_input == 1):
            get_artist_info(answers)
            print answers
        else:
            print "Invalid choice\n"
    
    return


if __name__ == '__main__':
    main()