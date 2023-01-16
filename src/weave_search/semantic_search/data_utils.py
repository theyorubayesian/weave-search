from collections import defaultdict

import requests

REACTOME_API_URL = "https://reactome.org/ContentService/search/query"


def get_information_for_term(term, max_rows=100):

    params = {"query":term,
            "cluster": True,
            "parserType":"STD",
            "Start row":0,
            "rows":max_rows,
            "Force filters":False
            }
    r = requests.get(REACTOME_API_URL, params=params)
    if r.status_code == 200:
        res = r.json()
    else:
        res = []
        return res
    
    dbytype = {x['typeName']: x['entries'] for x in res['results']}
    res = parse_dbytype(dbytype)
    return res


all_res = {}
def parse_dbytype(dbytype):
    res = {}
    res["pathologies"] = defaultdict(list)
    res["nonpathologies"] = defaultdict(list)
    for x in dbytype['Protein']:
        if x['isDisease']:
            res["pathologies"][x['referenceName']].append(x)
        else:
            res["nonpathologies"][x['referenceName']].append(x)
    all_res['Protein'] = res    

    res = {}
    res["pathologies"] = []
    res["nonpathologies"] = []
    for x in dbytype['Complex']:
        if x['isDisease']:
            res["pathologies"].append(x)
        else:
            res["nonpathologies"].append(x)
    all_res['Complex'] = res


    res = {}
    res["pathologies"] = []
    res["nonpathologies"] = []
    for x in dbytype['Reaction']:
        if x['isDisease']:
            res["pathologies"].append(x)
        else:
            res["nonpathologies"].append(x)
    all_res['Reaction'] = res


    res = {}
    res["pathologies"] = []
    res["nonpathologies"] = []
    for x in dbytype['Pathway']:
        if x['isDisease']:
            res["pathologies"].append(x)
        else:
            res["nonpathologies"].append(x)
    all_res['Pathway'] = res
    return all_res