'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def get_artist_info(dct, artist):
    
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

    # build the query which will grab similar artists
    url = "http://musicbrainz.org/ws/2/artist?query=tag:"
    stop = len(dct['tags'])-1
    for index, x in enumerate(dct['tags']):
        url += x
        if index != stop:
            url += "%20AND%20tag:"

    # grab the similar artists
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")
    artist_names = list()
    for element in soup.find_all("artist"):
        _score = element.get('ext:score')
        _name = element.find("name").text
        if _name.lower() != dct["artist_name"].lower() and int(_score) > 60:
            artist_names.append([_name,_score])
    dct['similar artists'] = artist_names


    return

def main():
    '''This is our main function!'''

    print "starting music app...\n"

    while True:
        answers = {}
        #query user for the artist, and make sure it is url friendly
        artist = str(raw_input('enter an artist: '))
        answers['artist_name'] = artist
        print "\noptions:\n1. find similar artists\n"
        user_input = input("choose a function: ")
        if (user_input == 1):
            get_artist_info(answers, artist.replace(' ', '%'))
            print "\n"
            print "we found " + str(len(answers['similar artists'])) + " artists related to " + answers['artist_name'].lower() + ":"
            for x in answers['similar artists']:
                print x[0].lower() + " - score: " + str(x[1])
            print "\n"
        else:
            print "invalid choice\n"
    
    return


if __name__ == '__main__':
    main()