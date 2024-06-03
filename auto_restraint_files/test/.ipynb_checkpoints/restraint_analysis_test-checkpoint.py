import sys
import os
import unittest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from restraint_analysis import *

#ChatGPT
def almost_equal(a, b, places=7):
    """
    Custom function to check if two floating-point numbers are almost equal.
    :param a: First floating-point number
    :param b: Second floating-point number
    :param places: Number of decimal places to consider
    :return: True if the numbers are almost equal, False otherwise
    """
    return round(abs(a - b), places) == 0

#get_angle
def test_get_angle():
    assert(almost_equal(get_angle(1,1,1), 1.047, 3))
    assert(almost_equal(get_angle(1,2,3), 0, 3))

    print('get_angle passed')
    
test_get_angle()