# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import gtk


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class PlotWidget(gtk.DrawingArea):

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose-event", self.expose)
        self.connect("motion_notify_event", self.motion_notify_event)
        self.connect("enter_notify_event", self.enter_notify_event)
        self.connect("leave_notify_event", self.leave_notify_event)
        self.set_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.ENTER_NOTIFY_MASK)

        self.functions = []
        self.show_cursor = True
        self.cursor_position = None
        self.area = gtk.gdk.Rectangle(0, 0, 0, 0)

    def do_realize(self):
        gtk.DrawingArea.do_realize(self)

    def motion_notify_event(self, widget, event):
        self.cursor_position.x, self.cursor_position.y = event.x, event.y
        self.queue_draw()
        return True

    def enter_notify_event(self, widget, event):
        self.cursor_position = Point(event.x, event.y)
        self.queue_draw()
        return True

    def leave_notify_event(self, widget, event):
        self.cursor_position = None
        self.queue_draw()
        return True

    def expose(self, widget, event):
        self.area = event.area
        cr = widget.window.cairo_create()

        # background
        cr.set_source_rgb(0, 0, 0)
        cr.paint()

        # lines
        cr.set_source_rgb(0, 128, 0)
        cr.set_line_width(2.0)
        cr.move_to(0, 0)
        cr.line_to(event.area.width, event.area.height)
        cr.stroke()

        # cursor
        if self.show_cursor is True and self.cursor_position is not None:
            cr.set_source_rgb(0.5, 0.5, 0.5)
            cr.set_dash({5.0, 5.0})
            cr.set_line_width(1.0)

            cr.move_to(self.cursor_position.x + 0.5, 0.0)
            cr.line_to(self.cursor_position.x + 0.5, self.area.height)

            cr.move_to(0, self.cursor_position.y + 0.5)
            cr.line_to(self.area.width, self.cursor_position.y + 0.5)
            cr.stroke()

        return True
