#!/usr/bin/env python
import gtk

class NeonPlot:
    
    def __init__(self):
        filename = "MainWindow.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)
        
        window = builder.get_object("mainWindow")
        window.connect("destroy", self.onDeleteWindow)
        window.show_all()
        
    def canvasExposeEvent(self, widget, event):
        cr = widget.window.cairo_create()
        
        # background
        cr.set_source_rgb(0, 0, 0)
        cr.paint()
        
        # lines
        cr.set_source_rgb(0, 128, 0)
        cr.set_line_width(2.0)
        cr.move_to(5, 5)
        cr.line_to(20, 50)
        cr.stroke()
        
        return True
    
    def onDeleteWindow(self, *args):
        gtk.main_quit(*args)

neonPlot = NeonPlot()
gtk.main()