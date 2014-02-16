import random

adjectives = [
    'heroic',
    'magnificent',
    'mighty',
    'amazing',
    'wonderful',
    'fantastic',
    'incredible',
    'spectacular',
    'tremendous',
    'throbbing',
    'enormous',
    'aqua',
    'aquamarine',
    'azure',
    'beige',
    'black',
    'almond'
    'blue',
    'brown',
    'chartreuse',
    'coral',
    'cornflower',
    'crimson',
    'cyan',
    'navy',
    'goldenrod',
    'gray',
    'grey',
    'green',
    'khaki',
    'magenta',
    'olive',
    'salmon',
    'slate',
    'turquoise',
    'violet',
    'pink',
    'skyblue',
    'brick',
    'white',
    'fuchsia',
    'gainsboro',
    'golden',
    'honeydew',
    'hotpink',
    'indigo',
    'ivory',
    'lavender',
    'lemon',
    'chiffon',
    'purple',
    'orchid',
    'linen',
    'rose',
    'orange',
    'orangered',
    'pale',
    'powderblue',
    'sandy',
    'seashell',
    'silver',
    'burntsienna',
    'tan',
    'teal',
    'thistle',
    'violet',
    'plaid',
    'polkadot',
    'paisley',
    'iron',
    'bronze',
    'stone',
    'birch',
    'cedar',
    'cherrywood',
    'sandalwood',
    'pine',
    'fir',
    'yew',
    'hemlock',
    'spruce',
    'chestnut',
    'boxwood',
    'butternut',
    'camphor',
    'elm',
    'oak',
    'mahogany',
    'huckleberry',
    'ironwood',
    'maple',
    'poplar',
    'unpoplar',
    'teak',
    'beech',
    'nutmeg',
    'willow',
    'cinnamon',
    'allspice',
    'basil',
    'cardamom',
    'clove',
    'garlic',
    'juniper',
    'gin-soaked',
    'rum',
    'lime',
    'licorice',
    'capable',
    'trustworthy',
    'heavy',
    'fast',
    'slow',
    'charming',
    'noticeable',
    'sly',
    'slippery',
    'sluggish',
    'casual',
    'cautious',
    'cement',
    'diabolical',
    'evil',
    'metropolitan',
    'banana',
    'good',
    'neutral',
    'apple',
    'pear',
    'winter',
    'spring',
    'fall',
    'autumn',
    'summer',
    'garbage',
    'imposing',
    'correct',
    'underhanded',
    'salty',
    'coffee',
    'cheese',
    'floppy',
    'unpopular',
    'popular',
    'forgettable',
    'misty',
    'soulful',
    'gassy',
    'spectacular',
    'sleepy',
    'laudable',
    'comfortable',
    'soft',
    'dicey',
    'memorable',
    'patterned',
    'greasy',
    'elongated'
]

nouns = [
    'apparatus',
    'butt',
    'hunter',
    'fisher',
    'bean',
    'harvest',
    'mixer',
    'hand',
    'finger',
    'nose',
    'eye',
    'belly',
    'jeans',
    'plan',
    'disk',
    'horse',
    'battery',
    'staple',
    'face',
    'button',
    'byte',
    'cabinet',
    'vehicle',
    'canyon',
    'dance',
    'crayon',
    'sausage',
    'meat',
    'napkin',
    'device',
    'cape',
    'chair',
    'person',
    'character',
    'cheeseburger',
    'ham',
    'beef',
    'book',
    'circuit',
    'civilian',
    'clamp',
    'circuitry',
    'calculus',
    'cloud',
    'code',
    'coast',
    'coin',
    'corporation',
    'concern',
    'space',
    'key',
    'object',
    'heart',
    'stapler',
    'mug',
    'bottle',
    'cable',
    'note',
    'lamp',
    'shelf',
    'blanket',
    'dong',
    'captain',
    'board',
    'indicator',
    'injection',
    'investment',
    'issue',
    'job',
    'knife',
    'thing',
    'phone',
    'sweater',
    'pants',
    'boot',
    'sock',
    'socks',
    'hat',
    'ring',
    'dong',
    'wrap',
    'holder',
    'pen',
    'pencil',
    'bag',
    'dispenser'
]

years = [
    1991,
    1992,
    1993,
    1994,
    1995,
    1996,
    1997,
    1998,
    1999,
    2000,
    1970,
    1985,
    2015
]


def adjective():
    return random.choice(adjectives)


def noun():
    return random.choice(nouns)


def year():
    return random.choice(years)


def name():
    adj = "-".join([adjective() for x in range(0, 2)])
    noun_ = "".join([noun() for x in range(0, 2)])
    return adj + "-" + noun_
