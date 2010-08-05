# coding: utf8

import os
from unittest2 import TestCase
import copy
from difflib import Differ
from pprint import pprint

import csstyle

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data')
TEST_FILE = os.path.join(DATA_FILE, 'test.css')

def ignore_characters(unstripped_string):
    new_string = unstripped_string.splitlines()
    for element in new_string:
        element = element.strip(' \r\n\t')
        if element:
            yield element
 
def test_helper(self,keep_existant=False, browser=csstyle.BROWSERS):
    """ Test function called by all tests methods """
    string = ("/* Generated by CSStyle */\n\n")
    parser = csstyle.Parser(TEST_FILE)
    for engine in browser:
        browser_parser = getattr(csstyle, engine)
        string +=  repr(browser_parser.transform(copy.deepcopy(parser), 
                        keep_existant))
    string = list(ignore_characters(string))
    
    # define to be compared filename
    name = ''
    if keep_existant:
        name = 'keep_'
    if browser == csstyle.BROWSERS:
        name += 'result_all.css'
    else:
        name += 'result_%s.css' % browser[0]
    string_to_compare = list(ignore_characters(open(os.path.join(DATA_FILE, 
                                          name)).read()))
    self.assertEqual(string_to_compare, string)

class CSStyleTestCase(TestCase):
  
    def test_parser_all(self):
        """ Tests new lines only with all browsers at once """
        test_helper(self)
        
    def test_parser_webkit(self):
        """ Tests new lines only with webkit only """
        test_helper(self, browser=('webkit', ))
        
    def test_parser_gecko(self):
        """ Tests new lines only with webkit gecko """
        test_helper(self, browser=('gecko', ))
        
    def test_parser_presto(self):
        """ Tests new lines only with presto only """
        test_helper(self, browser=('presto', ))
        
    def test_keep_parser_all(self):
        """ Tests old and new lines with all browsers """
        test_helper(self, True)
        
    def test_keep_parser_webkit(self):
        """ Tests old and new lines with webkit only """
        test_helper(self, True, ('webkit', ))
        
    def test_keep_parser_gecko(self):
        """ Tests old and new lines with gecko only """
        test_helper(self, True, ('gecko', ))
        
    def test_keep_parser_presto(self):
        """ Tests old and new lines with presto only """
        test_helper(self, True, ('presto', ))