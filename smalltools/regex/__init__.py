'''
A serial regular expression used to
'''
import re

# Used to match regular float number
# For example: -0.1
reFloatNumber = re.compile('[-+]?[0-9]*\.?[0-9]*')

reScientificFloatNumber = re.compile('[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?')

rePercentageFloatNumber = re.compile('[0-9]*\.?[0-9]*\%')
