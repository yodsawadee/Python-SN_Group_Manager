import sys
from PySide.QtCore import*
from PySide.QtGui import*
from PySide.QtUiTools import*
import os
import time

display_width = 800
display_height = 600
center = ((1366-display_width)/2,(768-display_height)/2)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % center

#Pictures
bill_bg = QImage('images/bill_bg.png')
bg = QImage('images/bg.png')

title_font_img = QImage('images/title_font.png')
title_font_width = 543

building_img = QImage('images/SNGroupBuilding.jpg')





