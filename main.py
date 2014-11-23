# -*- coding: UTF-8 -*-
# !/usr/bin/env python
__author__ = 'Piotr Krzemiński'

import gtk
from PythonFunctionEvaluator import PythonFunctionEvaluator
from DrawableFunction import DrawableFunction
from ColorSelectionWindow import ColorSelectionWindow
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

        self.functionsVbox = builder.get_object("functionsVbox")
        self.addFunctionButton = builder.get_object("addFuncitonButton")

        self.viewParamsStatusBar = builder.get_object('viewParamsLabel')
        self.errorsStatusBar = builder.get_object('errorsLabel')

        self.eventbox1 = builder.get_object("eventbox1")
        self.plotWidget = PlotWidget()
        self.plotWidget.connect('view_updated', self.update_plotview_status_bar)
        self.plotWidget.update_view_info()
        self.plotWidget.show()
        self.eventbox1.add(self.plotWidget)

        #self.viewCursorMenuItem = builder.get_object('viewCursor')
        #self.viewCursorMenuItem.connect("toggled", self.viewCursor_toggled_cb)

        # test = builder.get_object("eventbox1")
        #test.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#FF8"))

    def update_plotview_status_bar(self, widget):
        self.viewParamsStatusBar.set_text('Środek: ' + str(widget.center) + ', skala: ' + str(widget.scale) + ' px/j')

    def viewCursor_toggled_cb(self, widget):
        self.plotWidget.show_cursor = widget.active

    def viewGridlines_toggled_cb(self, widget):
        self.plotWidget.show_gridlines = widget.active

    def open_about_window_cb(self, widget):
        filename = "AboutWindow.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)
        window = builder.get_object("aboutWindow")
        window.show_all()

    def addFunction(self, widget):

        # DrawableFunction
        drawableFunction = DrawableFunction()
        self.plotWidget.add_function(drawableFunction)

        # GtkEventBox (will contain all elements)
        eventBox = gtk.EventBox()
        eventBox.show()

        # GtkFixed and setting its height
        fixed = gtk.Fixed()
        fixed.show()
        fixed.set_size_request(-1, 60)

        # "x" button
        removeButton = gtk.Button()
        removeButton.show()
        removeButton.set_size_request(45, 21)
        removeButton.set_label('usuń')
        removeButton.connect("clicked", self.removeFunction, drawableFunction, eventBox)
        fixed.put(removeButton, 197, 2)

        # "choose color" button
        changeColorButton = gtk.Button()
        changeColorButton.show()
        changeColorButton.set_size_request(73, 21)
        changeColorButton.set_label('zmień kolor')
        changeColorButton.connect("clicked", self.changeColor, drawableFunction, eventBox)
        fixed.put(changeColorButton, 120, 2)

        # text field
        textField = gtk.Entry()
        textField.show()
        textField.set_size_request(230, 27)
        textField.connect('changed', self.editFunction, drawableFunction)
        fixed.put(textField, 10, 23)

        # "draw' checkbox
        checkBox = gtk.CheckButton()
        checkBox.show()
        checkBox.set_size_request(70, 27)
        checkBox.set_label('aktywna')
        checkBox.set_active(True)
        checkBox.connect('toggled', self.showOrHideFunction, drawableFunction)
        fixed.put(checkBox, 10, 0)

        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#CCCCCC"))

        # adding the event box as a child of the functionsVbox
        eventBox.add(fixed)
        self.functionsVbox.pack_start(eventBox, False, True, 1)

        # move the function adding button to the end of the Vbox
        self.functionsVbox.reorder_child(self.addFunctionButton, -1)

        # placing cursor in the newly added Entry
        textField.grab_focus()

    def showOrHideFunction(self, checkBox, drawableFunction):
        drawableFunction.enabled = checkBox.get_active()
        self.plotWidget.queue_draw()

    def editFunction(self, entry, drawableFunction):
        newText = entry.get_text()
        drawableFunction.function_evaluator.set_function(newText)

        entry.modify_base(gtk.STATE_NORMAL,
                          gtk.gdk.Color("#FFF" if drawableFunction.function_evaluator.can_be_drawn else "#F66"))
        self.errorsStatusBar.set_text(str(drawableFunction.function_evaluator.errors))

        self.plotWidget.queue_draw()

    def changeColor(self, button, drawableFunction, eventBox):
        csw = ColorSelectionWindow(self.plotWidget, drawableFunction, eventBox)
        csw.show_window()

    def removeFunction(self, widget, drawableFunction, eventBox):
        self.plotWidget.functions.remove(drawableFunction)
        self.functionsVbox.remove(eventBox)
        self.plotWidget.queue_draw()

    def onDeleteWindow(self, *args):
        gtk.main_quit(*args)

if __name__ == "__main__":
    neonPlot = NeonPlot()
    gtk.main()