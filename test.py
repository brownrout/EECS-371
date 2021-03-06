'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib
from yt import getYTLink
import string

def isAscii(s):
    for c in s:
        if c not in string.ascii_letters:
            return False
    return True

def get_similar_artists(artist, tags):
    """ Search for similar artist based on tags from musicbrainz """

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
    """ Search for all information on artist from musicbrainz xml """

    artist = artist_dict["artist_name"]

    # create the new url for query
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=artist:\""+artist.replace(' ','%20')+"\"").read()
    soup = BeautifulSoup(r, "lxml")

    artist_dict['artist_id'] = ""
    # grab artist id from the query page
    if (soup.find("artist-list").find("artist") is not None):
        artist_dict['artist_id'] = soup.find("artist-list").find("artist").get("id")
    else:
        return

    # get artist facts
    get_facts(artist_dict, soup)

    # grab tags from query
    tags = list()
    for tag in soup.find_all("tag"):
        if isAscii(tag.find("name").text):
            tags.append(tag.find("name").text)
    artist_dict['tags'] = tags



    # grab the similar artists
    artist_names = get_similar_artists(artist_dict['artist_name'], artist_dict['tags'])
    artist_dict['similar artists'] = artist_names

    return

def get_facts(input_dict, soup):
    """ Search for potential facts from musicbrainz xml """

    if soup.find("artist").find("disambiguation"):
        input_dict['disambiguation'] = soup.find("artist").find("disambiguation").text
    # grab the area
    if soup.find("artist").find("area"):
        input_dict['area'] = soup.find("artist").find("area").text
    # grab the beginarea
    if soup.find("artist").find("begin-area"):
        input_dict['beginarea'] = soup.find("artist").find("begin-area").find("name").text
    # grab the endarea
    if soup.find("artist").find("end-area"):
        input_dict['endarea'] = soup.find("artist").find("end-area").find("name").text
    # grab the ended
    if soup.find("artist").find("ended"):
        input_dict['ended'] = soup.find("artist").find("ended").text
    # grab the end
    if soup.find("artist").find("end"):
        input_dict['end'] = soup.find("artist").find("end").text
    # grab the begin
    if soup.find("artist").find("begin"):
        input_dict['begin'] = soup.find("artist").find("begin").text
    return

def pretty_print_artist_facts(input_dict):
    """ Print artist facts if applicable """

    pretty_statements = list()
    a_name = input_dict.get("artist_name")

    # search for potential facts to print in artist_dict
    if input_dict.get('disambiguation'):
        pretty_statements.append("disambiguation: {}".format(input_dict.get('disambiguation')))
    if input_dict.get('area'):
        pretty_statements.append("area: {}".format(input_dict.get('area')))
    if input_dict.get('begin'):
        pretty_statements.append("born/started in: {}".format(input_dict.get('begin')))
    if input_dict.get('beginarea'):
        pretty_statements.append("begin Area: {}".format(input_dict.get('beginarea')))
    if input_dict.get('end'):
        pretty_statements.append("end: {}".format(input_dict.get('end')))
    elif input_dict.get('ended'):
        pretty_statements.append("ended: {}".format(input_dict.get('ended')))
    if input_dict.get('endarea'):
        pretty_statements.append("end area: {}".format(input_dict.get('endarea')))
    if len(pretty_statements) == 0:
        pretty_statements.append("there doesn't seem to be much on this artist. congratulations, you're officially a hipster.")

    # print all facts and return
    print "\n".join(pretty_statements)
    pretty_statements = list()
    return


def build_playlist(artist_dict):
    """ Build a playlist of songs for user """

    artist = artist_dict["artist_name"]

    # create the new url for query
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=artist:\""+artist.replace(' ','%20')+"\"").read()
    soup = BeautifulSoup(r, "lxml")

    artist_dict['artist_id'] = ""
    # grab artist id from the query page
    if (soup.find("artist-list").find("artist") is not None):
        artist_dict['artist_id'] = soup.find("artist-list").find("artist").get("id")
    else:
        return

    # grab tags from query
    tags = list()
    for tag in soup.find_all("tag"):
        if isAscii(tag.find("name").text):
            tags.append(tag.find("name").text)
    artist_dict['tags'] = tags

    # grab the similar artists
    track_list = get_tracks(artist_dict['artist_name'], artist_dict['tags'])
    artist_dict['playlist-one'] = track_list

    return

def get_tracks(artist, tags):
    """ Gather tracks and youtube urls from tags given in musicbrainz xml """
    # construct search url
    url = "http://musicbrainz.org/ws/2/work?query="
    stop = len(tags)-1
    for index, tag in enumerate(tags):
        url += "tag:" + tag.replace(' ','%')
        if index != stop:
            url += "+"

    # get response
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, "lxml")

    # parse response
    track_names = list()
    artists = []

    for element in soup.find("work-list").find_all("work"):
        if (element.get('type') == 'Song') and element.find("relation-list").find("name"):
            _score = element.get('ext:score')
            _name = element.find("title").text
            _artist = element.find("relation-list").find("name").text
            try:
                _video = getYTLink(_name + " " + _artist)
            except KeyError:
                continue
            if (_artist not in artists):
                artists.append(_artist)
                track_names.append([_name,_artist,_score,_video])

    return track_names

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
        print "\noptions:\n1. get artist info\n2. find similar artists\n3. build playlist based off artist\n"
        user_input = input("choose a function: ")
        if (user_input == 1):
            print "\n"
            if len(artist_dict) <= 1:
                get_artist_info(artist_dict)
            pretty_print_artist_facts(artist_dict)
            print "\n"
        elif (user_input == 2):
            if len(artist_dict) <= 1:
                get_artist_info(artist_dict)
            print "\n"
            if (artist_dict['artist_id'] != ""):
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
            else:
                print "hrmm, something went wrong, please try a new artist\n"

        elif (user_input == 3):
            print "This may take a second...\n"
            build_playlist(artist_dict)
            print "\n"
            if (artist_dict['artist_id'] != ""):
                if len(artist_dict['playlist-one']) == 0:
                    print "sorry, we couldn't build a playlist of songs similar to " + artist_dict['artist_name'].lower()
                elif len(artist_dict['playlist-one']) <= 10:
                    print "the top " + str(len(artist_dict['playlist-one'])) + " songs similar to " + artist_dict['artist_name'].lower() + " are:"
                else:
                    print "the top 10 of " + str(len(artist_dict['playlist-one'])) + " most similar songs related to " + artist_dict['artist_name'].lower() + " are:"
                for index,x in enumerate(artist_dict['playlist-one']):
                    if index <= 9:
                        print x[0].lower() + " / " + x[1].lower() + " - score: " + str(x[2]) + " - video: " + x[3]
                print "\n"
            else:
                print "hrmm, something went wrong, please try a new artist\n"
        else:
            print "invalid choice\n"
        artist_dict = dict()

    return


if __name__ == '__main__':
    main()
