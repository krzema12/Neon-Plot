# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import unittest
import math
from PythonFunctionEvaluator import PythonFunctionEvaluator


class PythonFunctionEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = PythonFunctionEvaluator()

    def test_set_function_EmptyFunctionString_CannotBeDrawnAndNoErrors(self):
        self.evaluator.set_function('')

        self.assertFalse(self.evaluator.can_be_drawn)
        self.assertEquals(self.evaluator.errors, None)

    def test_set_function_SimpleConstantFunction_CanBeDrawnAndNoErrors(self):
        self.evaluator.set_function("3.5")

        self.assertTrue(self.evaluator.can_be_drawn)
        self.assertEquals(self.evaluator.errors, None)

    def test_set_function_GenericSyntaxError_ShouldReturnInvalidSyntaxError(self):
        self.evaluator.set_function('2.4 + * 3.5')
        errors = self.evaluator.errors

        expected_exception = SyntaxError()
        expected_exception.lineno = 1
        expected_exception.offset = 7
        expected_exception.msg = 'invalid syntax'

        self.assertEquals(errors.lineno, expected_exception.lineno, 'line number is invalid')
        self.assertEquals(errors.offset, expected_exception.offset, 'offset is invalid')
        self.assertEquals(errors.msg, expected_exception.msg, 'message is invalid')

    def test_set_function_NonexistentFunctionUsed_ShouldReturnNoSuchFunctionError(self):
        self.evaluator.set_function("math.foobar(2)")
        errors = self.evaluator.errors

        self.assertEqual(errors.message, "'module' object has no attribute 'foobar'")
        # "'module' object has no attribute '[^']+'"

    def test_evaluate_SimpleConstantFunction_ShouldReturnValue(self):
        self.evaluator.set_function('3.5')
        result = self.evaluator.evaluate(53)

        self.assertEquals(result, 3.5)

    def test_evaluate_LinearFunction_ShouldReturnValue(self):
        self.evaluator.set_function("2*x + 3")
        result = self.evaluator.evaluate(4)

        self.assertEquals(result, 11)

    def test_evaluate_DivisionByXEqualToZero_ShouldReturnNotANumber(self):
        self.evaluator.set_function("1/x")
        result = self.evaluator.evaluate(0)

        self.assertTrue(math.isnan(result))

    def test_evaluate_XIsBeyondAllowedRange_ShouldReturnNotANumber(self):
        self.evaluator.set_function("math.log(x)")
        result = self.evaluator.evaluate(-2)

        self.assertTrue(math.isnan(result))



if __name__ == '__main__':
    unittest.main()