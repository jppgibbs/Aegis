# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\User Files\Downloads\AegisGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.lang import Builder
# import aegis
import os
import subprocess
cmd = 'python aegis.py --pot aegisec.pot --domain aegisec.me'
meme = os.system(cmd)

root = Builder.load_string(r'''

ScrollView:

    Label:

        text: '''+meme.toString()+'''

        font_size: 30

        size_hint_x: 1.0

        size_hint_y: None

        text_size: self.width, None

        height: self.texture_size[1]

''')
class MyApp(App):
    def build(self):
        return Label(text='Hello world')

if __name__ == '__main__':
    import sys
    runTouchApp(root)
    #MyApp().run()
    currentDir = os.getcwd()


