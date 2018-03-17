# HKEX

The Project:  
The program downloads the daily quotation web pages, in a specified range of dates, which is made available 
by Hong Kong Stock Exchange to the pulbic via its website.  Then the program will go on to extract the summary 
of the day's activities and accumulated them in csv format.

The scripts:  
hkex.py is the main script that combined both part1.py and part2.py.  
myfunctions.py contains all functions for the project.  
part1.py downloads the daily quotation webpage from HKEX.  
part2.py extracts the data from the downloaded webpage and stored them in csv-format. 

Future work:  
This is my first python project and it has been fun.  I am planning to add a filter routine to extract  
quotation of a particular stock of interest.

Remarks:  
I have an earlier version that reads the webpage and converts the data directly into individual file which represents  
each individual stock.  The project works however it took a long time for windows to run, could be due to a lot
of file handlings.  Linux handles the same script better even on older machine.  It also generated a large number of 
small files.  So I switched to save the webpage preserving the raw data before extracting the data to save them in one 
csv file.
