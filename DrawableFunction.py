# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

from PlotWidget import *


class DrawableFunction(object):

    def __init__(self):
        self.function_evaluator = PythonFunctionEvaluator()
        self.enabled = True
        self.color = ColorRGB(0.5, 0.5, 0.5)