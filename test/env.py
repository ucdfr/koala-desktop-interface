__author__ = 'yilu'
'''
Allow test scripts to find their modules!
Originally from Stack Overflow: http://stackoverflow.com/questions/61151/where-do-the-python-unit-tests-go
'''

import sys
import os

# append module root directory to sys.path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)