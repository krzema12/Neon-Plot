# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import gtk
from PlotWidget import ColorRGB


def color_from_hex_to_float(color_as_string):
    color_as_string = color_as_string.replace('#', '0x', 1)
    color_as_int = int(color_as_string, 16)

    blue = float(color_as_int % 65536)/65535
    color_as_int /= 65536
    green = float(color_as_int % 65536)/65535
    color_as_int /= 65536
    red = float(color_as_int % 65536)/65535

    return ColorRGB(red, green, blue)

class ColorSelectionWindow:

    def __init__(self, plotWidget, drawableFunction, eventBox):
        self.plotWidget = plotWidget
        self.drawableFunction = drawableFunction
        self.eventBox = eventBox

        filename = "ColorSelectionWindow.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)

        self.window = builder.get_object("colorSelectionWindow")

    def show_window(self):
        self.window.show_all()

    def on_colorSelector_color_changed(self, color):
        currentColor = str(color.get_current_color())
        self.drawableFunction.color = color_from_hex_to_float(currentColor)
        self.plotWidget.queue_draw()
        self.eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(currentColor))
