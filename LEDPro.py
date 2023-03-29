#-*- coding: utf-8 -*-

import time, datetime
import numpy as np
from PyQt5 import QtCore, QtGui
from blinkt import DAT, CLK, set_pixel, show


class LedBr(QtCore.QThread):
    def __init__(self, parent=None):
        super(LedBr, self).__init__(parent)
        self.Working = True
        self.mainWindow = parent

        self.input = False
        self.data = 0
        self.LED_bar_color = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 255, 0], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 255, 0], [0, 255, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 255, 0], [0, 255, 0], [255, 0, 0], [255, 0, 0], [0, 0, 0]],
                              [[0, 0, 255], [0, 0, 255], [0, 0, 255], [0, 255, 0], [0, 255, 0], [255, 0, 0], [255, 0, 0], [255, 0, 0]]]

    def run(self):
        while self.Working:
                for i in range(8):
                    set_pixel(i, self.LED_bar_color[self.data][i][0], self.LED_bar_color[self.data][i][1],
                              self.LED_bar_color[self.data][i][2])
                show()
                #time.sleep(0.05)
                self.input = False
                time.sleep(0.0001)
    def wr(self, data):
        self.data = data
        #self.input = True