# # -*- coding: utf-8 -*-
#
# # Form implementation generated from reading ui file 'F:\User Files\Downloads\AegisGUI.ui'
# #
# # Created by: PyQt5 UI code generator 5.11.3
# #
# # WARNING! All changes made in this file will be lost!
#
# import kivy
# kivy.require('1.0.6')
import tkinter as tk
from tkinter import ttk, scrolledtext, Radiobutton
from tkinter.ttk import Combobox
# from kivy.app import App
# from kivy.uix.label import Label
# from kivy.base import runTouchApp
# from kivy.lang import Builder
# # import aegis
import os
# import subprocess
cmd = 'python aegis.py --pot aegisec.pot --domain aegisec.me'
meme = os.system(cmd)
#
# root = Builder.load_string(r'''
#
# ScrollView:
#
#     Label:
#
#         text: 'meme'
#
#         font_size: 30
#
#         size_hint_x: 1.0
#
#         size_hint_y: None
#
#         text_size: self.width, None
#
#         height: self.texture_size[1]
#
# ''')
# class MyApp(App):
#     def build(self):
#         return Label(text='Hello world')
#
# if __name__ == '__main__':
#     import sys
#     runTouchApp(root)
#     #MyApp().run()
#     currentDir = os.getcwd()

win = tk.Tk()
win.title("Forensic Tweet Analyser")
win.minsize(width=1900, height=1500)
win.maxsize(width=1900, height=1500)
win.configure(background="#eaeaea")

# Select File Label
ttk.Label(win, text="File Name:").place(x=5, y=1)

# User selected file
jsonFile = tk.StringVar()
jsonFileNameEntered = ttk.Entry(win, width=30, textvariable=jsonFile, )
jsonFileNameEntered.place(x=5, y=20)

# Search Label
ttk.Label(win, text="Search String:").place(x=5, y=45)

# Textbox Entry
name = tk.StringVar()
nameEntered = ttk.Entry(win, width=30, textvariable=name, )
nameEntered.place(x=5, y=65)

# This button calls the SearchJSON function, passing in the value of the radioboxes for whether the results should be clustered or not
action = ttk.Button(win, width=30, text="Search String")
action.place(x=5, y=90)

actionRegex = ttk.Button(win, width=30, text="Regex Search",
                         )
actionRegex.place(x=5, y=115)

actionDate = ttk.Button(win, width=30, text="Search Date [YYYY-MM-DD]",
                        )
actionDate.place(x=5, y=140)

# Using a scrolled Text control
scrolW = 84
scrolH = 30
scr = scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD, background="#f0f0f0")
scr.place(x=200, y=1)

# Search Limit Label
ttk.Label(win, text="Search Limit:").place(x=10, y=175)

# Textbox Entry Search Limit
searchLimit = tk.StringVar()
searchLimitEntry = ttk.Entry(win, width=15, textvariable=searchLimit, )
searchLimitEntry.place(x=95, y=173)

# Search Label Beer
ttk.Label(win, text="Search Template:").place(x=40, y=200)

# Note: Using a Lambda function to avoid triggering the command when creating the button and calling the SearchTemplate argument with an array of words to search for as well as the radiobox value
# Beers Template
action = ttk.Button(win, width=30, text="Beers",
                    )
action.place(x=5, y=220)

action = ttk.Button(win, width=30, text="University",
                    )
action.place(x=5, y=245)

action = ttk.Button(win, width=30, text="Gym",
                    )
action.place(x=5, y=270)

# Adding radio boxes for toggling clustered markers
clusterOnButton = Radiobutton(win, text="Clustered Markers", value=1)
clusterOnButton.place(x=5, y=300)
clusterOffButton = Radiobutton(win, text="Individual Markers", value=0)
clusterOffButton.place(x=5, y=325)

# Show Heatmap Button
loadingJsonButton = ttk.Button(win, width=30, text=" Show Plotted Search Heatmap ")
loadingJsonButton.place(x=5, y=350)

# Show Normal Map Button
loadingJsonButton = ttk.Button(win, width=30, text=" Show Plotted Search Results ")
loadingJsonButton.place(x=5, y=375)

# Clear Console Button
clearButton = ttk.Button(win, width=30, text=" Clear Console ")
clearButton.place(x=5, y=400)

# Place cursor into name Entry
nameEntered.focus()

# Start GUI
win.mainloop()
