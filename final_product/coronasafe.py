import tkinter as tk
from tkinter import ttk
import plotly.express as px
from plotly.offline import plot
import plotly.io as pio
import pandas as pd
import ssl
import urllib.request
from urllib.request import urlopen
import os
import json
import datetime as dt
import requests
from PIL.ImageTk import PhotoImage
 
adress = []
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# first window frame startpage
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
 
        canvas = tk.Canvas(self, width=1800,height=900, background = "#0F111A") 
        canvas.grid(columnspan=18,rowspan=9)
 
        #Title
        Title_lbl = tk.Label(self, text = "Corona-Safe", bg = "#0F111A", fg = "white", font = ("MS Gothic",40))
        Title_lbl.grid(columnspan = 8, rowspan = 2, column = 5, row = 1)
 
        button1 = ttk.Button(self, text ="Next",
        command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
           
  
# second window frame page1 
class Page1(tk.Frame):
     
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
         
        canvas = tk.Canvas(self, width=1800,height=900, background = "#0F111A")
        canvas.grid(columnspan=18,rowspan=9)
 
        #Title
        Title_lbl2 = tk.Label(self, text = "Corona-Safe", bg = "#0F111A", fg = "white")
        Title_lbl2.grid(columnspan = 8, rowspan = 2, column = 5, row = 1)
 
        #State Cases
        Title_lbl3 = tk.Label(self, text = "State Cases", bg = "#0F111A", fg = "white")
        Title_lbl3.grid(columnspan = 8, rowspan = 2, column = 5, row = 4)
 
        txt_adress = tk.Entry(self)
        txt_adress.grid(columnspan = 8, column = 5, row = 3)
 
        def get_adress():
            adress = txt_adress.get()
            adress = adress.split(",")
            print(adress)
            return adress
 
        #Severity Level Finder
        def severity_level():
            adress = txt_adress.get()
            adress = adress.split(",")
            address = adress[0]
            apt_num = adress[1]
            city = adress[2]
            zip_code = adress[3]
            state = adress[4]
            # major values
            # Google API Key for all Google API interactions
            g_api_key = "AIzaSyA592HwCkixwp7W8zRekEf2NZuyfKZNfvc"
 
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
 
 
            # half mile radius for optimal results for scale within 20 value range
            radius = 0.5
 
            # Searches for important buildings nearby, takes in API key, address parameters, and search search radius
            def key_buildings_search(google_api_key, address, city, state, zip_code, search_radius):
                search_results = None
                important_types = ["airport", "amusement_park", "aquarium", "art_gallery", "bank", "casino", "clothing_store", 
                "convenience_store", "department_store", "drugstore", "movie_theater", "museum", "park", "pharmacy", "restaurant", "shopping_mall", "stadium", 
                "store", "subway_station", "supermarket", "tourist_attraction", "zoo", "lodging"]
 
                # not actually used but helps with visualization of data pipeline
                is_important = False
                # converts radius from miles to meters
                radius = 1609.34 * search_radius
                base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
 
                # gets coordinates for given address
                geo_data = master_geocoding(google_api_key, address, city, state, zip_code)
                latitude = geo_data[0]
                longitude = geo_data[1]
 
                # sends json request
                endpoint = f"{base_url}?location={latitude}, {longitude}&radius={str(radius)}&opennow&rankby=prominence&key={google_api_key}"
 
                r = requests.get(endpoint)
 
                if r.status_code not in range(200, 299):
                    return None
 
                # attempts to parse json, and find key locations within 0.5 mile radius, that meet important location types criteria, and gives a total number of them
                try:
                    # sends a json request
                    json_file = r.json()
                    search_results = json_file["results"]
                    raw_number = len(search_results)
                    final_number = 0
                    status = json_file["status"]
 
                    # logic to get if a place is important or not by iterating through types within each resultant location within 0.5 mile radius
                    i = 0
                    k = 0
                    already_true = False
                    while (i<raw_number):
                        is_important = False
                        already_true = False
                        types_length = len(search_results[i]["types"])
                        k = 0
                        while ((k < types_length) and (already_true == False)):
                            if(search_results[i]["types"][k] in important_types):
                                is_important = True
                                already_true = True
                            else:
                                is_important = False
                            k = k + 1
                        if((already_true == True)):
                            final_number = final_number + 1
                        i = i + 1
                        
 
                    # NON-ERRORS:
                    # "OK" indicates that no errors occurred; the address was successfully parsed and at least one geocode was returned
                    if (status == "OK"):
                        # return [final_number, search_results]
                        return final_number
                    # "ZERO_RESULTS" indicates that the geocode was successful but returned no results. This may occur if the geocoder was passed a non-existent address
                    elif (status == "ZERO_RESULTS"):
                        return status
                    
 
                    # ERRORS:
                    # "REQUEST_DENIED" indicates that your request was denied.
                    elif (status == "REQUEST_DENIED"):
                        return status
                    
                    # "INVALID_REQUEST" generally indicates that the query (address, components or latlng) is missing.
                    elif (status == "INVALID_REQUEST"):
                        return status
                    
                    # "UNKNOWN_ERROR" indicates that the request could not be processed due to a server error. The request may succeed if you try again.
                    elif (status == "UNKNOWN_ERROR"):
                        return status
 
                # except case
                except:
                    # Pass: https://www.google.com/search?q=pass+python+function&rlz=1C1SQJL_enUS806US806&oq=pass+python&aqs=chrome.2.69i57j0l6j69i65.2918j0j1&sourceid=chrome&ie=UTF-8 
                    pass
                    return None
 
            # converts raw number of important locations to relative scale with weightage based on max important location density and current hour, as a value from 0-100
            def risk_rating_scaler(google_api_key, address, city, state, zip_code, search_radius):
                try:
                    # gets number of important locations
                    raw_value = int(key_buildings_search(google_api_key, address, city, state, zip_code, search_radius))
                    # gets current hour
                    current_hour = int(dt.datetime.now().hour)
                    # dictionary of weights from 0.0 to 1.0 based on hour of day on 24 hour system
                    time_weights = {
                        0: 0.2,
                        1: 0.1,
                        2: 0.1,
                        3: 0.1,
                        4: 0.1,
                        5: 0.2,
                        6: 0.3,
                        7: 0.4,
                        8: 0.5,
                        9: 0.5,
                        10: 0.5,
                        11: 0.6,
                        12: 0.6,
                        13: 0.7,
                        14: 0.7,
                        15: 1.0,
                        16: 1.0,
                        17: 1.0,
                        18: 0.8,
                        19: 0.8,
                        20: 0.8,
                        21: 0.5,
                        22: 0.5,
                        23: 0.2
                    }
 
                    # max density * most popular time of day to create "total value" for percentage calculation
                    max = 20 * 1.0
                    # applies weights to raw number of important locations
                    weighted_value = ((raw_value * time_weights[current_hour])/max) * 100
                    # print(raw_value)
                    # print(weighted_value)
 
                    # assigns scale rating based on weighted_value & returns it
                    if(weighted_value < 33.33):
                        return "low"
                    elif(weighted_value < 66.66):
                        return "medium"
                    elif(weighted_value <= 100):
                        return "high"
                    else:
                        return "Error"
 
                # except case
                except:
                    return "Error"
            risk_lvl = risk_rating_scaler(g_api_key, address, city, state, zip_code, radius)
            print(risk_lvl)
            if risk_lvl == "low":
                #Severity level Button
                d_lvl = tk.Button(self, width = 20, bg = "green", command = lambda:get_adress())
                d_lvl.grid(columnspan = 4, column = 9, row = 7)
            elif risk_lvl == "medium":
                #Severity level Button
                d_lvl = tk.Button(self, width = 20, bg = "orange", command = lambda:get_adress())
                d_lvl.grid(columnspan = 4, column = 8, row = 7)
            else:
                #Severity level Button
                d_lvl = tk.Button(self, width = 20, bg = "red", command = lambda:get_adress())
                d_lvl.grid(columnspan = 4, column = 8, row = 8)
 
 
        #Severity Level Button
        s_finder = tk.Button(self, text = "Find Danger Level", bg = "#0A0C15", fg = "white", command = lambda:severity_level())
        s_finder.grid(columnspan = 1, column = 10, row = 6)
 
        #Severity Level
        Title_lbl4 = tk.Label(self, text = "Danger Level", bg = "#0F111A", fg = "white")
        Title_lbl4.grid(columnspan = 8, rowspan = 2, column = 5, row = 6)
 
        #Directions
        adress_lbl2 = tk.Label(self, text = "Input your desired address as 'street name,suite,city,zip-code,state'", bg = "#0F111A", fg = "white")
        adress_lbl2.grid(columnspan = 8, column = 5, row = 2)
 
        #Text Entry
       
 
        #gets heat map
        def get_hmap():
            ssl._create_default_https_context = ssl._create_unverified_context
            response = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
            response1 = urllib.request.urlopen('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')
 
 
 
            url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
            df = pd.read_csv(url, converters={'fips': lambda x: str(x)})
 
            url = "https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv"
            df_abbrev = pd.read_csv(url)
 
            last_date = df['date'].max()
            df = df[ df['date'] == last_date]
            print(df['cases'].sum())
            df = df.groupby('state')['cases'].sum().to_frame()
            df = pd.merge(df, df_abbrev, left_on=df.index, right_on='State')
 
            fig = px.choropleth(df, locations=df['Abbreviation'], color=df['cases'],
                                locationmode="USA-states",
                                color_continuous_scale="hot",
                                range_color=(0, 4500000),
                                scope="usa"
                                    )
 
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo=dict(bgcolor= '#4E5D6C',lakecolor='#4E5D6C'))
 
            plot(fig)
 
        #get_adress2
 
 
        #Enter Button
        adress_enter = tk.Button(self, text = "Enter", bg = "#0A0C15", fg = "white", command = lambda:get_adress())
        adress_enter.grid(columnspan = 1, column = 11, row = 3)
 
        #Heat Map Button
        get_heatm_btn = tk.Button(self, text = "Get Heat Map", bg = "#0A0C15", fg = "white", command = lambda:get_hmap())
        get_heatm_btn.grid(columnspan = 1, column = 11, row = 5)
 
        #Graph Button
        graph_finder = tk.Button(self, text = "Get Map of Covid data", bg = "#0A0C15", fg = "white", command = lambda:state_graph())
        graph_finder.grid(columnspan = 1, column = 12, row = 5)
 
        #State Text Field
        state_txt = tk.Entry(self)
        state_txt.grid(columnspan = 8, column = 5, row = 5)
 
        #Find Graph
        def state_graph():
            state_input = state_txt.get()
            ssl._create_default_https_context = ssl._create_unverified_context
            response1 = urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
 
            with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
                counties = json.load(response)
 
            counties["features"][0]
 
 
 
            response = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
 
 
            url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
            df = pd.read_csv(url, converters={'fips': lambda x: str(x)})
 
            #Pick a state
            df_Maryland = df[ df['state'] == state_input]
            last_date = df['date'].max()
            df = df_Maryland[ df_Maryland['date'] == last_date]
 
            print(df['cases'].sum())
            print(df['deaths'].sum())
 
 
            fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',
                                    color_continuous_scale="Viridis",
                                    range_color=(0, 20000)
                                    )
 
            #Added for zoom and to set rest of map to invisible. 
            fig.update_geos(fitbounds="locations", visible=False)
 
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_text='COVID-19 Cases From Each County in Maryland')
            plot(fig)
 
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Back",
                            command = lambda : controller.show_frame(StartPage))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
 
  
# Driver Code
app = tkinterApp()
app.mainloop()