import requests

# formats address chunks into whole address
def address_formatter(address, city, state, zip_code):
    # Ex: "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
    # Make sure state is just 2 letters!
    formatted_address = (address + ", " + city + ", " + state + " " + zip_code + ", USA")
    return formatted_address

# gets latitude, longitude
def get_lat_long(google_api_key, address, city, state, zip_code):
    input_address = address_formatter(address, city, state, zip_code)

    lat = None
    long = None
    place_id = None
    status = None
    api_key = google_api_key

    # generates json request
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={input_address}&key={api_key}"

    r = requests.get(endpoint)

    if r.status_code not in range(200, 299):
        return [None, None]
    
    # stores json file and attemps to retrieve latitude and longitude
    try:
        json_file = r.json()
        results = json_file["results"][0]
        lat = results["geometry"]["location"]["lat"]
        long = results["geometry"]["location"]["lng"]
        status = json_file["status"]

        # NON-ERRORS:
        # "OK" indicates that no errors occurred; the address was successfully parsed and at least one geocode was returned
        if (status == "OK"):
            return [lat, long]

        # "ZERO_RESULTS" indicates that the geocode was successful but returned no results. This may occur if the geocoder was passed a non-existent address
        elif (status == "ZERO_RESULTS"):
            return [status, status]
        

        # ERRORS:
        # "REQUEST_DENIED" indicates that your request was denied.
        elif (status == "REQUEST_DENIED"):
            return [status, status]
        
        # "INVALID_REQUEST" generally indicates that the query (address, components or latlng) is missing.
        elif (status == "INVALID_REQUEST"):
            return [status, status]
        
        # "UNKNOWN_ERROR" indicates that the request could not be processed due to a server error. The request may succeed if you try again.
        elif (status == "UNKNOWN_ERROR"):
            return [status, status]

    # except case if json retrieval gives an error
    except:
        # Pass: https://www.google.com/search?q=pass+python+function&rlz=1C1SQJL_enUS806US806&oq=pass+python&aqs=chrome.2.69i57j0l6j69i65.2918j0j1&sourceid=chrome&ie=UTF-8 
        pass
        return [None, None]

# master function
def master_geocoding(google_api_key, address, city, state, zip_code):
    return get_lat_long(google_api_key, address, city, state, zip_code)