import os
import subprocess

# https://code.google.com/archive/p/pyswip/wikis/Examples.wiki

# test = subprocess.Popen(["ping","-W","2","-c", "1", "192.168.1.70"], stdout=subprocess.PIPE)

# output = test.communicate()[0]

def main():
    '''This is our main function!'''

    print "starting music app...\n"

    #devnull = open('/dev/null', 'w')

    while True:
        print '\n'
        print "\nOptions:\n1. Get Artist Info\n2. Get Custom Playlist"
        user_input = input("Choose a function: ")
        if (user_input == 1):
            artist = raw_input('Which artist would you like to search:')
            # Still need to find way to pass param artist to the prolog.pl file
            pipe = subprocess.Popen("swipl --quiet prolog.pl", shell=True, stdout=subprocess.PIPE).stdout
            output = pipe.read()
        elif (user_input == 2):
            #unimplemented
            os.system("swipl --quiet prolog.pl")
        else:
            print "Invalid choice\n"
        
        print '\n\n\nThe following is the ouput from prolog.pl:\n\n'
        print output
    
    return


if __name__ == '__main__':
    main()