# Kivy UI Core
from kivy.app import App
# from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
# Importing Drop-down from the module to use in the program
from kivy.uix.dropdown import DropDown

# Kivy MatPlotLib
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import numpy as np
import matplotlib.pyplot as plt

# CoronaSafe Backend
import coronasafe_v2_backend as cs_backend

# UI REQUIREMENTS:
# MVP:
    # 1 PAGE
    # HEADER: CORONASAFE
    # TOP:
        # QUERY INPUT FIELD -> SEARCH BUTTON -> RESULTS SHOWN AS DROPDOWN BELOW INPUT FIELD -> USER SELECTS WHICH ONE -> 
        # CHOSEN ONE REPLACES INPUT FIELD -> SEARCH BUTTON (SAME ONE IDEALLY FOR STREAMLINING) -> RISK RATING (VERTICAL IDEALLY) BAR GRAPH DISPLAYED
# IF TIME PERMITS:
    # BOTTOM:
        # LABEL: US COVID HEAT MAP | STATE COVID GRAPH
        # LEFT SIDE: US COVID HEAT MAP BUTTON -> OPEN US COVID HEAT MAP (IN BROWSER)
        # RIGHT SIDE: STATES DROPDOWN -> USER SELECTS STATE -> STATE COVID HEAT MAP BUTTON -> OPENS STATE COVID GRAPH (IN BROWSER)

# UI COMPLETED:
    # HEADER: CORONASAFE
    # TOP:
        # QUERY INPUT FIELD -> SEARCH BUTTON -> RESULTS SHOWN AS DROPDOWN BELOW INPUT FIELD -> USER SELECTS WHICH ONE -> 
        # CHOSEN ONE REPLACES INPUT FIELD -> SEARCH BUTTON (SAME ONE IDEALLY FOR STREAMLINING) -> RISK RATING (VERTICAL IDEALLY) BAR GRAPH DISPLAYED
        # BOTTOM:
            # US COVID HEAT MAP BUTTON -> OPEN US COVID HEAT MAP (IN BROWSER)


# CODE:
class CoronaSafeUI(App):
# class CoronaSafeUI(MDApp):
    # CORE BUILD:
    def build(self):
        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # LOGO image widget
        self.window.add_widget(Image(source="coronasafe_full_logo.png"))

        # WHERE TO? label widget
        self.where_to = Label(
                        text= "WHERE TO? ",
                        font_size= 18,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.where_to)

        # SEARCH QUERY input widget
        self.search_query = TextInput(
                    multiline= False,
                    padding_y= (15,8),
                    size_hint= (1, 0.5)
                    )

        self.window.add_widget(self.search_query)

        # SEARCH PLACE button widget
        self.search_button = Button(
                      text= "SEARCH",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.search_button.bind(on_press=self.search_results_dropdown_builder)
        self.window.add_widget(self.search_button)

        # COVID RISK CALCULATION button widget
        self.risk_button = Button(
                      text= "CALCULATE RISK",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.window.add_widget(self.risk_button)
        self.risk_button.disabled = True
        self.risk_button.bind(on_press=self.get_risk_rating)

        # US COVID MAP button widget
        self.us_covid_map = Button(
                      text= "OPEN US COVID MAP",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.window.add_widget(self.us_covid_map)
        self.us_covid_map.bind(on_press=self.generate_us_heat_map)

        return self.window
    

    # LIVE FUNCTIONS:
    def search_results_dropdown_builder(self, event):
        search_query = self.search_query.text
        # print(search_query)

        if (search_query != False):
            self.search_query.disabled = True
            search_results = cs_backend.places_search(search_query)
            # print(search_results)
            search_results_length = len(search_results)

            self.search_results_dropdown = DropDown()
            search_results_length = len(search_results)

            for i in range(search_results_length):
                # Adding button in drop down list
                # sp makes kind of dynamic
                result = Button(text = search_results[i], font_size = "12sp", size_hint_y = None, height = 40)
            
                # binding the button to show the text when selected
                result.bind(on_release = lambda btn: self.search_results_dropdown.select(btn.text))

                # then add the button inside the dropdown
                self.search_results_dropdown.add_widget(result)

            self.search_button.bind(on_release = self.search_results_dropdown.open)
            # one last thing, listen for the selection in the 
            # dropdown list and assign the data to the button text.
            
            self.search_results_dropdown.bind(on_select = lambda instance, x: setattr(self.search_query, 'text', x))

            self.risk_button.disabled = False
        
    
    def get_risk_rating(self, event):
        raw_address = self.search_query.text

        risk_rating = cs_backend.master_risk_calculator(raw_address)
        # print(risk_rating)

        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        
        self.window.add_widget(FigureCanvasKivyAgg(self.build_risk_rating_graph(risk_rating)))

        # return self.window
    

    def build_risk_rating_graph(self, risk_rating):
        # print(risk_rating)
        
        x = "Risk Rating"
        y = risk_rating

        # colour choice
        if (risk_rating <= 33.33):
            graph_colour = "lawngreen"
            x = "LOW"
        elif (risk_rating <= 66.66):
            graph_colour = "darkorange"
            x = "MEDIUM"
        elif (risk_rating <= 100):
            graph_colour = "firebrick"
            x = "HIGH"
        else:
            raise ValueError("Risk Rating not in range [0, 100]")
        
        fig = plt.figure("COVID Risk Rating", figsize = (5, 5))

        # creating the bar plot
        plt.bar(x, y, color = graph_colour,
                width = 0.1)
        plt.yticks(np.arange(0, 110, 10))
        
        plt.title("COVID Risk Rating")
        plt.show()
    
    def generate_us_heat_map(self, event):
        cs_backend.make_us_heat_map()
            
        
# run CoronaSafeUI class
if __name__ == "__main__":
    CoronaSafeUI().run()