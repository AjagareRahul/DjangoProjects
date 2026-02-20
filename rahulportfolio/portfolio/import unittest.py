import unittest

from rahulportfolio.portfolio import unit


def divide(a,b):
        if b==0:
            raise ValueError("Cannot divide only zero")
        return a/b
class Testdivide(unit.TestCase):
    def test_divide_zero(self):
        self.assertRaises(ValueError,divide,10,0)
        
if __name__ == "__main__":unittest.main()
