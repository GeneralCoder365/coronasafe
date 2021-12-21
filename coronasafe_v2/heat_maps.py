import plotly.express as px
from plotly.offline import plot
import plotly.io as pio
import pandas as pd
import ssl
import urllib.request
from urllib.request import urlopen
import json


# makes US heat map
def make_us_heat_map():
    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    response1 = urllib.request.urlopen('https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv')

    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    df = pd.read_csv(url, converters={'fips': lambda x: str(x)})

    url = "https://raw.githubusercontent.com/jasonong/List-of-US-States/master/states.csv"
    df_abbrev = pd.read_csv(url)

    last_date = df['date'].max()
    df = df[ df['date'] == last_date]
    # print(df['cases'].sum())
    df = df.groupby('state')['cases'].sum().to_frame()
    df = pd.merge(df, df_abbrev, left_on=df.index, right_on='State')

    fig = px.choropleth(df, locations=df['Abbreviation'], color=df['cases'],
                        locationmode="USA-states",
                        # alternate colour scheme -> color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                        # _r reverses the hot colour scheme
                        color_continuous_scale="hot_r",
                        range_color=(0, 4500000),
                        scope="usa"
                            )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo=dict(bgcolor= '#4E5D6C',lakecolor='#4E5D6C'))
    
    fig.write_html('frontend/assets/temp-plot.html')

    # plot(fig)

# # tester code
# make_us_heat_map()

# makes state case graph
def make_state_case_graph(state_input):
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

# tester code -> I think the format for the state is: Ex. "MD"
# make_state_case_graph("MD")