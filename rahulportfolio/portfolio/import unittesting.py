import unittest

class Testcode(unittest.TestCase):

    def testupper(self):
        self.assertFalse('pYTHON'.isupper())

    def testlower(self):
        self.assertTrue('python'.islower())
        
    def testsplit(self):
        s = 'Rahul'
        
        self.assertEqual(s.split(), ['Rahul'])
        
        

if __name__ == "__main__":
    unittest.main()