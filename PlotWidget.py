# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import gtk
import copy
import gobject
import math
from math import log10
from gtk import gdk


class Point:

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x*other.x, self.y*other.y)
        elif isinstance(other, float):
            return Point(self.x*other, self.y*other)

    def __div__(self, other):
        if isinstance(other, Point):
            return Point(self.x/other.x, self.y/other.y)
        elif isinstance(other, float):
            return Point(self.x/other, self.y/other)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self):
        return '(' + str(round(self.x, 5)) + ', ' + str(round(self.y, 5)) + ')'


def round_to_nearest(x, base=5):
    return int(base * math.ceil(float(x)/base))


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump


class PlotWidget(gtk.DrawingArea):

    SCROLL_RATIO = 1.2

    __gsignals__ = {
        'view_updated': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
    }

    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.connect("expose-event", self.expose)
        self.connect("motion_notify_event", self.motion_notify_event)
        self.connect("enter_notify_event", self.enter_notify_event)
        self.connect("leave_notify_event", self.leave_notify_event)
        self.connect("scroll_event", self.mouse_scroll)
        self.connect("button-press-event", self.button_press_event)
        self.connect("button-release-event", self.button_release_event)
        self.set_events(self.get_events() | gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.ENTER_NOTIFY_MASK | gtk.gdk.SCROLL_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)

        self.functions = []
        self.center = Point(0.0, 0.0)
        self.scale = Point(100.0, 100.0)
        self.__calculate_grid_spacing()
        self.cursor_position = None
        self.cursor_position_before_dragging = None
        self.mouse_button_pressed = False
        self.area = gtk.gdk.Rectangle(0, 0, 0, 0)

        self.show_cursor = True
        self.show_gridlines = True

    def do_realize(self):
        gtk.DrawingArea.do_realize(self)

    def motion_notify_event(self, widget, event):
        self.cursor_position.x, self.cursor_position.y = event.x, event.y

        if self.mouse_button_pressed:
            self.center -= (self.cursor_position - self.cursor_position_before_dragging)*Point(1.0, -1.0)/self.scale
            self.cursor_position_before_dragging = copy.copy(self.cursor_position)

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

    def mouse_scroll(self, widget, event):
        z = self.to_plot_coordinates(self.cursor_position)
        g = z - self.center

        if event.direction == gdk.SCROLL_UP:
            g /= self.SCROLL_RATIO
        else:
            g *= self.SCROLL_RATIO

        self.center = z - g

        if event.direction == gdk.SCROLL_UP:
            self.scale *= self.SCROLL_RATIO
        else:
            self.scale /= self.SCROLL_RATIO

        self.__calculate_grid_spacing()
        print self.gridSpacing
        self.update_view_info()
        self.queue_draw()

        return True

    def __calculate_grid_spacing(self):
        self.gridSpacing = Point(pow(10, -math.floor(log10(self.scale.x) + 0.2) + 1),
                                 pow(10, -math.floor(log10(self.scale.y) + 0.2) + 1))

    def button_press_event(self, widget, args):
        self.cursor_position_before_dragging = copy.copy(self.cursor_position)
        self.mouse_button_pressed = True

    def button_release_event(self, widget, args):
        self.mouse_button_pressed = False

    def to_screen_coordinates(self, point):
        x = point - self.center
        y = x*self.scale
        return Point(self.area.width/2 + y.x, self.area.height/2 - y.y)

    def to_plot_coordinates(self, point):
        x = Point(point.x - self.area.width/2, -(point.y - self.area.height/2))
        y = x/self.scale
        return y + self.center

    def update_view_info(self):
        self.emit('view_updated')

    def draw_vertical_gridline(self, cr, lower_right, upper_left, spacing_multiplier=1):
        start_x = upper_left.x - (upper_left.x % (self.gridSpacing.x*spacing_multiplier))
        end_x = lower_right.x + (lower_right.x % (self.gridSpacing.x*spacing_multiplier))

        start_x = self.to_screen_coordinates(Point(start_x, 0)).x
        end_x = self.to_screen_coordinates(Point(end_x, 0)).x

        for x in frange(start_x, end_x, self.gridSpacing.x*spacing_multiplier*self.scale.x):
            cr.move_to(x + 0.5, 0.0)
            cr.line_to(x + 0.5, self.area.height)
            cr.stroke()

    def draw_horizontal_gridlline(self, cr, lower_right, upper_left, spacing_multiplier=1):
        start_y = lower_right.y - (lower_right.y % (self.gridSpacing.y*spacing_multiplier))
        end_y = upper_left.y - (upper_left.y % (self.gridSpacing.y*spacing_multiplier))

        start_y = self.to_screen_coordinates(Point(0, start_y)).y
        end_y = self.to_screen_coordinates(Point(0, end_y)).y

        for y in frange(end_y, start_y, self.gridSpacing.y*spacing_multiplier*self.scale.y):
            cr.move_to(0.0, y + 0.5)
            cr.line_to(self.area.width, y + 0.5)
            cr.stroke()

    def expose(self, widget, event):
        self.area = event.area
        cr = widget.window.cairo_create()

        # background
        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.paint()

        # grid ----------------------------------

        if self.show_gridlines:
            upper_left = self.to_plot_coordinates(Point(0, 0))
            lower_right = self.to_plot_coordinates(Point(self.area.width, self.area.height))

            # X grid (vertical lines)

            cr.set_source_rgb(0.25, 0.25, 0.25)
            cr.set_line_width(0.5)
            self.draw_vertical_gridline(cr, lower_right, upper_left)

            cr.set_source_rgb(0.25, 0.25, 0.25)
            cr.set_line_width(2.0)
            self.draw_vertical_gridline(cr, lower_right, upper_left, 10)

            # Y grid (horizontal lines)

            cr.set_source_rgb(0.25, 0.25, 0.25)
            cr.set_line_width(0.5)
            self.draw_horizontal_gridlline(cr, lower_right, upper_left)

            cr.set_source_rgb(0.25, 0.25, 0.25)
            cr.set_line_width(2.0)
            self.draw_horizontal_gridlline(cr, lower_right, upper_left, 10)

        # axes ----------------------------------

        center_on_screen = self.to_screen_coordinates(Point(0, 0))
        cr.set_source_rgb(0.75, 0.75, 0.75)

        # Y axis
        cr.set_line_width(2.0)
        cr.move_to(center_on_screen.x + 0.5, 0.0)
        cr.line_to(center_on_screen.x + 0.5, self.area.height)
        cr.stroke()

        # X axis
        cr.set_line_width(2.0)
        cr.move_to(0.0, center_on_screen.y + 0.5)
        cr.line_to(self.area.width, center_on_screen.y + 0.5)
        cr.stroke()

        # squares (for testing purposes)

        z = self.to_screen_coordinates(Point(0.0, 0.0))
        cr.set_source_rgb(0, 128, 0)
        cr.set_line_width(2.0)
        cr.rectangle(z.x, z.y, 6, 6)
        cr.fill()

        t = self.to_screen_coordinates(Point(1.0, 1.0))
        cr.set_source_rgb(1.0, 0, 0)
        cr.set_line_width(2.0)
        cr.rectangle(t.x, t.y, 6, 6)
        cr.fill()

        t = self.to_screen_coordinates(Point(-4.0, 2.0))
        cr.set_source_rgb(0.5, 0.5, 1.0)
        cr.set_line_width(2.0)
        cr.rectangle(t.x, t.y, 6, 6)
        cr.fill()

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
