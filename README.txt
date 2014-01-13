This is a rather simplistic tool to extract data from openpetition.org.

***You may not need this tool! After publishing this tool I was
contacted by openpetition.org. They are very happy to provide the data
in different formats.***

It will help to dowload supporter list pages, parse them and store the
data for further analysis in JSON format.

Example:

$ URL=https://www.openpetition.de/petition/unterzeichner/BLUBLUBLUB 
$ python openpetitionparser.py download $URL 94

This generates a folder called "openpetition" and downloads the pages
of the supporter list. Important - currently you have to give the
total number of pages you want to retrieve as a second positional
argument. You have to get the maximum number of pages from the
petition page.

Once the data is downloaded you can parse it and generate a JSON file.

$ python openpetitionparser.py json

This will parse the HTML files and create a single JSON file that
contain the supportor by country and city. It is just the starting
point e.g. for an correlation analysis.

If you just need a list you can use 

$ python openpetitionparser.py csv

to create a CSV (tab separated) based on the JSON file. This can be
loaded in common spreadsheet programs.

Be aware that the data is not very clean and often supporters enter
the data in a wrong way.
