This is a rather simplistic tool to extract data from openpetition.org.

It will help to dowload supporter list pages, parse them and store the
data for further analysis in JSON format.

Example:

$ python openpetitionparser.py download https://www.openpetition.de/petition/unterzeichner/my_test_peptition 94

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
