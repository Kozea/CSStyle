# coding: utf8
import sys
import os
import unittest2
import doctest

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
TEST_PACKAGES = ['test']

def make_suite(names=None):
    """Build a test suite.
    
    Build a test suite each from each package, module, 
    test case class or method name.
    
    """
    suite = unittest2.TestSuite()
    for name in TEST_PACKAGES:
        loader = unittest2.TestLoader()
        suite.addTest(loader.discover(name, '*.py', PROJECT_DIR))    
    
    return suite

def run_suite(suite, verbose):
    """
    Run test suite & report test results on the standard error stream by default
    """
    unittest2.installHandler()
    
    verbosity = 2 if verbose else 1
    unittest2.TextTestRunner(buffer=True, verbosity=verbosity).run(suite)

def main():
    args = sys.argv[1:]
    verbose = '-v' in args
    if verbose:
        args.remove('-v')
    run_suite(make_suite(args), verbose)