## WineTruth ##

WineTruth is a searchable database of Wines and Wineries. It is only concerned
with objective truth about wine - for example, 
"Black Hills Estate has a 2009 Carmenere" is a WineTruth. 
"I give the Black Hills Estate Carmenere 3 out of 5 stars" is not a WineTruth.

You may need to run `make install` before debugging WineTruth. 

The Trello page for WineTruth is here: https://trello.com/b/23aeKf5N/winetruth

### WineTruth API ###

The WineTruth API always returns `application-json` if successful, and an
error code if unsuccessful. 

#### POST /truth/winery ####

Create a winery. 

    name: Black Hills Estates
    location: Canada - British Columbia: Okanagan Valley

Returns the JSON object that is created:

    {
      "key": 5768037999312896, 
      "id": 5768037999312896, 
      "region": "British Columbia", 
      "name": "Black Hills Estate", 
      "json": {}, 
      "location": "Canada - British Columbia: Okanagan Valley", 
      "rank": 544, 
      "verified_by": null, 
      "location_fuzzy": null, 
      "country": "Canada", 
      "verified": false, 
      "url": "/winery/5768037999312896", 
      "subregion": "Okanagan Valley"
    }

##### name #####

The 'name' field is mandatory.

##### location #####

The 'location' field is optional. You may use any location that you like, 
however, if you would like to be able to search by country, region, or 
subregion, you must use one of the locations provided by `/truth/location`

##### Any other fields #####

It is possible to store any key-value pair you please against the winery. 


#### GET /truth/location ####

Returns a list of locations that the system of aware of. 

#### GET /truth/winery ####

A search interface for getting wineries using NDB's fast index searching
rather than Google's still-fast-but-more-limited document search searching.

Still needs some work, but it's possible to search for wineries by `country`, 
`region`, `subregion`, `name`, `location`, `verified`, `verified_by`, 
and `location_fuzzy`.

For example: 

    GET /truth/winery?country=Canada

would produce: 

    [
      {
        "key": 5768037999312896, 
        "name": "Black Hills Estate", 
        "location": "Canada - British Columbia: Okanagan Valley", 
        "id": 5768037999312896, 
        "verified": false, 
        "url": "/winery/5768037999312896"
      }, 
      ...
    ]
    

or:

    GET /truth/winery?verified=True

or:

    GET /truth/winery?region=British Columbia

Data returned by the query will never include the field searched on - 
wineries returned by the country=Canada query won't contain a country field, 
for example. 

Compound queries do not work yet, and for now would require that you use the
Search interface.  This would fail:

    GET /truth/winery?country=Canada&verified=True

#### GET /truth/winery/_winery-id_ ####

Returns data about the winery. 

    {
      "key": 5768037999312896, 
      "id": 5768037999312896, 
      "region": "British Columbia", 
      "name": "Black Hills Estate", 
      "json": {}, 
      "location": "Canada - British Columbia: Okanagan Valley", 
      "rank": 544, 
      "verified_by": null, 
      "location_fuzzy": null, 
      "country": "Canada", 
      "verified": false, 
      "url": "/winery/5768037999312896", 
      "subregion": "Okanagan Valley"
    }

#### POST /truth/winery/_winery-id_ ####

Add data about this winery. 

    awesomeness: high

You cannot change existing data about the winery, this will throw a 401 and
poop itself to death. The only exception is if you pass a Winery Private Token
with the request, which gives you access to alter data about the Winery.

Each Winery has its own Private Token. 


#### GET /truth/winery/_winery-id_/wine ####

Returns a list of every wine produced by the winery. 

    GET /truth/winery/6123180255084544/wine 
    [
      {
        "upc": null, 
        "name": null, 
        "url": "/winery/6123180255084544/wine/5665783417929728", 
        "winetype": "Red", 
        "json": {}, 
        "verified_by": null, 
        "id": 5665783417929728, 
        "verified": false, 
        "year": 2009, 
        "varietal": "Cabernet Sauvignon"
      }, 
      {
        "upc": null, 
        "name": "Le Grand Vin", 
        "url": "/winery/6123180255084544/wine/6228733371351040", 
        "winetype": "Red", 
        "json": {}, 
        "verified_by": null, 
        "id": 6228733371351040, 
        "verified": false, 
        "year": 2006, 
        "varietal": "Blend"
      }, 
      ...
    ]

#### POST /truth/winery/_winery-id_/wine ####

