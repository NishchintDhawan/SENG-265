#!/opt/local/bin/python

import sys
import re
import argparse
import calendar

dict = {'fmt':0, 'mrgn':0, 'width':160 , 'cap': False, 'marginflag':1,'replaceflag':0 ,'rep': "" , 'new': "" ,"monthabbr": False}

class Formatter:
    """This is the definition for the class"""

    
    #fmt 1 means on , fmt 0 means off.
    formatted=""

    def __init__(self, filename=None, inputlines=None):
        global formatted

        if (filename != None):
            formatted = self.formatfiles(filename)
        else:
            formatted = self.formatfiles(inputlines)

        
    #..........................detect the formatting style.............................#
    def detectline(self,line):
        global dict 
        formatcmd = line.split()
 
        if formatcmd[0] == "?fmt":
            if formatcmd[1]=="off":
                dict['fmt'] = 0
                dict['marginflag']=False
                
            elif formatcmd[1] == "on":
                dict['marginflag']=True
                if dict['width']!=160:
                    dict['fmt'] = 1
                    
            return 0
        
        if formatcmd[0]=="?maxwidth":
            if formatcmd[1][0]=="-":
                dict['width'] = dict['width'] - int(formatcmd[1][1:])
                return 0
            if formatcmd[1][0] == "+":
                dict['width']= dict['width']+ int(formatcmd[1][1:])
                return 0            
            else:
                dict['width'] = int(formatcmd[1])
                dict['fmt'] = 1
                return 0		


        if formatcmd[0] == "?mrgn":
            dict['marginflag']=1
            if formatcmd[1][0]=="-":
                dict['mrgn'] = dict['mrgn']-int(formatcmd[1][1:]) 
                if dict['mrgn'] <0:
                    dict['mrgn'] =0	
                return 0
		
            if formatcmd[1][0] == "+":
                dict['mrgn'] += int(formatcmd[1][1:])
                if dict['mrgn'] > dict['width'] -20:
                    dict['mrgn'] = dict['width'] -20
                return 0
            else:
                dict['mrgn'] = int(formatcmd[1])         		
                return 0
				
				
        if formatcmd[0]=="?cap":
            if formatcmd[1]=="off":
                dict['cap'] = False
            elif formatcmd[1]=="on":
                dict['cap'] = True
            return 0

        if formatcmd[0]=="?replace":
            dict['rep']= formatcmd[1]
            dict['new']= formatcmd[2] 
            dict['replaceflag']= 1
            return 0

        if formatcmd[0]=="?monthabbr":
            if formatcmd[1]== "on":
                dict['monthabbr']=True
            return 0

        return 1  


    #..........................getmonth.................................#

    def getmonth(self,month):
        string = ""
        index = int(month[1]) + 10* int(month[0])
        string = calendar.month_abbr[index]
   
        return string
        
    #.....................justify.....................................#


    def justify2(self,string):
        global dict
        justifylist= string.split()
        y=""
		
        if len(justifylist)>1:
            i=0
            word = ""
            for i in range(0,len(justifylist)):
	            justifylist[i] += " "
            i=0
            word=justifylist[len(justifylist)-1]     
            word = word[:-1]
            justifylist[len(justifylist)-1] =word	
            word = ""
            additionalspaces = dict['width'] - len(string)
            for i in range(additionalspaces):
                word = justifylist[i%(len(justifylist)-1)] 
                word = word+" "
                justifylist[i%(len(justifylist)-1)] = word
            word = ""

        for i in range(dict['mrgn']):
	        y+=" "
        for j in range(0,len(justifylist)):
            y+=justifylist[j]
        return y

    #...............................formatfiles...................................#

    def formatfiles(self,files):
        global dict
        output =""
        string= ""
        linelength =0
        testerflag=0
        dict['marginflag'] =1
        margin=""	
        
        for line in files:

            tester = line.split()
            if tester == []:
                if dict['fmt']==1:
                #if previous was empty, then '\n' only once. (more than 1 empty line).
                    if testerflag==1 :
                        if string!="":
                            output+= self.justify2(string) +"\n"
                        else:
                            output+=string+"\n"
                    else:
                        if string!="":
                            output += self.justify2(string)+"\n\n"
                        else: 
                            output+=string +"\n\n"
                else: 
                    output+= "\n"
                string = ""
                dict['marginflag']=1
                linelength= dict['mrgn']
                testerflag =1
                continue

            else:
                testerflag =0

            if self.detectline(line) == 0:
                continue
      

            if  dict['marginflag']==1:
                for i in range(dict['mrgn']):
                    string+= " "
                i=0
                dict['marginflag']=0
                linelength=dict['mrgn']

            if dict['replaceflag']==1:
                line = re.sub( dict['rep'], dict['new'], line)
            linewords = line.split()
                    
            linewords2 = linewords
            if ( dict['monthabbr']==True ):
                for k in range(0,len(linewords2)):
                    p = re.findall( r'^([00-12]\d{1})(-|\.|\/)([00-31]\d{1})(-|\.|\/)([00-99]\d{3})',linewords2[k])
                if  p:
                    change =""
                    initial =""
                    word = linewords2[k]
                    p =p[0]
                    mon = p[0]
                    day = p[2]
                    year = p[4]
                    month = self.getmonth(mon)
                    for i in p:
                         initial+=i
                    change = month +". "+day+", "+year
                    word = re.sub(initial,change,word)
                    wordlist = word.split()
                    linewords2[k] = wordlist[0]
                    wordlist = word.split()
                    for x in range(1,len(wordlist)):
                        linewords2.insert(k+1,wordlist[x])
                        k+=1
                                    
            linewords = linewords2

        #........................ if fmt is 1......................#
            if dict['fmt'] ==1:

		#tokenize each word using split().
		##start loop for each tokenized word ##
                for word in linewords:
                    
                    if ( dict['monthabbr']==True ):
                        p = re.findall( r'^([00-12]\d{1})(-|\.|\/)([00-31]\d{1})(-|\.|\/)([00-99]\d{3})',word)
                        if  p:
                            p =p[0]
                            mon = p[0]
                            day = p[2]
                            year = p[4]
                            month = self.getmonth(mon)
                            word = month +". "+day+", "+year


                    if linelength + len(word)+1 > dict['width']:
                        output = output+  self.justify2(string)+'\n'
                        string= ""

                        for i in range(dict['mrgn']):
                            string+=" "
                        linelength=dict['mrgn'] 

                    if linelength != dict['mrgn']:
                        string+=" "      
                        linelength+=1      
                    
                    if dict['cap']==True:
                        string+= word.upper()

                    else:
                        string+=word 
                    linelength+=len(word)        
           
         #......................if fmt is 0....................#
            if dict['fmt'] ==0:
                margin=""
                for i in range(dict['mrgn']):
                    margin+=" "
                output+=margin
                margin =""
                if (dict['monthabbr'] == True):
                    for word in linewords:
                        output+= word +" "
                    output = output[:-1]
                    output += '\n'
                else:
                    output+=line+'\n'
                
        margin =""
        for i in range(dict['mrgn']):
            margin+=" "
        
	# last line is left here. 
        
        if (dict['fmt']==1 and string!= margin and string!=""):
            output += self.justify2(string)
        else:
            if (string!= margin and string!=""):
                output+= string

        output1 =""
        if output[-1]=='\n'  :
            output1 = output[:-1]
        else: 
            output1 = output
    
        return output1

    #..........used to return the lines in form of a list............#
    def get_lines(self):
        global formatted
        y = formatted.split("/r/n")
        return y
 
def main ():
    #..........if called directly.................#
    inputtext = []
   
    #.......if the file name is not specified....................#
    if len(sys.argv)==1:
        for line in sys.stdin:
            inputtext.append(line)
    else:
        with open(sys.argv[1]) as f:
            inputtext = f.readlines()
    
    #...........Using the Formatter class to format the input.........#     


    myformat = Formatter(inputlines=inputtext)
    outputlines = myformat.get_lines()

    for line in outputlines:
        print(line)
    
if __name__ == "__main__":
    main()
