# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'


class PythonFunctionEvaluator(object):

    def __init__(self):
        self.functionString = ""

    def validate(self):
        if self.functionString == "":
            return None

    def set_function(self, string):
        self.functionString = string;

    def evaluate(self, xParam):
        x = xParam
        result = eval(self.functionString)
        return result