# https://github.com/GeneralCoder365/coronasafe

from datetime import datetime as dt
import requests, json

import local_risk_calculator as local_risk
import surrounding_risk_calculator as surrounding_risk


def places_search(search_query: str, g_api_key = "AIzaSyDIZyDl-PXON-jAk67gpnVtHSxoWiJdC3M") -> list:
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    # get method of requests module
    # return response object
    r = requests.get(base_url + 'query=' + search_query + '&key=' + g_api_key)

    # stores data in json file
    json_file = r.json()
    search_results = json_file["results"]
    # print(search_results)
    formatted_search_results = []

    if (len(search_results) == 0):
        return False
    else:
        i = 0
        while ((i < 10) and (i < len(search_results))):
            # name: str = (search_results[i])["name"]
            name: str = (search_results[i])["name"]
            # print(name)
            address: str = (search_results[i])["formatted_address"]
            # print(address)
            if (name == ""):
                formatted_address = address
            else:
                formatted_address = "(" + name + ") " + address
            formatted_search_results.append(formatted_address)

            i += 1
    
    return formatted_search_results

# tester code
# print(places_search(input("Query: ")))


def master_risk_calculator(raw_address: str) -> int:
    try:
        local_risk_rating = local_risk.at_address_risk_rating(raw_address)
    except KeyError:
        local_risk_rating = None
    # print(local_risk_rating)
    try:
        surrounding_risk_rating = surrounding_risk.surrounding_risk_rating(raw_address)
    except Exception:
        surrounding_risk_rating = None
    # print(surrounding_risk_rating)
    cumulative_risk_rating = 0

    if (((type(local_risk_rating) == int) or (type(local_risk_rating) == float)) and 
    (((type(surrounding_risk_rating) == int) or (type(surrounding_risk_rating) == float)))):
        cumulative_risk_rating = (local_risk_rating * 0.8) + (surrounding_risk_rating * 0.2)
    elif ((type(local_risk_rating) == int) or (type(local_risk_rating) == float)):
        cumulative_risk_rating = local_risk_rating
    elif ((type(surrounding_risk_rating) == int) or (type(surrounding_risk_rating) == float)):
        cumulative_risk_rating = surrounding_risk_rating
    else:
        return False
    
    cumulative_risk_rating = round(cumulative_risk_rating, 2)
    # cumulative_risk_rating = "Cumulative Risk: " + str(cumulative_risk_rating)
    return cumulative_risk_rating

# tester code
# print(master_risk_calculator("(Westfield Montgomery) 7101 Democracy Blvd, Bethesda, MD 20852, United States"))


# master tester code (can change [0] to another index for the list but make sure you know that it is within the length of the results - 1)
print(master_risk_calculator(places_search(input("Query: "))[0]))