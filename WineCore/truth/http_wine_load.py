import httplib
import urllib
import json
import random
from datetime import date

import random_name
import wine_types

prelude = "/truth"

count = {
    'winery':3,
    'wine':15,
    'cellar':2,
    'winebottles':25,
    'userwine':12
}


def main():
    import sys

    if not len(sys.argv) > 1 or not sys.argv[1].startswith("http"):
        print """please provide URL arguments: 
            1. the host to post sample data to (i.e. http://localhost:8000)"""
        quit()

    host = striphost(sys.argv[1])

    print "Connecting to host: ", host
    connection = httplib.HTTPConnection(host)

    wineries = loadWineries(connection, count['winery'])
    wines = loadWines(connection, wineries,count['wine'])
    cellar = loadCellar(connection, count['cellar'])
    loadWineBottle(connection,cellar,wines,count['winebottles'])
    #loadUserWines(connection, wines,count['userwine'])



def get_random_name():
    return random_name.adjective().capitalize() + " " + random_name.noun().capitalize()

def get_random_date(past=True):
    if past:
        year = random.randint(1990,date.today().year)
        month = random.randint(1,12)
        day = random.randint(1,28)
        if year == date.today().year:
            month = random.randint(1,date.today().month)
            if month == date.today().month:
                day = random.randint(1,date.today().day)
    else:
        year = random.randint(date.today().year,2025)
        month = random.randint(1,12)
        day = random.randint(1,28)
        if year == date.today().year:
            month = random.randint(date.today().month,12)
            if month == date.today().month:
                day = random.randint(date.today().day,28)

    return str(year) + "/" + str(month) + "/" + str(day)

def create_random_winery(connection):
    data = {
            'name':get_random_name(), 
            'location':"San Randomino, The Magical Country Where Test Data Lives"
        }
    return POST(connection, "/winery", data)


def create_random_wine(connection, winery_id):
    data = {
        'name':get_random_name(), 
        'year':random_name.year(),
        'winetype':random.choice(wine_types.types), 
        'varietal':random.choice(wine_types.varietals).encode("ascii", "ignore")
    }
    wine = POST(connection, "/winery/%d/wine" % winery_id, data)
    wine['winery_id'] = winery_id
    return wine


def create_random_userwine(connection, winery_id, wine_id):
    data = {
        'drink_after':get_random_date(past=False),
        'drink_before':get_random_date(past=False),
        'tags':json.dumps([random_name.adjective() for x in range(0,4)])
    }
    return POST(connection, "/winery/%d/wine/%d/userwine" % (winery_id,wine_id), data)

def create_random_cellar(connection):
    data = {
        'name':get_random_name()
    }
    return POST(connection, "/cellar",data)

def create_random_winebottle(connection, cellar_id, winery_id, wine_id):
    data = {
        'winery_id':winery_id,
        'wine_id':wine_id,
        'bottleSize':"750ml",
        'storage_location1':random.choice(["cellar","box","shelves"]),
        'storage_location2':"rack " + str(random.randint(0,5)) + " row " + str(random.randint(0,5)),
        'purchase_date':get_random_date(past=True),
        'purchase_location':random.choice(["winery","store"]),
        'cost':random.randint(5,100) + random.randint(0,99)/100
    }
    if random.choice([True,False]):
        data['consumed']="true"
        data['consumed_date'] = get_random_date(past=True)
    else:
        data['consumed']="false"
    winebottle = POST(connection, "/cellar/%d/wine/" % cellar_id, data)
    winebottle['cellar_id'] = cellar_id
    return winebottle

def loadWineries(connection,count):
    wineries = GET(connection, "/winery")
    for i in range(len(wineries), count):
        wineries.append(create_random_winery(connection))
    return wineries

def loadWines(connection,wineries,count):
    wines = []
    for winery in wineries:
        wineryWines = GET(connection,"/winery/"+str(winery["id"])+"/wine")
        for wine in wineryWines:
            wine['winery_id'] = winery['id']
        wines.extend(wineryWines)

    for i in range(len(wines),count):
        wines.append(create_random_wine(connection,wineries[random.randint(0,len(wineries)-1)]["id"]))

    return wines

def loadCellar(connection,count):
    cellar = GET(connection, "/cellar")
    for i in range(len(cellar), count):
        cellar.append(create_random_cellar(connection))
    return cellar

def loadWineBottle(connection,cellars,wines,count):
    winebottles = []
    for cellar in cellars:
        winebottles.extend(GET(connection,"/cellar/"+str(cellar["id"])+"/wine"))

    for i in range(len(winebottles),count):
        wine = random.choice(wines)
        winebottles.append(create_random_winebottle(connection,random.choice(cellars)['id'],wine['winery_id'],wine['id']))

    return winebottles

def GET(connection, url):
    url = prelude+url
    print "Get: ", url 
    connection.request("GET", url)
    response = connection.getresponse()
    print "\t", response.status
    resp = response.read()
    if response.status != 200: 
        print "\t", resp
    return json.loads(resp)    

def POST(connection, url, params={}):
    url = prelude+url
    print "POST: ", url 
    params = urllib.urlencode(params)
    connection.request("POST", url, params)
    response = connection.getresponse()
    print "\t", response.status
    resp = response.read()
    if response.status != 200:
        print "params: " + str(params)
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
