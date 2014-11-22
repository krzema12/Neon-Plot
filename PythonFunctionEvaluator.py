# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import math


class PythonFunctionEvaluator(object):
    not_a_number = float("nan")

    def __init__(self):
        self.function_string = ""
        self.can_be_drawn = False  # when the function is empty or invalid
        self.errors = None
        self.x = 0

    def __validate(self):
        if self.function_string == "":
            self.can_be_drawn = False
            self.errors = None
            return

        try:
            self.__evaluate()
        except (SyntaxError, AttributeError) as ex:
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