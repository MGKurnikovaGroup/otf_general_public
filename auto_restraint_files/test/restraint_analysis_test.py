import sys
import os
import pytest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from restraint_analysis import *

#ChatGPT
def almost_equal(a, b, places=3):
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
    assert(almost_equal(get_angle(1,1,1), 1.047))
    assert(almost_equal(get_angle(1,1,1), 1.047))
    with pytest.raises(ValueError, match="Invalid triangle sides"):
        get_angle(1, 2, 3)
    with pytest.raises(ValueError, match="Side lengths cannot be zero"):
        get_angle(0, 3, 4)
    print('get_angle passed')
    
test_get_angle()