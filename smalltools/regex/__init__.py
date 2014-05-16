'''
A serial commonly regular expressions is listed below. It includes:
    * Regular float number, like ``1.0``, ``0.9``
    * Scientific float number, like ``1.0e4``
    * Float number with percentage, like ``93.75%``
'''
import re

# Used to match regular float number
# For example: -0.1
reFloatNumber = re.compile('[-+]?[0-9]*\.?[0-9]*')

reScientificFloatNumber = re.compile('[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?')

rePercentageFloatNumber = re.compile('[0-9]*\.?[0-9]*\%')

# It's extramely ugly but very helpful.
reURL = re.compile("((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)")

from generalize import Generalize
