# **moco_hacks_2021**
# **Corona-Safe**
#
# [**PROJECT BREAKDOWN**](https://docs.google.com/presentation/d/17h2YCBYd2IV8gmgW2EP3E4Fs_UIJhe6aSL9WO3uOtms/edit?usp=sharing)
#
# **FILE STRUCTURE BREAKDOWN**
1. Final Product:
    - `final_product` --> `coronasafe.py`
        - Contains all the code for the project, including GUI
            - This is because importing other python files and external functions is difficult in Tkinter.
2. Foot Traffic Backend (not run in final product):
    - `backend` --> `foot_traffic` --> `foot_traffic.py`
        - Contains all code for foot traffic processing & geocoding.
    - `backend` --> `foot_traffic` --> `geocoding.py`
        - Contains all code for geocoding.
#
# **APIs USED**
#### [`Google Geocoding API`](https://developers.google.com/maps/documentation/geocoding/overview)
#### [`Google Places API`](https://developers.google.com/maps/documentation/places/web-service/overview)
#### **Prerequisite**: [`Google API Key`](https://developers.google.com/maps/documentation/javascript/get-api-key)
#
# **DOCUMENTATION**
## **Main Groups**
1. COVID-19 risk calculator based on an input address
    - Libraries used: [`datetime`](https://docs.python.org/3/library/datetime.html), and [`requests`](https://pypi.org/project/requests/)
        - Pip installation commands:
            - `datetime`: `pip install DateTime`
            - `requests`: `pip install requests`
    - Parameters: `google_api_key, address, city, state, zip_code, search_radius`
        - state needs to be formatted in their 2-letter, all caps format
        - Sample parameters (for the Empire State Building): `g_api_key, "20 W 34th St", "New York", "NY", "10001", radius`
            - NOTE: the default value for radius is set to 0.5 (miles)
    - functionality breakdown:
        - Uses address fields from user to generate a formatted address: `address_formatter(address, city, state, zip_code)`
        - The formatted address is geocoded using the Google Geocoding API: `master_geocoding(google_api_key, address, city, state, zip_code)`
            - A json request is made to access the Google Geocoding API
            - The latitude and longitude of the address is stored
        - A radius is then traced around the geocoded coordinates, and a list of (up to 20) nearby locations is extracted using the Google Places API: `key_buildings_search(google_api_key, address, city, state, zip_code, search_radius)`
            - A json request is made to access the Google Geocoding API
            - Each item in the list contains a types metadata
                - This is checked against a list of important types that signify a location that usually has a lot of people, and the total number of important locations is stored
        - The raw number from c.ii. is taken and multiplied by a weight relative to the current hour of day before being divided by the maximum time-weighted and multiplied by 100 to get a scale of risk from 0-100: `risk_rating_scaler(google_api_key, address, city, state, zip_code, search_radius)`
            - Weightage approximates typical times when people are the busiest on a  0.0-1.0 scale
        - The 100 scale is divided in thirds to output a low, medium, or high risk level that is returned to be turned into a visual representation in the GUI: `risk_rating_scaler(google_api_key, address, city, state, zip_code, search_radius) & tkinter GUI code`
            - Sample function call (for the Empire State Building): `risk_rating_scaler(g_api_key, "20 W 34th St", "New York", "NY", "10001", radius)`
2. Real time COVID-19 map that updates every 24 hours
  Libraries used: [`ssl`](https://docs.python.org/3/library/ssl.html), [`pandas`](https://pandas.pydata.org/), [`csv`](https://docs.python.org/3/library/csv.html), and [`urllib`](https://docs.python.org/3/library/urllib.html#module-urllib)

    * Pip installation commands:

    * `ssl`: `pip install ssl`
    * `pandas`: `pip install pandas`
  * functionality breakdown:

    * Uses pandas to read the following csv files:

    * ``https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv``
    * `https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv`
    * `https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv`
    * SSL is imported to connect plotly with the CSV files through this code:

    * ``ssl._create_default_https_context = ssl._create_unverified_context``
    * Two maps are created:

    * A heat map that collects the sum of all COVID-19 cases in each state.
    * A choropleth map that collects the sum of all COVID-19 cases in each county at a particular state that the user inputs.
    * Choropleth map:

    * Pandas iterates through all the columns that contain the keyword for a particular state:
      * A manually coded example (doesn't take into account for user input)': ``df_Maryland = df[ df['state'] == "Maryland"]``
    * Pandas is used to set the date to the current date by using the built-in  function `max()` function and then is used to iterate through all COVID-19 cases for the current date in that particular state:
      * `last_date = df['date'].max()`
      * `df = df_Maryland[ df_Maryland['date'] == last_date]` (manually coded example)
    * Pandas is also used calculate the sum of all COVID-19 cases and deaths for a particular state through the built-in function `sum()`:
      * `df['cases'].sum()`
      * `df['deaths'].sum()`
      * This iterates through all cases and deaths for each county for that state in the csv file.
    * Plotly is used to make a choropleth map that iterates through the COVID-19 data for all counties in order to create the map:
      * `fig = px.choropleth(df, geojson=counties, locations='fips', color='cases', color_continuous_scale="Viridis", range_color=(0, 20000) )`
    * Heat map:

    * Pandas is again used set the date to the current date by using the built-in  function `max()` function and then is used to iterate through all COVID-19 cases for the current date in that particular state:

      * `last_date = df['date'].max()`
      * `df = df[ df['date'] == last_date]`
    * Pandas is also used to calculate the sum of all COVID-19 cases and deaths in the U.S. through the built-in function `sum()`:

      * `df['cases'].sum()`
      * `df['deaths'].sum()`
      * This iterates through all cases and deaths for for each state in the csv file which gets added up to calculate the sum of all COVID-19 cases and deaths in the U.S.
    * Pandas is used to calculate the sum of all COVID-19 cases and deaths in each U.S. state through the built-in function `sum()` and `to_frame`:

      * `df = df.groupby('state')['cases'].sum().to_frame()`
    * Plotly is used to make a heat map that iterates through the COVID-19 data for all states in order to create the map:

      * `fig = px.choropleth(df, locations=df['Abbreviation'], color=df['cases'], locationmode="USA-states", color_continuous_scale="hot", range_color=(0, 4500000), scope="usa"))`