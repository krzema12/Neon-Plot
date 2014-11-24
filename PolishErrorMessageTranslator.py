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

    if type(error) is SyntaxError:
        return "Błąd: coś jest nie tak ze składnią w linii " + str(error.lineno)\
               + ", przy znaku nr " + str(error.offset) + "!"

    print '!!! nie wiem jak przetłumaczyć: ' + message + '!!!'
    return "Nieznany błąd!"