Create a wine. 

    name: Le Grand Vin 
    winetype: Red
    upc: 123456789
    year: 2008
    varietal: Blend

You'll note that it's impossible to create a wine without first creating
a winery. This is intentional. 

##### name #####

Unlike in Winery, 'name' is not required for a wine. However, some combination
of winetype and ( year, varietal, or name ) is required.

##### winetype #####

Winetype is _mandatory_, and must be one of the winetypes provided by 
`/truth/winetype` - at the moment one of _Red_, _White_, _Rose_, _Blend_,
_Fruit/Vegetable Wine_, _Dessert Wine_, _Sparkling Red_, _Sparkling White_, 
_Sparkling Rose_, _Fortified Red_, _Fortified White_, or _Fortified Rose_. 

##### upc, year #####

UPC and year are not mandatory. 

##### varietal #####

Varietal is unrestricted, however, for the sake of searchability, we recommend
you choose from the varietals available at `/truth/varietal`

##### Any other fields #####

It is possible to store any key-value pair you please against the wine. 

#### GET /truth/winetype ####

Return a list of all valid wine types.

#### GET /truth/varietal ####

Return a list of all recommended varietals. This is hard-coded, rather than
calculated - if someone includes a wine with a varietal that we didn't think 
of, that varietal will _not_ appear on this list. 

#### GET /truth/winery/_winery-id_/wine/_wine-id_ ####

Return all of the data about this particular wine. 

    GET /truth/winery/5768037999312896/wine/5630599045840896
    {
      "upc": null, 
      "name": "Nota Bene", 
      "url": "/winery/5768037999312896/wine/5630599045840896", 
      "winetype": "Red", 
      "json": {}, 
      "verified_by": null, 
      "id": 5630599045840896, 
      "verified": false, 
      "year": 2004, 
      "varietal": "Blend"
    }

#### POST /truth/winery/_winery-id_/wine/_wine-id_ ####

Add data about this wine. 

    awesomeness: high

You cannot change existing data about the wine, this will throw a 401 and
poop itself to death. The only exception is if you pass a Winery Private Token
with the request, which gives you access to alter data about the Wine.

Each Winery has its own Private Token, which can be used to alter the data
of any Wine that has the Winery as its parent. 

#### GET /truth/search?s=_search-terms_ ####

Searches through all of the wines and wineries using a search term you provide.

Supports partial-text matching on winery name, winery location, wine name, 
and varietal. 

The query-string rules are here: https://developers.google.com/appengine/docs/python/search/query_strings

##### Fields #####

    winery:
        name
        partial_name 
        location
        partial_location
        country
        region
        subregion
        verified
        rank
        id

    wine:
        name
        partial_name
        winery
        partial_winery
        winetype
        varietal
        partial_varietal
        upc
        verified
        id
        winery_id
        rank

##### Results #####
    
The search results are sorted by 'rank', which is a magical guess at how
relevant the data is. 
  
Search results are divided into Wineries and Wines: 

    GET /truth/search?q=Ca
    {
      "wines": [
        {
          "name": "Cabernet Sauvignon Reserve", 
          "url": "/winery/5838406743490560/wine/6682831673622528", 
          "winery": "Mission Hill", 
          "id": 6682831673622528, 
          "verified": "False", 
          "year": 2007, 
          "winery_id": 5838406743490560, 
          "varietal": "Cabernet Sauvignon", 
          "rank": 390
        }, 
        ...
      ], 
      "wineries": [
        {
          "name": "Black Hills Estate", 
          "location": "Canada - British Columbia: Okanagan Valley", 
          "id": 5768037999312896, 
          "verified": "False", 
          "url": "/winery/5768037999312896", 
          "rank": 544
        }, 
        ...
      ]
    }

### San Randomino, The Magical Country Where Test Data Lives ###

This is a special country. Put test or random data in here. 

### WineTruth Makefile ###

#### `make install` ####

Install PIP dependencies for WineTruth. 

#### `make test` ####

Run all of the Doctests, using stub Google services defined in stubs.py

#### `make random_wine` ####

HTTP connect to localhost:8080 and create a random winery with 4 random wines.

#### `make sample_wine` ####

HTTP connect to localhost:8080 and load all of the wines in 
`data/wine_sample.json`

#### `make lint` ####

Have PEP8 tell us all of the many, many things we're doing wrong. 

#### `make todo` ####

Fish any "TODO"s out of the code. TODOs belong in Trello. 



