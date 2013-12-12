from models import *


def sample_data():
    okanagan = 'Canada - British Columbia: Okanagan Valley'
    v = Vintner()
    v_key = v.create({'name': 'Hillside Estate',
                      'location': okanagan})

    w = Wine(parent=v_key)
    w.create({'name': 'Mosaic',
              'varietal': 'Blend',
              'winetype': 'Red',
              'year': '2008',
              'alcohol': '13.8%',
              'upc': '626990028932'}, v)

    w = Wine(parent=v_key)
    w.create({'name': 'Merlot',
              'varietal': 'Merlot',
              'year': '2009',
              'winetype': 'Red',
              'alcohol': '13.8%',
              'upc': '628694536836'}, v)

    w = Wine(parent=v_key)
    w.create({'name': 'Cabernet Franc',
              'varietal': 'Cabernet Franc',
              'year': '2009',
              'winetype': 'Red',
              'alcohol': '13.5%',
              'upc': '626990019237'}, v)

    v = Vintner()
    v_key = v.create({'name': 'Hester Creek',
                      'location': okanagan,
                      'website': 'http://www.hestercreek.com'})

    w = Wine(parent=v_key)
    w.create({'name': 'Character',
              'varietal': 'Blend',
              'year': '2011',
              'winetype': 'Red',
              'alcohol': '13.5%',
              'upc': '626990112228',
              'blend': "['Merlot', 'Syrah', 'Malbec', 'Petit Verdot']"}, v)

    w = Wine(parent=v_key)
    w.create({'name': 'Trebbiano',
              'varietal': 'Trebbiano',
              'year': '2012',
              'alcohol': '13.8%',
              'upc': '626990125341'}, v)



