# https://pypi.org/project/LivePopularTimes/

from datetime import datetime as dt
import livepopulartimes
# import typing

def places_search(search_query: str) -> list:
    search_results: list = livepopulartimes.get_places_by_search(search_query)
    # print(search_results)
    formatted_search_results = []

    if (len(search_results) == 0):
        return False
    else:
        formatted_search_results = []
        for i in range(len(search_results) - 1):
            name: str = (search_results[i])["name"]
            address: str = (search_results[i])["address"]
            if (name == ""):
                formatted_address = address
            else:
                formatted_address = "(" + name + ") " + address
            formatted_search_results.append(formatted_address)
    
    return formatted_search_results

def at_address_risk_rating(formatted_address):
    place_data = livepopulartimes.get_populartimes_by_address(formatted_address)
    current_popularity = place_data["current_popularity"]
    # current_popularity = None data type if no popularity data at current time
    
    if (current_popularity == None):
        current_day_of_week = dt.today().weekday()
        current_hour = dt.now().hour
        print(current_day_of_week)
        print(current_hour)

        # today's popular times (0 AM - 11 PM so index = hour)
        current_popularity = place_data["populartimes"][current_day_of_week - 1]["data"][current_hour]

        # range: [0, 100) = (0 <= x < 101)
        if (current_popularity not in range(0, 101)):
            return None
    
    return current_popularity

# print(places_search(input("Query: ")))
# at_address_risk_rating("(Westfield Montgomery) 7101 Democracy Blvd, Bethesda, MD 20852, United States")
print(at_address_risk_rating("(Starbucks) 10251 Old Georgetown Rd, Bethesda, MD 20814"))
# print(at_address_risk_rating("(McDonald's) 11564 Rockville Pike, Rockville, MD 20852"))