# -*- coding: UTF-8 -*-
__author__ = 'Piotr Krzemiński'

import re

def translate_to_polish(error):
    message = str(error)

    if error is None:
        return "Ok."
    if message == "float() argument must be a string or a number":
        return "Błąd: wyrażenie nie zwraca liczby!"
    if str.startswith(message, "unexpected EOF while parsing"):
        return "Błąd: oczekiwano czegoś jeszcze na końcu kodu funkcji!"
    if message == "math domain error":
        return "Błąd: próbujesz narysować funkcję w przedziale wykraczającym poza jej dziedzinę (TODO)."

    match = re.match(r"name '([^']+)' is not defined", message, re.M | re.I)

    if match:
        function_name = match.group(1)
        return "Błąd: nie wiem co to jest '" + function_name + "'!"

    match = re.match(r"([^\(]+)\(\) takes exactly one argument \(([^\s]+) given\)", message, re.M | re.I)

    if match:
        function_name = match.group(1)
        how_much_arguments_given = match.group(2)
        return "Błąd: funkcja '" + function_name + "' przyjmuje 1 argument, a podano " + how_much_arguments_given + "!"

    match = re.match(r"([^\s]+) expected ([^\s]+) arguments, got ([^\s]+)", message, re.M | re.I)

    if match:
        function_name = match.group(1)
        how_much_arguments_expected = match.group(2)
        how_much_arguments_given = match.group(3)
        return "Błąd: funkcja '" + function_name + "' przyjmuje " + how_much_arguments_expected + " argumenty, a podano " + how_much_arguments_given + "!"

    match = re.match(r"'([^']+)' object is not callable", message, re.M | re.I)

    if match:
        type_name = match.group(1)
        return "Błąd: nie możesz wywołać obiektu/typu '" + type_name + "'!"

    if type(error) is SyntaxError:
        return "Błąd: coś jest nie tak ze składnią w linii " + str(error.lineno)\
               + ", przy znaku nr " + str(error.offset) + "!"

    print '!!! nie wiem jak przetłumaczyć: ' + message + '!!!'
    return "Nieznany błąd!"