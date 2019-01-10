#!/usr/bin/python

# arxiv2bib.py
#
# Script for taking a list of ArXiV numbers and producing a .bib file with
# .bib entries for each paper.
#
# Currently supported:
#    * Taking a directory with files of the form "1811.10581.pdf"
#         and spitting out a combined .bib file with @TECHREPORT
#         bib entries for each file.
#
# Idiosyncrasies
#    * ArXiV may decide you are a bot (you are) and so may block you. Try
#         not to run this on too large a directory.
#    * the output bibtex is utf-8 encoded, which may or may not play well
#         with accents etc. appearing in your bib.
#
# Future potential features
#    * Taking a list of ArXiV numbers in a .txt file
#    * Output formats other than @TECHREPORT
#    * Dealing better with accented characters
#
# USAGE:
#     python arxiv2bib.py [directory]  [output file]
#     python mergetex.py  /Users/foo/toread/  readinglist.bib
#
#
#
#
# v0.1 by Anand Sarwate (anand.sarwate@rutgers.edu)


import argparse
import string
import codecs
import re
import sys
import os.path
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from time import sleep
from random import random
import urllib2



# global constants
absurl = 'https://www.arxiv.org/abs/'




# input argument parser
#    args.format will contain filename for format file
#    args.bibfile will contain filename of bibliography
inparser = argparse.ArgumentParser(description='Parses argument list')
inparser.add_argument('directory', metavar='dir', help='target directory')
inparser.add_argument('output', metavar='output', help='desired target output file')
args = inparser.parse_args()


# STILL NEEDED: CATCH INPUT EXCEPTIONS



# grab list of files in directory in the right format
allfiles = [f for f in listdir(args.directory)
                if (isfile(join(args.directory, f))
                        and re.match('[0-9][0-9][0-9][0-9].[0-9][0-9][0-9][0-9].*.pdf',f)) ]
fout = codecs.open(args.output, 'w', 'utf-8')

for f in allfiles:

    # random delay
    sleep(5*random())
    
    # generate url for abstract info and open it
    recordurl = absurl + f[:-4]
    print 'Opening ' + recordurl
    paperinfo = urllib2.urlopen(recordurl)

    # parse out content from website
    soup = BeautifulSoup(paperinfo.read(), 'lxml')

    # get title
    title = soup.find("h1", {"class": "title mathjax"}).contents[1]

    # get authors
    authorlist = soup.find("div", {"class": "authors"}).find_all("a")
    alist = []
    for tag in authorlist:
        alist.append( tag.contents )
    authors = [item for sublist in alist for item in sublist]
        
    # get arxivid / number
    number = soup.find("span", {"class": "arxivid"}).find("a").contents[0]
    classification = soup.find("span", {"class": "arxivid"}).contents[2]
    arxivid = number + classification

    # get month
    # get year
    lastsub = soup.find("div", {"class": "submission-history"}).contents[-2]
    datepieces = lastsub.split(' ')
    month = datepieces[2].lower()
    year = datepieces[3]
    
    authglue = u' and '
    fout.write(u'@techreport{' + f[:-4] + u', \n')
    fout.write(u'\tTitle = {' + title + u'},\n')
    fout.write(u'\tAuthor = {' + authglue.join(authors) + u'},\n')
    fout.write(u'\tInstitution = {' + 'ArXiV' + u'},\n')
    fout.write(u'\tNumber = {' + arxivid + u'},\n')
    fout.write('\tMonth = ' + month + '}.\n')
    fout.write('\tYear = {' + year + '}.\n')
    fout.write(u'\tUrl = {' + recordurl + u'}\n')
    fout.write(u'}\n\n')




