import httplib
import urllib
import json
import random
from datetime import date
from copy import copy
import time


import random_name
import wine_types

prelude = "/truth"

count = {
    'winery': 5,
    'wine': 25,
    'cellar': 2,
    'winebottles': 45,
    'userwine': 12,
    'tastings': 20
}

users = {  # Actually a Header object.
    '113317414025130442177':
        {"Cookie": 'dev_appserver_login="alice@winebits.com:False:113317414025130442177"; Path='},
    '115169173179252616778':
        {"Cookie": 'dev_appserver_login="bob@winebits.com:False:115169173179252616778"; Path='},
    '125911331821051851470':
        {"Cookie": 'dev_appserver_login="charlie@winebits.com:False:125911331821051851470"; Path=/'}
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

    wineries = load_wineries(connection, count['winery'])
    wines = load_wines(connection, wineries, count['wine'])
    cellar = load_cellar(connection, count['cellar'])
    load_wine_bottle(connection, cellar, wines, count['winebottles'])
    userwines = load_user_wines(connection, wines, count['userwine'])
    load_tastings(connection, userwines, count['tastings'])


def get_random_name():
    return random_name.adjective().capitalize() + " " + random_name.noun().capitalize()


def get_random_date(past=True):
    if past:
        year = random.randint(1990, date.today().year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        if year == date.today().year:
            month = random.randint(1, date.today().month)
            if month == date.today().month:
                day = random.randint(1, date.today().day)
    else:
        year = random.randint(date.today().year, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        if year == date.today().year:
            month = random.randint(date.today().month, 12)
            if month == date.today().month:
                day = random.randint(date.today().day, 28)

    return str(year) + "/" + str(month) + "/" + str(day)


def create_random_winery(connection):
    data = {
        'name': get_random_name(),
        'location': "San Randomino, The Magical Country Where Test Data Lives"
    }
    return POST(connection, "/winery", data)


def create_random_wine(connection, winery_id):
    data = {
        'name': get_random_name(),
        'year': random_name.year(),
        'winetype': random.choice(wine_types.types),
        'varietal': random.choice(wine_types.varietals).encode("ascii", "ignore")
    }
    wine = POST(connection, "/winery/%d/wine" % winery_id, data)
    wine['winery_id'] = winery_id
    return wine


def create_random_cellar(connection, user):
    data = {
        'name': get_random_name()
    }
    cellar = POST(connection, "/cellar", data, user)
    cellar['user'] = user
    return cellar


def create_random_winebottle(connection, user, cellar_id, winery_id, wine_id):
    data = {
        'winery_id': winery_id,
        'wine_id': wine_id,
        'bottle_size': "750ml",
        'storage_location1': random.choice(["cellar", "box", "shelves"]),
        'storage_location2': "rack " + str(random.randint(0, 5)) + " row " + str(random.randint(0, 5)),
        'purchase_date': get_random_date(past=True),
        'purchase_location': random.choice(["winery", "store"]),
        'cost': random.randint(5, 100) + random.randint(0, 99) / 100
    }
    if random.choice([True, False]):
        data['consumed'] = "true"
        data['consumed_date'] = get_random_date(past=True)
    else:
        data['consumed'] = "false"
    winebottle = POST(connection, "/cellar/%d/wine/" % cellar_id, data, user)
    winebottle['cellar_id'] = cellar_id
    winebottle['user'] = user
    return winebottle


def create_random_userwine(connection, user, winery_id, wine_id):
    data = {
        'drink_after': get_random_date(past=False),
        'drink_before': get_random_date(past=False),
        'tags': json.dumps([random_name.adjective() for x in range(0, 4)])
    }
    userwine = POST(connection, "/winery/%d/wine/%d/userwine" % (winery_id, wine_id), data, user)
    userwine['user'] = user
    return userwine


def create_random_tasting(connection, user, winery_id, wine_id, userwine_id):
    data = {
        'consumption_type': random.choice(['tasting', 'bottle']),
        'consumption_location': random.choice(['home', 'winery', 'restaurant']),
        'date': get_random_date(past=True),
        'rating': random.randint(50, 99),
        'flawed': 'false',
        'note': random_name.adjective()
    }
    tasting = POST(connection,
                   "/winery/%d/wine/%d/userwine/%d/tasting" % (winery_id, wine_id, userwine_id), data)
    tasting['user'] = user
    return tasting


def load_wineries(connection, count):
    wineries = GET(connection, "/winery")
    for i in range(len(wineries), count):
        wineries.append(create_random_winery(connection))
    return wineries


def load_wines(connection, wineries, count):
    wines = []
    for winery in wineries:
        winery_wines = GET(connection, "/winery/" + str(winery["id"]) + "/wine")
        for wine in winery_wines:
            wine['winery_id'] = winery['id']
        wines.extend(winery_wines)

    for i in range(len(wines), count):
        wines.append(create_random_wine(connection, wineries[random.randint(0, len(wineries) - 1)]["id"]))

    return wines


def load_cellar(connection, count):
    cellars = []
    available_users = []
    for key in users:
        user = users[key]
        cellar = GET(connection, "/cellar", user)
        if len(cellar) > 0:
            cellar['user'] = user
            cellars.append(cellar)
        else:
            available_users.append(user)

    time.sleep(2)  # neccisary so that the cache updates and we don't create duplicate users

    for i in range(len(cellars), count):
        user = random.choice(available_users)
        available_users.remove(user)
        cellars.append(create_random_cellar(connection, user))
    return cellars


def load_wine_bottle(connection, cellars, wines, count):
    winebottles = []
    for cellar in cellars:
        winebottles.extend(GET(connection, "/cellar/" + str(cellar["id"]) + "/wine", cellar['user']))

    for i in range(len(winebottles), count):
        wine = random.choice(wines)
        cellar = random.choice(cellars)
        winebottles.append(
            create_random_winebottle(connection, cellar['user'], cellar['id'], wine['winery_id'], wine['id']))

    return winebottles


def load_user_wines(connection, wines, count):

    user_map_data = GET(connection, "/debug/usermap")
    user_map = {}
    for user in user_map_data:
        user_map[user["id"]] = users[user["guser"]]

    existinguserwines = []
    for wine in wines:
        new_userwines = GET(connection,
                            "/winery/" + str(wine["winery_id"]) + "/wine/" + str(wine["id"]) + "/userwine")
        for new_userwine in new_userwines:
            new_userwine["winery_id"] = wine["winery_id"]
            new_userwine["wine_id"] = wine["id"]
            new_userwine['user'] = user_map[new_userwine['user']]
        existinguserwines.extend(new_userwines)

    available_wines = copy(wines)
    userwines = []

    for i in range(len(existinguserwines), count):
        wine = random.choice(available_wines)
        available_wines.remove(wine)
        user = random.choice(users.values())
        new_userwine = create_random_userwine(connection, user, wine["winery_id"], wine["id"])
        new_userwine["winery_id"] = wine["winery_id"]
        new_userwine["wine_id"] = wine["id"]
        new_userwine['user'] = user
        userwines.append(new_userwine)

    userwines.extend(existinguserwines)

    return userwines


def load_tastings(connection, userwines, count):
    tastings = []
    for userwine in userwines:
        tastings.extend(
            GET(connection,
                "/winery/%d/wine/%d/userwine/%d/tasting" % (userwine["winery_id"],
                                                            userwine["wine_id"],
                                                            userwine["id"]),
                userwine['user']))

    for i in range(len(tastings), count):
        userwine = random.choice(userwines)
        tastings.append(
            create_random_tasting(connection,
                                  userwine['user'],
                                  userwine["winery_id"],
                                  userwine["wine_id"],
                                  userwine["id"]))


def GET(connection, url, user={}):
    url = prelude + url
    print "Get: ", url,
    connection.request("GET", url, None, user)
    response = connection.getresponse()
    print "\t", response.status
    resp = response.read()
    if response.status != 200:
        print resp
        raise Exception("Status: " + str(response.status))
    else:
        return json.loads(resp)


def POST(connection, url, params={}, user={}):
    url = prelude + url
    print "POST: ", url,
    params = urllib.urlencode(params)
    connection.request("POST", url, params, user)
    response = connection.getresponse()
    print "\t", response.status
    resp = response.read()
    if response.status != 200:
        print "params: " + str(params)
        print resp
        raise Exception("Status: " + str(response.status))
    else:
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
