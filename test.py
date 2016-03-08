'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def get_names(dct):
    artist = str(raw_input('Which artist would you like to search: '))
    artist.replace(' ', '%')
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=artist:\""+artist+"\"").read()
    soup = BeautifulSoup(r, "lxml")
    dct['artist_ids'] = []
    tag = soup.find("artist-list").find("artist")
    artistID = tag.get('id')
    dct['artist_ids'].append(tag.get('id'))
    # print tag.get('id')
    #     dct['artist_ids'].append(tag.get('id'))
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
            get_names(answers)
            print answers

        else:
            print "Invalid choice\n"
    
    return


if __name__ == '__main__':
    main()