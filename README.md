# HKEX

__The Project:__
The program perfroms the following to the daily quotation web pages which is made available
by Hong Kong Stock Exchange to the pubic via its website.

1. Download the daily quotation webpage  
2. Extract summary of the day's performance of all stocks traded on the day  
3. Collect the data of any particular company of interest into a *csv* file  

__The scripts:__
hkex.py is the main script that will control the download and data extraction.  
myfunctions.py contains all functions for the project.  

__Future work:__
Considering to read the *csv* file with *R* and .....

Remarks:
__2021-05-03__
The downloaded html files take up a lot of space, most of the space for this
project. Converting them to text file and storing them together double the
storage space.  So project revert back to extract data directly from html files.

__2021-05-2__
Delete all CSV files in /Data/ directory and run the latest script.
Found error when extracting data form line starting with html tag.  Instead of
cleaning up the html tag and escape sequence as we extract data, the program
will create a text file by stripping in line html tags and converting the escape
sequence.  Then the data will be extracted from the resulting text file after
download all webpages.
