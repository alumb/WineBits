import httplib
import urllib
import json

import random_name
import random
import wine_types


def main():
    import sys

    if not len(sys.argv) > 2 or not sys.argv[1].startswith("http"):
        print """please provide two arguments: 
            1. the host to post sample data to (i.e. http://localhost:8000) 
            2. the file containing sample data (i.e. data/wine_sample.json"""
        quit()

    host = striphost(sys.argv[1])
    datafile = sys.argv[2]

    print "Connecting to host: ", host
    connection = httplib.HTTPConnection(host)

    print "With data file: ", datafile
    try:
        json_data = json.loads(open(datafile).read())
    except IOError:
        json_data = None

    if json_data:
        for key, value in json_data.iteritems():
            location = key
            print location
            for k, v in value.iteritems():
                winery = k
                print "\t", winery
                winery_url = create_winery(connection, winery, location)
                for wine in v:
                    post_wine(connection, winery_url, wine) 
                    for winekey, winevalue in wine.iteritems():
                        print "\t\t", winekey, ":", winevalue
                    print "\t\t-------------"
    else: 
        print "Data file not found: Generating random wine."
        winery_url = create_random_winery(connection)
        for i in range(0,4):
            create_random_wine(connection, winery_url)

def create_random_winery(connection):
    location = "San Randomino, The Magical Country Where Test Data Lives"
    name = ("Winery " + random_name.adjective().capitalize() + " " 
            + random_name.noun().capitalize())
    return create_winery(connection, name, location)


def create_random_wine(connection, winery_url):
    name = (random_name.adjective().capitalize() + " " + 
            random_name.adjective().capitalize())
    year = random_name.year()
    winetype = random.choice(wine_types.types)
    varietal = random.choice(wine_types.varietals)
    post = {
        'name':name, 
        'year':year,
        'winetype':winetype, 
        'varietal':varietal
    }
    return post_wine(connection, winery_url, post)


def create_winery(connection, name, location):
    """
    returns winery URL
    """
    post_data = {
        'name':name, 
        'location':location
    }
    return post_winery(connection, post_data)['url']


def post_winery(connection, post_this={}):
    return post(connection, "/winery", post_this)


def post_wine(connection, winery_url, post_this={}):
    return post(connection, winery_url+"/wine", post_this)


def post(connection, url, params={}):
    print "POST: ", url 
    params = urllib.urlencode(params)
    connection.request("POST", url, params)
    response = connection.getresponse()
    print "\t", response.status
    resp = response.read()
    print "\t", resp
    return json.loads(resp)


def striphost(host):
    """

    >>> striphost("http://www.google.com")
    'www.google.com'
    >>> striphost("https://butts.org")
    'butts.org'
    >>> striphost("nope")
    'nope'

    """
    if host.startswith("http://"):
        return host[7:]
    elif host.startswith("https://"):
        return host[8:]
    else:
        return host

if __name__ == '__main__':
    main()
