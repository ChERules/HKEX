# HKEX

The Project:  
The program perfroms the following to the daily quotation web pages which is made available
by Hong Kong Stock Exchange to the pubic via its website.

1) Download the daily quotation webpage  
2) Extract summary of the day's performance of all stocks traded on the daily  
3) Collect the date of any particular company of interest into a csv file  

The scripts:  
hkex.py is the main script that will control the download and data extraction.  
myfunctions.py contains all functions for the project.  

Future work:  
Considering to read the csv file with R and .....

Remarks:  
I have an earlier version that reads the webpage and converts the data directly into
individual file which represents each individual stock.  The project works however it
took a long time for windows to run, could be due to a lot of file handlings.  Linux
handles the same script better even on older machine.  It also generated a large number
of small files.  So I switched to save the webpage preserving the raw data before
extracting the data to save them in one csv file.
