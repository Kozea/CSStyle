# coding: utf8
import sys
import os
import doctest

try:
    import unittest2 as unittest
except ImportError:
    import unittest
    
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
TEST_PACKAGES = ['test']

def make_suite(names=None):
    """Build a test suite.
    
    Build a test suite each from each package, module, 
    test case class or method name.
    
    """
    suite = unittest.TestSuite()
    for name in TEST_PACKAGES:
        loader = unittest.TestLoader()
        suite.addTest(loader.discover(name, '*.py', PROJECT_DIR))    
    
    return suite

def run_suite(suite, verbose):
    """
    Run test suite & report test results on the standard error stream by default
    """
    unittest.installHandler()
    
    verbosity = 2 if verbose else 1
    unittest.TextTestRunner(buffer=True, verbosity=verbosity).run(suite)

def main():
    args = sys.argv[1:]
    verbose = '-v' in args
    if verbose:
        args.remove('-v')
    run_suite(make_suite(args), verbose)