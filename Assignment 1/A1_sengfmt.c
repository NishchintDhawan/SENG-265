/*
 * UVic SENG 265, Fall 2018, A#1
 *
 * This will contain a solution to sengfmt. In order to complete the
 * task of formatting a file, it must open and read the file (hint:
 * using fopen() and fgets() method) and format the text content base on the
 * commands in the file. The program should output the formated content
 * to the command line screen by default (hint: using printf() method).
 *
 * Supported commands include:
 * ?width width :  Each line following the command will be formatted such
 *                 that there is never more than width characters in each line
 * ?mrgn left   :  Each line following the command will be indented left spaces
 *                 from the left-hand margin.
 * ?fmt on/off  :  This is used to turn formatting on and off.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <time.h>
#define BIGLINE (200000)


int size;
int fmt=0;                   /* flag to check if the fmt is on or off*/
int linesize=0               /* length of the input line*/
int widthvalue=0;            /* amount of width */
int marginvalue=0;           /* amount of margin*/
char output[BIGLINE];        /*Stores the output after formatting is done*/



 /*Function to check the patterns input*/

int formatchecker(char* line){
   char line2[BIGLINE];
  strncpy (line2, line, BIGLINE);

  char* readword = strtok (line2, " ");

  if ( !strncmp(line2, "?width", BIGLINE) ) {   /*Checks for width command*/
    fmt =1;
    widthvalue = atoi( strtok(NULL," ") );
    return 1;
  }
  else if ( strncmp(line2, "?mrgn", BIGLINE)==0 ) {      /*Checks for mrgn (margin) command*/
   marginvalue = atoi(strtok(NULL," "));

    return 1;
  }

   else if ( strcmp(readword, "?fmt")==0 ) {     /*Checks for fmt (format on/off) command*/
    readword = strtok(NULL," ");
    if ( strcmp(readword, "off\n")==0 ) {
      fmt = 0;
    }
    else if( strcmp(readword,"on\n")==0){
      fmt = 1;
    }

    return 1;
  }



  return 0;
  }


int main(int argc, char *argv[]) {

     FILE* ifp;
     ifp = fopen (argv[1], "r");
  if (ifp == NULL) {
    return -1;
  }
    char line[BIGLINE];
    char dumper[BIGLINE];


    char storeword[BIGLINE];


    int count=0;

   int val =1;
   int j=0;
   int i=0;
   int wordchecker =0;

int fullstop=0;
linesize = 0;
int marginflag =0;
while( fgets(line, 80,ifp)!= NULL){          /*Gets the content of the file line by line */


       char line3[BIGLINE];
       strcpy(line3,line);
      if(formatchecker(line3)==1){
        continue;
      }

 if(fmt ==1){
        if(marginvalue!=0  &&marginflag==0){         /* If fmt is on, we make changes to the file contents */
                while(count<marginvalue){
                printf(" ");
                count++;
            }
            marginflag =1;
            count=0;
            }
       if (!strncmp (line3, "\n", 1) ) {
      strcat (output, "\n\n");
      linesize = 0;
  if(marginvalue!=0){
        while(count<marginvalue-1){
                    strcat(output," ");
                    count++;
                    linesize++;
                }
               count=0;
  }
    }
    char * readword = strtok(line3," \n");
    while(readword){

       if(linesize>0 && (linesize+1+strlen(readword)<=widthvalue) ){
        strcat(output," ");
        linesize++;
       }

        else
        {
          if (linesize>0){
            strcat(output,"\n");

            {
               if(marginvalue!=0){
               linesize =0;
              while(count<marginvalue){
                    strcat(output," ");
                    count++;
                    linesize++;
                }
               count=0;
                }
              else{
                  linesize=0;
              }
            }
          }
        }
         if(linesize==0){
            linesize =marginvalue;

         }
           strncat(output,readword,BIGLINE);
           linesize+=strlen(readword);

     readword = strtok(NULL, " \n");
    }

}
else if(fmt ==0){
 strcat(output, line);
 }
}


  printf("%s",output);

	exit(0);
}













