
### Location ###
#### fields ####
- location: "Canada - British Columbia: Okanagan Valley"  
 
#### urls ####
- list: GET /truth/location

### WineType ###
#### fields ####
- winetype: "White"   
 
#### urls ####
- list: GET /truth/winetype

#### Varietal ###
#### fields ####
- varietal: "Riesling"  
 
#### urls ####
- list: GET /truth/varietal

### Winery ###
#### fields ####
- id: 5768037999312896 
- url: "/winery/5768037999312896" 
- name: "8th Generation Vineyard" 
- location_fuzzy: null 
- location: "Canada - British Columbia: Okanagan Valley" 
- country: "Canada" 
- region: "British Columbia" 
- subregion: "Okanagan Valley"
- Appellation: "VQA"
- latitude: 49.5745629
- longitude: -119.6296763
- verified: false 
- verified_by: null 
- json: { wineryURL: "www.8thgeneration.com", cellarTrackerID:52020 } 
- rank: 544

#### urls ####
- list:   GET /truth/winery
- create: POST /truth/winery
- read:   GET /truth/winery/_winery-id_
- update: POST /truth/winery/_winery-id_
 
#### notes ####
cellarTrackerID gets you https://www.cellartracker.com/producer.asp?iProducer=<cellarTrackerID>

### Wine ###
parent: Winery
#### fields ####
- id: 5665783417929728 
- url: "/winery/6123180255084544/wine/5665783417929728" 
- name: "Selection"
- vintage: 2011 
- varietal: "Riesling"
- winetype: "White" 
- sweetness: 1  //from: ['00', '0', 1-30]
- verified_by: null 
- verified: false 
- upc: 626990124900 
- json: {wineURL:..., cellarTrackerID:1391458 }

#### urls ####
- list:   GET /truth/winery/_winery-id_/wine
- create: POST /truth/winery/_winery-id_/wine
- read:   GET /truth/winery/_winery-id_/wine/_wine-id_ 
- update: POST /truth/winery/_winery-id_/wine/_wine-id_ 

#### notes ####
cellarTrackerID gets you https://www.cellartracker.com/wine.asp?iWine=<cellarTrackerID>
display name: <varietal> <winery name> <varietal> <name>
 
### UserWine ###
parent: Wine
#### fields ###
- user: 123456890123456
- drink_after: 2013/10/1
- drink_before: 2015/10/1
- tags: ["cheap","Special Occasion"]

#### urls ####
- create: POST /truth/winery/_winery-id_/wine/_wine-id_/userwine
- read:   GET /truth/winery/_winery-id_/wine/_wine-id_/userwine/_userwine-id_
- update: POST /truth/winery/_winery-id_/wine/_wine-id_/userwine/_userwine-id_
- delete: DELETE /truth/winery/_winery-id_/wine/_wine-id_/userwine/_userwine-id_

### WineCellar ###
#### fields ####
- id: 1234567890123456
- url: cellar/1234567890123456
- name: "My House"

#### urls ####
- create: POST /truth/cellar
- read:   GET /truth/cellar/_cellar-id_
- update: POST /truth/cellar/_cellar-id_
- delete: DELETE /truth/cellar/_cellar-id_

#### notes ####
Cellars are required to solve the multiple people using one cellar problem.
For example, Aimee and I share a cellar, but not a Google account, so we both 
need permission to log in and add / remove / drink bottles.

### CellarPermission ###
Parent: cellar
#### fields ####
- id: 1234567890123456
- user: 1234567890123456
- permission: 'owner' //from: ['read', 'write', 'owner']

#### urls ####
- list:   GET /truth/cellar/_cellar-id_/permission
- create: POST /truth/cellar/_cellar-id_/permission
- delete: DELETE /truth/cellar/_cellar-id_/permission/_permission-id_

### WineBottle ###
Parent: cellar
#### fields ####
- id: 5665783417929728
- wine_key: 1234567890123456
- bottleSize: "750ml"
- storage_location1: "cellar"
- storage_location2: "Rack 5 row 2"
- purchase_date: 2012/10/1
- delivery_date: null
- purcahse_location: 'winery'
- cost: $18
- consumed: false 
- consumed_date: null
- json: {}

#### urls ####
- list:   GET /truth/cellar/_cellar-id_/wine 
- create: POST /truth/cellar/_cellar-id_/wine
- read:   GET /truth/cellar/_cellar-id_/wine/_winebottle-id_
- update: POST /truth/cellar/_cellar-id_/wine/_winebottle-id_
- delete: DELETE /truth/cellar/_cellar-id_/wine/_winebottle-id_

#### notes ####
bottleSizes: [750ml, 1.5L, 375ml, 500ml, 50ml, 100ml, 187ml, 200ml, 250ml, 300ml, 330ml, 620ml, 700ml, 1.0L, 1.75L, 3.0L, 3.78L, 4.0L, 5.0L, 6.0L, 9.0L, 12.0L, 15.0L, 16.0L, 18.0L, 27.0L, 1.125L, 2.5L]

### WineTasting ###
Parent: UserWine
#### fields ####
- id: 1234567890123456
- consumption_type: 'tasting' //from:['fromMyCellar','tasting',...]
- consumption_location: 'winery' //from: ['home', 'winery', 'restaurant']
- consumption_locationName: null //name if at restaurant
- date: 2013/8/25
- rating: 92
- flawed: false
- note: "less sweet than the normal Riesling"

#### urls ####
- list:   GET /truth/winery/_winery-id_/wine/_wine-id_/tasting
- list:   GET /truth/winery/_winery-id_/wine/_wine-id_/tasting/_user-id_  //all for a particular user
- create: POST /truth/winery/_winery-id_/wine/_wine-id_/tasting
- update: POST /truth/winery/_winery-id_/wine/_wine-id_/tasting/_tasting-id_
- delete: POST /truth/winery/_winery-id_/wine/_wine-id_/tasting/_tasting-id_

### User ###
#### fields ####
- id: 1234567890123456
- email: "bob.smith@email.com"
- nickname: "Bob Smith"

#### urls ####
- list:   GET /truth/user
- read:   GET /truth/user/_user-id_

### Event ###
#### fields ####
- id: 1234567890123456
- user: 1234567890123456
- action: "update"
- model: "Key('Winery', 5639274879778816, 'Wine', 5707702298738688)"
- model_type: "Wine"
- time: "2014/1/26 21:57pm PST"

### Search ###
GET /truth/search?s=_search-terms_ 



