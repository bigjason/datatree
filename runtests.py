import unittest
from os import path
import sys

if __name__ == "__main__":
    current_folder = path.dirname(__file__)
    base_folder = path.join(current_folder, "datatree")
    
    sys.path.insert(0, current_folder)
    
    suite = unittest.TestSuite()
    loader = unittest.loader.defaultTestLoader
    suite.addTest(loader.discover(base_folder, pattern="test*.py"))
    runner = unittest.TextTestRunner()
    runner.verbosity = 2
    runner.run(suite.run)
