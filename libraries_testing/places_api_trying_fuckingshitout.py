import requests, json

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

# print(places_search(input("Query: ")))