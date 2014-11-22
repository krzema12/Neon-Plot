# -*- coding: UTF-8 -*-
# !/usr/bin/env python
__author__ = 'Piotr Krzemiński'

import gtk
import gobject
from PlotWidget import PlotWidget


class NeonPlot:
    def __init__(self):
        filename = "MainWindow.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)

        window = builder.get_object("mainWindow")
        window.connect("destroy", self.onDeleteWindow)
        window.show_all()

        self.functions = []

        self.functionsVbox = builder.get_object("functionsVbox")
        self.addFunctionButton = builder.get_object("addFuncitonButton")

        self.viewParamsStatusBar = builder.get_object('viewParamsLabel')

        self.eventbox1 = builder.get_object("eventbox1")
        plotWidget = PlotWidget()
        plotWidget.connect('view_updated', self.update_plotview_status_bar)
        plotWidget.update_view_info()
        plotWidget.show()
        self.eventbox1.add(plotWidget)

        # test = builder.get_object("eventbox1")
        #test.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#FF8"))

        #entry = builder.get_object("entry1")
        #entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color("#F88"))

    def update_plotview_status_bar(self, widget):
        self.viewParamsStatusBar.set_text('Widok: ' + str(widget.center) + ', X: ' + str(round(widget.scale.x, 5))
                                          + ' px/j, Y: ' + str(round(widget.scale.y, 5)) + ' px/j')

    def addFunction(self, widget):
        # creating a new GtkEventBox
        eventBox = gtk.EventBox()
        eventBox.show()

        # creating a new GtkFixed and setting its height
        fixed = gtk.Fixed()
        fixed.show()
        fixed.set_size_request(-1, 60)

        # creating a new "x" button
        removeButton = gtk.Button()
        removeButton.show()
        removeButton.set_size_request(18, 18)
        removeButton.set_label("x")
        removeButton.connect("clicked", self.removeFunction, eventBox)
        fixed.put(removeButton, 222, 2)

        # creating a new text field
        textField = gtk.Entry()
        textField.show()
        textField.set_size_request(230, 27)
        fixed.put(textField, 10, 23)

        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#0F0"))

        # adding the event box as a child of the functionsVbox
        eventBox.add(fixed)
        self.functionsVbox.pack_start(eventBox, False, True, 1)

        # move the function adding button to the end of the Vbox
        self.functionsVbox.reorder_child(self.addFunctionButton, -1)

        print self.functions

    def removeFunction(self, widget, arg):
        self.functionsVbox.remove(arg)

    def onDeleteWindow(self, *args):
        gtk.main_quit(*args)

if __name__ == "__main__":
    gobject.type_register(PlotWidget)
    neonPlot = NeonPlot()
    gtk.main()