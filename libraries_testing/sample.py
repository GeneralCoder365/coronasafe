from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.gridlayout import GridLayout

# plt.plot([1, 23, 2, 4])
# plt.ylabel('some numbers')

class MyApp(App):
    def build(self):
        # box = BoxLayout()

        # returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        
        # box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        self.window.add_widget(FigureCanvasKivyAgg(self.build_risk_rating_graph("bob", 100)))
        # return self.window
    
    def build_risk_rating_graph(self, raw_address, risk_rating):
        print(raw_address)
        print(risk_rating)
        x = raw_address
        y = risk_rating

        # colour choice
        if (risk_rating < 33.33):
            graph_colour = "lawngreen"
        elif (risk_rating < 66.66):
            graph_colour = "darkorange"
        elif (risk_rating <= 100):
            graph_colour = "firebrick"
        else:
            raise ValueError("Risk Rating not in range [0, 100]")
        
        fig = plt.figure(figsize = (3, 5))

        # creating the bar plot
        plt.bar(x, y, color = graph_colour,
                width = 0.1)
        plt.yticks(np.arange(0, 110, 10))
        
        # plt.xlabel("Courses offered")
        # plt.ylabel("No. of students enrolled")
        plt.title("COVID Risk Rating")
        plt.show()

MyApp().run()