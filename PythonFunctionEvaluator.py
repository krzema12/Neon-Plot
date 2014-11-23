# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

from math import *


class PythonFunctionEvaluator(object):
    not_a_number = float("nan")

    def __init__(self):
        self.function_string = ""
        self.can_be_drawn = False  # when the function is empty or invalid
        self.errors = None
        self.x = 0

    def __validate(self):
        self.can_be_drawn = False
        self.errors = None

        if self.function_string == "":
            return

        try:
            val = self.__evaluate()

            if type(float(val)) is not float:
                return
        except (SyntaxError, AttributeError, NameError) as ex:
            self.errors = ex
            return
        except Exception as e:  # unknown error
            print e
            return

        self.can_be_drawn = True
        self.errors = None

    def set_function(self, string):
        self.function_string = string
        self.__validate()
        print self.can_be_drawn

    def evaluate(self, x_param):
        try:
            self.x = x_param
            result = self.__evaluate()
            return result
        except (ZeroDivisionError, ValueError):
            return self.not_a_number

    def __evaluate(self):
            x = self.x
            result = eval(self.function_string, globals(), locals())
            return result