import os
import subprocess

# https://code.google.com/archive/p/pyswip/wikis/Examples.wiki

# mb_class(label).
# mb_class(artist).
# mb_class(work).
# mb_class(recording).
# mb_class(release).
# mb_class('release-group').
# mb_class(area).
# mb_class(url).



def artistSearchWrite (artist):
    target = open('prolog.pl', 'w')
    line1 = ":- use_module(library(musicbrainz))."
    line2 = ":- mb_search(artist,\'" + artist + "\',_Score,E), forall(mb_facet(E,F),(print(F),nl))."
    line3 = ":- halt."
    target.write(line1)
    target.write("\n")
    target.write(line2)
    target.write("\n")
    target.write(line3)
    target.write("\n")
    target.close()

def clearFile(filename):
    target = open('prolog.pl', 'w').close()

def main():
    '''This is our main function!'''

    print "starting music app...\n"

    #devnull = open('/dev/null', 'w')

    while True:
        print '\n'
        print "\nOptions:\n1. Get Artist Info\n2. Get Custom Playlist"
        user_input = input("Choose a function: ")
        if (user_input == 1):
            artist = str(raw_input('Which artist would you like to search:'))
            artistSearchWrite(artist)
            pipe = subprocess.Popen("swipl --quiet prolog.pl", shell=True, stdout=subprocess.PIPE).stdout
            output = pipe.read()
            clearFile('prolog.pl')
        elif (user_input == 2):
            #unimplemented
            os.system("swipl --quiet prolog.pl")
        else:
            print "Invalid choice\n"
        
        print '\nThe following is the ouput from prolog.pl:\n\n'
        test = output.splitlines()
        print test
    
    return


if __name__ == '__main__':
    main()