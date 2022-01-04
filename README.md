![logo](coronasafe_v2/coronasafe_full_logo_black_background.png)

# Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Repo Structure](#repo-structure)
* [Thanks](#thanks)
* [Contributors](#contributors)

# Introduction

*Version 2.0.1*

CoronaSafe is a Python-based application that provides easy access to a COVID-19 contraction risk rating for any global address. It does this by analyzing live foot traffic data and calculating urban density (with a time weight), giving it the potential to work for any viruses that spread through close proximity and respiratory fluids.

Since 2020, we saw and felt the internal panic that people experience every time they go out during the pandemic. The possibility of getting sick is constantly in the back of everyone's minds. This application allows people to be more informed about the world around them. We wanted people to find how busy a place would be with extreme ease, and to make it even more convenient, give them a simple "threat" bar to look at.

The goal behind the app was an incredibly simple UI with a powerful backend so that the user had a seamless experience while the high-quality backend development ensured quality results every time. To add to this, since our goal was to provide convenient access to information, we also included a button that opens an interactive heat map of live US COVID-19 case data. It sources the data directly from the constantly updating New York Times COVID cases CSV file.

* v1 was born during [MocoHacks 2021](https://mocohacks.org/). The app only included the surrounding risk calculation algorithm and the heat maps. It was wrapped in a Tkinter GUI.
* v2 was created for the [2021 Congressional App Challenge](https://www.congressionalappchallenge.us/). The backend code was reused for the heat maps and the surrounding risk calculation. The local risk calculation and master risk algorithm was added. It was wrapped in a new Kivy Python GUI.
* v3 of the app is currently being worked on, and will include a publicly accessible website, as well as support for more platforms, including desktop and mobile applications.

# Features

### COVID-19 Risk Calculator

Takes a search query in input field from user and runs it through a novel COVID-19 contraction risk calculation algorithm

* Takes in the search query, passes through the Google Maps Places API and outputs results to user as a dropdown
* User then selects one of the addresses

### COVID-19 Contraction Risk Calculation Algorithm

Generates risk level bar graph (through `matplotlib`) for the user chosen address

### Local Risk Calculation Algorithm

Uses the `livepopulartimes` library to get current live popular times (works best for named places such as a mall)

* If the live popular times isn't available, it cross references with the average popularity at the current day and time
* Outputs a local risk rating between 0 and 100

### Surrounding Risk Calculation Algorithm

Uses Google Geocoding API to transform address into coordinates that get passed through the Google Places API to output named places in a 0.5 mile radius around the given address
                
* Generates a list of "popular" locations within the search radius such as airports and mall
* Factors in the number of "popular" locations within the search radius and time-weights based on the current time of day
* Outputs a surrounding risk rating between 0 - 100

### Master Risk Calculation Algorithm

Combines both inputs (if available) to give a cumulative COVID-19 contraction risk rating between 0 - 100
        
### Real Time COVID-19 Maps

Uses `pandas` to read the following CSV files:
* https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv
* https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv
* https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv

SSL is imported to connect `plotly` with the CSV files. Two maps are created: a *heat map*, which collects the sum of all COVID-19 cases in each state, and a *chloropleth map*, which collects the sum of all COVID-19 cases in each county at a particular state that the user inputs.
      
### Choropleth Map

`pandas` iterates through all the columns that contain the keyword for a particular state:

* A manually coded example (doesn't take into account for user input)': ``df_Maryland = df[ df['state'] == "Maryland"]``
* Pandas is used to set the date to the current date by using the built-in  function `max()` function and then is used to iterate through all COVID-19 cases for the current date in that particular state
* Pandas is also used calculate the sum of all COVID-19 cases and deaths for a particular state through the built-in function `sum()`. This iterates through all cases and deaths for each county for that state in the CSV file.
* Plotly is used to make a choropleth map that iterates through the COVID-19 data for all counties in order to create the map
        
### Heat Map

* `pandas` is again used set the date to the current date by using the built-in function `max()` function and then is used to iterate through all COVID-19 cases for the current date in that particular state
* `pandas` is also used to calculate the sum of all COVID-19 cases and deaths in the U.S. through the built-in function `sum()`. This iterates through all cases and deaths for for each state in the csv file which gets added up to calculate the sum of all COVID-19 cases and deaths in the U.S.
* Pandas is used to calculate the sum of all COVID-19 cases and deaths in each U.S. state through the built-in function `sum()` and `to_frame`.
* Plotly is used to make a heat map that iterates through the COVID-19 data for all states in order to create the map

# Repo Structure

### Final Product/Frontend
[`coronasafe_v2`](coronasafe_v2) ⟶ [`coronasafe_v2_ui.py`](coronasafe_v2/coronasafe_v2_ui.py)

Contains frontend for CoronaSafe. Interacts with [`coronasafe_v2_backend.py`](coronasafe_v2/coronasafe_v2_backend.py)

### CoronaSafe Backend
[`coronasafe_v2`](coronasafe_v2) ⟶ [`coronasafe_v2_backend.py`](coronasafe_v2/coronasafe_v2_backend.py)

Contains places search function, master risk calculation algorithm, and COVID case maps constructor caller.

* [`local_risk_calculator.py`](coronasafe_v2/local_risk_calculator.py), which contains local risk calculation algorithm.
* [`surrounding_risk_calculator.py`](coronasafe_v2/surrounding_risk_calculator.py), which contains surrounding risk calculation algorithm (factoring in urban density and a time of day weight).
* [`heat_maps.py`](coronasafe_v2/heat_maps.py), which contains US and dtate heat map constructor functions.

# Thanks

### APIs
*Note: you must first obtain a [`Google API Key`](https://developers.google.com/maps/documentation/javascript/get-api-key)*

* [`Google Geocoding API`](https://developers.google.com/maps/documentation/geocoding/overview)
* [`Google Places API`](https://developers.google.com/maps/documentation/places/web-service/overview)

### Libraries
* [`requests`](https://pypi.org/project/requests/)
* [`livepopulartimes`](https://github.com/GrocerCheck/LivePopularTimes)
* [`plotly`](https://plotly.com/python/getting-started/)
* [`pandas`](https://pandas.pydata.org/docs/getting_started/install.html)
* [`ssl`](https://pypi.org/project/ssl/)
* [`argparse`](https://pypi.org/project/argparse/)
* [`python-dotenv`](https://pypi.org/project/python-dotenv/)
* [`pathlib`](https://pypi.org/project/pathlib/)

# Contributors

### v2 Team

Ainesh Chatterjee and Botond Parkanyi

* Kivy Python GUI (currently in use): Developed by Ainesh Chatterjee
* C# GUI (pending integration): Developed by Botond Parkanyi

### v1 Team

Ainesh Chatterjee, Lorenz Driza and Salamun Nuhin

*Special thanks to Charles Wang for the awesome logo!*