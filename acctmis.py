# Module containing code for ACCTMIS7810 course
# Contains utitilty routines for reading from websites
# Pre-requisites - the modules bs4 and mechanicalsoup must be installed on your computer.
#
# Author: David Trimm
# Date: Sept 22 2019 (first full commit on github)
#
# Import using the following "from acctmis import *"
#
################### Functions In This Module ###########################################
#
# get_web_page(url): Open up a web page found at a url, return the "soup" of that page
# get_all_links(soup): Return all the links on a web page's "soup"
# get_first_link_matching(soup, match): return the first link on a web page's "soup" that matches a string
# get_all_links_matching(soup, match): return all links in soup which match a string
# get_all_image_urls(soup): Return the full URLs of every image on a page
# download_image(img_url): Download an image at a url to a local file in the current directory 
# get_all_text(soup): Get all text that is on a web-page
# get_text_file_at_url(url): If the url is a text file (not html), then return that text as a string
# get_table(soup): Return the first table in "soup" as a list of lists (array).
# get_all_tables(soup): Return a list of all of the tables in "soup". Each table is represented as a list of lists (array).
# get_api_data(api): Return the data at an API endpoint (typically as a dictionary)"""
# distance(lat1, lon1, lat2, lon2): Calculate distance in km between two lat/long coordinates

import os
from bs4 import BeautifulSoup
import mechanicalsoup as ms
import requests
from math import sin, cos, sqrt, atan2, radians



# Global Variables
__browser__ = None



#################################################################


# get just the name of a file (e.g. an image) from a url and return it as a string,
# removing any extra bits we don't want like #,% and =
def get_name(s):
    l = s.split('/')
    n = len(l)
    while n > 0 and l[n-1]=='':
        n -= 1
    return l[n-1].replace("?","").replace("#","").replace(".html","").replace("=","").replace("%","")

# tidy up text by removing extraneous markers (tabs and carriage returns)
def __tidy(s):
    return s.replace('\n','').replace('\t','')

#################################################################


def create_a_browser(parser='html5lib'):
	""" create a browser object, and store it in the global variable __browser___
as well as returning it to the caller"""
	__browser__ = ms.StatefulBrowser(soup_config={'features': 'html5lib'})
	return __browser__



#################################################################


def get_browser():
    """Return the global browser object to the caller. If the browser
hadn't yet been created, then create it first, with the default 'html5lib' parser."""
    global __browser__
    if not __browser__:
        __browser__ = create_a_browser()
    return __browser__




#################################################################
# access a web page found at the address given by url
# return the soup or None if there is an error
# the error message will be printed out if there is a problem
def get_web_page(url):
    """Open and read the web page at the url given, and return the result as 'soup'."""
    br = get_browser()
    result = br.open(url)
    if result.status_code != 200:
        print("get_web_page: Error {} reading the webpage at {}".format(result, url))
        return None
    soup = br.get_current_page()
    return soup




#################################################################


def get_all_links(soup):
    """Return all the links which are in a web-page's "soup",
return it as a list (which will be an empty list if no links are found)"""
    br = get_browser()
    links = list(map(lambda x: x.get('href'), soup.find_all('a')))
    if not links:
        links = [] # make it an empty list, rather than "None"
    if None in links:
        links.remove(None) # remove any "erroneous" None entries in the list
    links = list(map(lambda x: br.absolute_url(x), links))
    return links



#################################################################


def get_first_link_matching(soup, match):
    """Return the first link (url) in the soup which matches the 'match' parameter"""
    link_list = get_all_links(soup)
    for link in link_list:
        if match in link:
            return link



#################################################################


def get_all_links_matching(soup, match):
    """Return all links (URLs) in the soup which matche the 'match' parameter"""
    link_list = get_all_links(soup)
    return_list = []
    for link in link_list:
        if match in link:
            return_list.append(link)
    return return_list
    

#################################################################

def get_all_image_urls(soup):
    """Return the addresses (urls) of all the images in the soup, return as a list
which can be empty if no images are found"""
    img_list = []
    br = get_browser()

    # the lambda function takes each relative url and converts to an absolute
    # so that the values returned in the list of images are each
    # full URLs which can be accessed independently.
    for img in soup.find_all('img'):
        img_list.append(br.absolute_url(img.get('src')))
                    
    return img_list


#################################################################

def download_image(img_url):
    """Download an image from a url, saving it in a file
with the same name in the current directory on the loacl machine. If successful, then
True will be returned, otherwise False, and an error message will be printed."""
    try:
        i = requests.get(img_url).content
        img_file = get_name(img_url)
        with open(img_file,'wb') as f:
            f.write(i)
        return True
    except:
        print("An error occured trying to read (or write locally) {}".format(img_url))
        return False
    return True




#################################################################


def get_all_text(soup):
    """Return all the text in the web page's soup. None is returned if there isn't any"""
    return soup.get_text()




#################################################################


def get_text_file_at_url(url):
    """Read in a text file from the internet (stored at "url")
and return the text as a string. If url isn't successfully
opened, then return None and issue a printed error message"""
    response = requests.get(url)
    if response.status_code != 200:
        print("get_text_file_at_url: Error {} reading file at {}".format(response.status_code, url))
        return None
    return response.text
    
    


#################################################################

    
def __get_table_data(table_soup, verbose=False):
    rows = table_soup.find_all('tr')
    if verbose:
        print("{} Rows".format(len(rows)))
    new_table = []
    for row in rows:
        new_row = []
        cols = row.find_all('td')
        if len(cols) == 0: # if there are no td tags, maybe there's a 'th'
            cols = row.find_all('th')
            
        if verbose:
            print("{} columns".format(len(cols)))
            
        for col in cols:
            new_col = []
            text = col.get_text()
            if text != None: 
                text = __tidy(text)
            #img = col.get('img')
            #link = col.get('a')
            # build the table row here
            new_col = text
            new_row.append(new_col)
        new_table.append(new_row)
    return new_table



#################################################################


def get_table(soup):
    """Gets all the entries in the table (links, images, text),
returning it as a list of lists (array)"""
    table = soup.find('table')
    if not table: # no table found
        print("get_table: no table found in soup.")
        return []
    return __get_table_data(table)
    


#################################################################

def get_all_tables(soup):
    """Gets all the entries in all the tables in soup (links, images, text),
returns as a list of lists (array)"""
    tables = soup.find_all('table')

    if not tables: # no table found
        print("get_all_tables: no table found in soup.")
        return []

    table_list = []
                    
    for table in tables:
        table_list.append(__get_table_data(table))

    return table_list



def get_api_data(api):
    """Gets the data at an API endpoint and returns it (typically as a dictionary)"""

    result = requests.get(api)
    if result.status_code != 200:
        print("get_api_data: Error {} reading data at {}".format(result.status_code, api))
        return None
    return result.json()


 
                    
#####################################################################

# Calculate the distance between two points on the surface of the earth
# given by lat,long coordinates.
def distance(lat1, lon1, lat2, lon2):
    """Calculate the approximate distance between two lat/lon coordinates on
the surface of the earth. Both lat and long inputs must be convertable to
'float' data and the result is returned as a float number"""
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    dist = R * c
    return dist





