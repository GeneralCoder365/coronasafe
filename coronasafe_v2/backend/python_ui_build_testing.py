from time import sleep

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
# Importing Drop-down from the module to use in the program
from kivy.uix.dropdown import DropDown

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



class CoronaSafeUI(App):
    def build(self):
        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image widget
        self.window.add_widget(Image(source="logo.png"))

        # label widget
        self.where_to = Label(
                        text= "WHERE TO? ",
                        font_size= 18,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.where_to)

        # text input widget
        self.search_query = TextInput(
                    multiline= False,
                    padding_y= (20,20),
                    size_hint= (1, 0.5)
                    )

        self.window.add_widget(self.search_query)

        # button widget
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

        return self.window

    def callback(self, event):
        print()
    
    def search_results_dropdown_builder(self, event):
        search_query = self.search_query.text
        print(search_query)

        if (search_query != False):
            self.search_query.disabled = True
            search_results = cs_backend.places_search(search_query)
            print(search_results)
            search_results_length = len(search_results)
            # change label text to "Hello + user name!"
            # self.greeting.text = "Hello " + self.user.text + "!"

            self.search_results_dropdown = DropDown()
            search_results_length = len(search_results)

            for i in range(search_results_length):
                # Adding button in drop down list
                result = Button(text = search_results[i], size_hint_y = None, height = 40)
            
                # binding the button to show the text when selected
                result.bind(on_release = lambda btn: self.search_results_dropdown.select(btn.text))
            
                # then add the button inside the dropdown
                self.search_results_dropdown.add_widget(result)

            self.search_button.bind(on_release = self.search_results_dropdown.open)
            # self.search_results_dropdown.open
            # one last thing, listen for the selection in the 
            # dropdown list and assign the data to the button text.
            # self.search_results_dropdown.bind(on_select = lambda instance, x: setattr(self.search_button, 'text', x))
            
            # self.search_results_dropdown.bind(on_select = lambda instance, x: setattr(self.search_query, 'text', x))
            self.search_results_dropdown.bind(on_select = lambda instance, x: setattr(self.search_query, 'text', x))

            sleep(0.5)

            raw_address = self.search_query.text
            print(raw_address)
        



# run Say Hello App Calss
if __name__ == "__main__":
    CoronaSafeUI().run()