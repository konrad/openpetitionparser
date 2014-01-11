#!/usr/bin/env python
"""A openpetition.org data extraction tool

A parser for openpetition.org. Download file of a given petition
and parses the html file.

Usage:

$ python openpetitionparser.py download https://www.openpetition.de/petition/unterzeichner/a_petition 50

$ python openpetitionparser.py json

$ python openpetitionparser.py csv

Copyright (c) 2014, Konrad Foerstner <konrad@foerstner.org>
    
Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.
    
THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

"""

__description__ = "Downloads pages from openpetition.org and extracts data"
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2014 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = ""

import argparse
from collections import defaultdict
import json
import os
import urllib.request
import sys
from bs4 import BeautifulSoup

def main():
    args = get_args()
    args.func(args)

def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_subparsers = arg_parser.add_subparsers(help="commands")
    download_arg_parser = arg_subparsers.add_parser(
        "download", help="Download html files")
    download_arg_parser.add_argument(
        "url", help="The full URL of the petition.")
    download_arg_parser.add_argument(
        "number_of_pages", type=int, help="Number of pages to download")
    download_arg_parser.add_argument(
        "--output_folder", default="openpetition", help="Output folder. "
        "Default is 'openpetition'.")
    download_arg_parser.set_defaults(func=download_pages)
    json_arg_parser = arg_subparsers.add_parser(
        "json", help="Convert to JSON")
    json_arg_parser.add_argument(
        "--input_folder", default="openpetition", help="Input folder. "
        "Default is 'openpetition'.")
    json_arg_parser.add_argument(
        "--output_json", default="openpetition.json", help="Output file. "
        "Default is 'openpetition.json'.")
    json_arg_parser.set_defaults(func=parse_and_create_json)
    csv_arg_parser = arg_subparsers.add_parser(
        "csv", help="Convert JSON to CSV")
    csv_arg_parser.add_argument(
        "--input_json", default="openpetition.json", help="Input JSON file. "
        "Default is 'openpetition.json'.")
    csv_arg_parser.add_argument(
        "--output_csv", default="openpetition.csv", 
        help="Output CSV (tab seperated) file. "
        "Default is 'openpetition.json'.")
    csv_arg_parser.set_defaults(func=create_csv)
    args = arg_parser.parse_args()
    if "func" in dir(args):
        return args
    else:        
        arg_parser.print_help()
        sys.exit()

def download_pages(args):
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    for page_number in range(1, args.number_of_pages+1):
        page_url = "%s/?seite=%s" % (args.url, page_number)
        urllib.request.urlretrieve(page_url, "%s/page_%03d.html" % (
            args.output_folder, page_number))

def parse_and_create_json(args):
    locations_and_supporters = defaultdict(lambda: defaultdict(list))
    for html_file in sorted(os.listdir(args.input_folder)):
        _parse_file(
            "%s/%s" % (args.input_folder, html_file), locations_and_supporters)
    with open(args.output_json, "w") as output_fh:
        json.dump(locations_and_supporters, output_fh)
        
def _parse_file(html_file, locations_and_supporters):
    soup = BeautifulSoup(open(html_file, "rb").read())
    signerlist = soup.find("div", { "class" : "signerlist" })
    curr_country = None
    curr_city = None
    for span in signerlist.find_all("span"):
        try:
            if "country" in span["class"]:
                curr_country = _clean_location(span.text)
            elif "city" in span["class"]:
                curr_city = _clean_location(span.text)
            elif "signer" in span["class"]:
                locations_and_supporters[curr_country][curr_city].append(
                    span.text.strip())
        except KeyError:
            continue

def _clean_location(location):
    location = location.replace(",", "") 
    location = location.replace(":", "") 
    location = location.strip()
    return(location)
    
def create_csv(args):
    locations_and_supporters = json.load(open(args.input_json))
    with open(args.output_csv, "w") as output_file:
        output_file.write("\t".join(["#Country", "City", "Supporter"]) + "\n")
        for country in sorted(locations_and_supporters.keys()):
            for city in sorted(locations_and_supporters[country].keys()):
                for supporter in sorted(
                        locations_and_supporters[country][city]):
                    output_file.write(
                        "\t".join([country, city, supporter]) + "\n")
                    
if __name__ == "__main__": 
    main()
