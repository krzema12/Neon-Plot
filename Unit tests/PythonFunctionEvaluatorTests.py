# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import unittest
from PythonFunctionEvaluator import PythonFunctionEvaluator


class PythonFunctionEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = PythonFunctionEvaluator()

    def test_validate_EmptyFunctionString_ShouldReturnNone(self):
        result = self.evaluator.validate()
        self.assertEquals(result, None)

    def test_validate_SimpleConstantFunction_ShouldReturnNone(self):
        result = self.evaluator.set_function("3.5")
        self.assertEquals(result, None)

    def test_evaluate_SimpleConstantFunctionAndAnyArgument_ShouldReturnValue(self):
        self.evaluator.set_function("3.5")
        result = self.evaluator.evaluate(53)
        self.assertEquals(result, 3.5)

if __name__ == '__main__':
    unittest.main()