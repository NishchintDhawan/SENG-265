#!/opt/local/bin/python

import sys
from formatter import Formatter
import fileinput

def main():
    inputtext =[]
    
    for line in fileinput.input():
        inputtext.append(line[:-1])

   #....if filename not given....#  
    
    f = Formatter(inputlines= inputtext) 
    y = f.get_lines()
    
   #....printing after formatting the input....#
    for line in y:
        print (line)


if __name__ == "__main__":
    main()
