# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import gtk
from PlotWidget import ColorRGB


def color_from_gtk_to_float(gtk_color):
    return ColorRGB(gtk_color.red_float, gtk_color.green_float, gtk_color.blue_float)

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
        self.drawableFunction.color = color_from_gtk_to_float(color.get_current_color())
        self.plotWidget.queue_draw()
        self.eventBox.modify_bg(gtk.STATE_NORMAL, color.get_current_color())
