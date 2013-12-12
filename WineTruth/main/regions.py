# coding=latin-1

#TODO: Fill in

region_map = {
    u"Argentina":[
        u"Mendoza",
        u"San Juan",
        u"Buenos Aires",
        u"Rio Negro",
        u"Neuquén",
        u"Salta",
        u"La Rioja",
        u"Catamarca"
    ],
    u"Bolivia":[
        u"Tarija"
    ],
    u"Brazil":[
        [u"Rio Grande do Sul", [
            u"Bento Gonçalves",
            u"Caxias do Sul",
            u"Garibaldi",
            u"Cotiporã"]],
        [u"Paraná", [
            u"Marialva",
            u"Maringá",
            u"Rosário do Avaí",
            u"Bandeirantes"]],
        [u"Santa Catarina", [
            u"São Joaquim",
            u"Pinheiro Preto",
            u"Tangará"]],
        [u"Mato Grosso", [
            u"Nova Mutum"]],
        [u"Minas Gerais", [
            u"Pirapora",
            u"Andradas",
            u"Caldas",
            u"Santa Rita de Caldas"]],
        [u"Bahia", [
            u"Juazeiro",
            u"Curaçá",
            u"Irecê"]],
        [u"Pernambuco", [
            u"Petrolina",
            u"Casa Nova",
            u"Santa Maria da Boa Vista"]],
        [u"São Paulo", [
            u"Jundiaí",
            u"São Roque"]]
    ],
    u"Canada":[
        [u"British Columbia", [
            u"Fraser Valley",
            u"Gulf Islands",
            u"Okanagan Valley",
            u"Similkameen Valley",
            u"Vancouver Island"]],
        [u"Nova Scotia", [
            u"Annapolis Valley"]],
        [u"Ontario", [
            u"Niagara Peninsula",
            u"Lake Erie & Pelee Island",
            u"Prince Edward County",
            u"Toronto"]],
        [u"Quebec", [
            u"Eastern Townships"]]
    ], 
    u"San Randomino, The Magical Country Where Test Data Lives":[
        "Inchoatius"
    ]
}

def format_region(country, region=None, subregion=None):
    if country and region and subregion:
        return "%s - %s: %s" % (country, region, subregion)
    if country and region:
        return "%s - %s" % (country, region)
    if country:
        return country

def get_regions_subregions():
    return_regions = []
    return_subregions = []
    location_list = []
    for country, regions in region_map.iteritems():
        location_list.append((format_region(country), (country, None, None)))
        for region in regions:
            if type(region) == list:
                subregions = region[1]
                region = region[0]
                for subregion in subregions:
                    location_list.append((format_region(country, region, subregion),
                                            (country, region, subregion)))
                    return_subregions.append(subregion)
            location_list.append((format_region(country, region),
                                    (country, region, None)))
            return_regions.append(region)
    location_list = sorted(location_list)
    return return_regions, return_subregions, location_list

countries = region_map.keys()
regions, subregions, location_tuples = get_regions_subregions()
location_list = [x[0] for x in location_tuples]
location_map = {location: tup for (location, tup) in location_tuples}

def regions_for_country(country):
    return_regions = []
    for region in region_map[country]:
        if type(region) == list:
            return_regions.append(region[0])
        else:
            return_regions.append(region)
    return return_regions

def subregions_for_country(country, region):
    return_subregions = []
    for region_ in region_map[country]:
        if type(region_) == list and region_[0] == region:
            return_subregions = return_subregions + region_[1]
    return return_subregions

def get_country(region):
    for country in countries:
        if region in regions_for_country(country):
            return country
    return None

