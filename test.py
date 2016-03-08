'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def get_similar_artists(artist, tags):
    # construct search url
    url = "http://musicbrainz.org/ws/2/artist?query="
    stop = len(tags)-1
    for index, tag in enumerate(tags):
        url += "tag:" + tag.replace(' ','%')
        if index != stop:
            url += "+"

    # get response
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")

    # parse response
    artist_names = list()
    for element in soup.find_all("artist"):
        _score = element.get('ext:score')
        _name = element.find("name").text
        if _name.lower() != artist.lower():
            artist_names.append([_name,_score])

    return artist_names

def get_artist_info(artist_dict):

    artist = artist_dict["artist_name"]

    # create the new url for query
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=artist:\""+artist.replace(' ','%')+"\"").read()
    soup = BeautifulSoup(r, "lxml")

    print "http://musicbrainz.org/ws/2/artist?query=artist:\""+artist.replace(' ','%')+"\""

    # grab artist id from the query page
    artist_dict['artist_id'] = soup.find("artist-list").find("artist").get("id")
    # grab artists disambiguation
    if soup.find("artist").find("disambiguation"):
        artist_dict['disambiguation'] = soup.find("artist").find("disambiguation").text
    # grab the area
    #artist_dict['location'] = soup.find("artist").find("area").find("_name")



    # grab tags from query
    tags = list()
    for tag in soup.find_all("tag"):
        tags.append(tag.find("name").text)
    artist_dict['tags'] = tags



    # grab the similar artists
    artist_names = get_similar_artists(artist_dict['artist_name'], artist_dict['tags'])
    artist_dict['similar artists'] = artist_names

    return

# artist_dict = dict()
# #query user for the artist, and make sure it is url friendly
# artist = str(raw_input('Which artist would you like to search: '))
# artist_dict['artist_name'] = artist

def main():
    '''This is our main function!'''

    print "starting music app...\n"
    artist_dict = dict()

    while True:
        artist = str(raw_input('enter an artist: '))
        artist_dict['artist_name'] = artist
        print "\noptions:\n1. find similar artists\n"
        user_input = input("choose a function: ")
        if (user_input == 1):
            get_artist_info(artist_dict)
            print "\n"
            if len(artist_dict['similar artists']) == 0:
                print "sorry, we couldn't find any artists similar to " + artist_dict['artist_name'].lower()
            elif len(artist_dict['similar artists']) <= 10:
                print "the top " + str(len(artist_dict['similar artists'])) + " artists similar to " + artist_dict['artist_name'].lower() + " are:"
            else:
                print "the top 10 of " + str(len(artist_dict['similar artists'])) + " most similar artists related to " + artist_dict['artist_name'].lower() + " are:"
            for index,x in enumerate(artist_dict['similar artists']):
                if index <= 9:
                    print x[0].lower() + " - score: " + str(x[1])
            print "\n"
            print artist_dict
        else:
            print "invalid choice\n"

    return


if __name__ == '__main__':
    main()