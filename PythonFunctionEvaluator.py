# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import math


class PythonFunctionEvaluator(object):
    not_a_number = float("nan")

    def __init__(self):
        self.functionString = ""
        self.arguments = {'x': lambda: 0}

    def validate(self):
        if self.functionString == "":
            return None

        try:
            self.__evaluate()
        except SyntaxError as se:
            return se

    def set_function(self, string):
        self.functionString = string;

    def evaluate(self, x_param):
        try:
            self.arguments['x'] = x_param
            result = self.__evaluate()
            return result
        except (ZeroDivisionError, ValueError):
            return self.not_a_number

    def __evaluate(self):
            result = eval(self.functionString, globals(), self.arguments)
            return result