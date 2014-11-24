# -*- coding: UTF-8 -*-
# !/usr/bin/env python
__author__ = 'Piotr Krzemiński'

import gtk
from PythonFunctionEvaluator import PythonFunctionEvaluator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from DrawableFunction import DrawableFunction
from ColorSelectionWindow import ColorSelectionWindow
from PlotWidget import PlotWidget
from ColorSelectionWindow import color_from_gtk_to_float
from PolishErrorMessageTranslator import translate_to_polish


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


class NeonPlot:
    def __init__(self):
        filename = "MainWindow.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)

        self.window = builder.get_object("mainWindow")
        self.window.connect("destroy", self.onDeleteWindow)
        self.window.show_all()

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

    def on_howToUse_activate(self, widget):
        filename = "HowToWindow.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)
        window = builder.get_object("howToWindow")
        window.show_all()

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

        return eventBox, textField, checkBox, drawableFunction

    def on_readFromFile_activate(self, widget):
        openDialog = gtk.FileChooserDialog('Wskaż plik, z którego mają zostać załadowane funkcje',
                                           self.window, gtk.FILE_CHOOSER_ACTION_OPEN,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        openDialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Pliki XML (*.xml)")
        filter.add_pattern("*.xml")
        openDialog.add_filter(filter)

        response = openDialog.run()

        if response == gtk.RESPONSE_OK:
            tree = ElementTree.parse(openDialog.get_filename())
            root = tree.getroot()

            for f in root:
                eventBox, textField, checkBox, drawableFunction = self.addFunction(None)

                color = f.find('color')

                gtkColor = gtk.gdk.Color(float(color.get('red')),
                                         float(color.get('green')),
                                         float(color.get('blue')))
                drawableFunction.color = color_from_gtk_to_float(gtkColor)
                eventBox.modify_bg(gtk.STATE_NORMAL, gtkColor)
                checkBox.set_active(f.get('active') == 'True')
                textField.set_text(f.find('code').text.strip())

        openDialog.destroy()

    def on_saveToFile_activate(self, widget):
        saveDialog = gtk.FileChooserDialog('Wskaż plik gdzie zapisać funkcje',
                                           self.window, gtk.FILE_CHOOSER_ACTION_SAVE,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                            gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        saveDialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Pliki XML (*.xml)")
        filter.add_pattern("*.xml")
        saveDialog.add_filter(filter)

        response = saveDialog.run()

        if response == gtk.RESPONSE_OK:
            functions = self.plotWidget.functions

            top = Element('functions')

            for f in functions:
                functionTag = SubElement(top, 'function')

                functionTag.set('active', str(f.enabled))

                colorTag = SubElement(functionTag, 'color')
                colorTag.set('red', str(f.color.r))
                colorTag.set('green', str(f.color.g))
                colorTag.set('blue', str(f.color.b))

                codeTag = SubElement(functionTag, 'code')
                codeTag.text = f.function_evaluator.function_string

            with open(saveDialog.get_filename(), 'w') as file:
                file.write(prettify(top))

        saveDialog.destroy()

    def on_clearList_activate(self, widget):
        self.plotWidget.functions = []

        for item in self.functionsVbox:
            if type(item) is gtk.EventBox:
                self.functionsVbox.remove(item)

    def on_zoomIn_activate(self, widget):
        self.plotWidget.zoom_in()

    def on_zoomOut_activate(self, widget):
        self.plotWidget.zoom_out()

    def on_reset_activate(self, widget):
        self.plotWidget.reset_view()
        self.plotWidget.queue_draw()

    def showOrHideFunction(self, checkBox, drawableFunction):
        drawableFunction.enabled = checkBox.get_active()
        self.plotWidget.queue_draw()

    def editFunction(self, entry, drawableFunction):
        newText = entry.get_text()
        drawableFunction.function_evaluator.set_function(newText)

        entry.modify_base(gtk.STATE_NORMAL,
                          gtk.gdk.Color("#FFF"
                                        if drawableFunction.function_evaluator.can_be_drawn or newText
                                        is "" else "#F66"))
        self.errorsStatusBar.set_text(translate_to_polish(drawableFunction.function_evaluator.errors))

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