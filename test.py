'''Version 0.1'''
from bs4 import BeautifulSoup
import urllib

def get_names(soup,dct):
    dct['artist_ids'] = []
    # artists = soup.find_all("artist")
    # for element in artists:
    #     print element
    #     # if element != '' and 'artist' in element.parent:
    #     #     dct['names'].append(str(element.text).lower())
    for tag in soup.find_all("artist"):
        print tag.get('id')
        dct['artist_ids'].append(tag.get('id'))
    return

def main():
    '''This is our main function!'''
    r = urllib.urlopen("http://musicbrainz.org/ws/2/artist?query=arid:0383dadf-2a4e-4d10-a46a-e9e041da8eb3").read()
    soup = BeautifulSoup(r, "lxml")

    answers = {}
    get_names(soup, answers)
    print answers
    return


if __name__ == '__main__':
    main()