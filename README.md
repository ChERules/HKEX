# HKEX

__The Project:__
The program will download the daily quotation web pages which is made available
by Hong Kong Stock Exchange to the pubic via its website. Then the daily
summary of each listing will be extracted and be stored in a CSV (comma separated
value) file.

There is another project ex2db project which will do the same task but the data
will be stored in a SQL Lite database. (Coming soon)

1. Download the daily quotation webpage.
2. Extract summary of the day's performance of all stocks traded on the day and
   stored them in a CSV file.
3. Collect the data of any particular company of interest into a separate CSV
   file.

__The scripts:__
hkex.py is the main script that will control the download and data extraction.  
myfunctions.py contains all functions for the project.  

__Future work:__
No plan for the project at present time.

Remarks:
__2021-05-09__
Decided to make the storing data in SQL database development of the project into
a different project "ex2db" which should appear shortly.  myfunctions.py has
been cleaned up to retain only the functions required for this project.  The
code for this project will be frozen for now except for bug fixes.  I will
work on the ex2db project for now.

Keeping hkex as is instead of moving it to a SQL database project, I imagine
the value of CSV files especially for the ease of reading it into other tools or
by other program.

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
