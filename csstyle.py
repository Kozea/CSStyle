#!/usr/bin/python
import os
import sys
import optparse
import copy

import csstyle

# Get command-line options
parser = optparse.OptionParser(usage= 'csstyle file [file[..]] [options]')
parser.add_option(
    "-b", "--browser", action="append",
    dest="browser",
    help="select specific browser engine")
options, args = parser.parse_args()

if not options.browser:
    options.browser = csstyle.BROWSERS

for option in args:
    parser = csstyle.Parser(option)
    for engine in options.browser:
        browser_parser= getattr(csstyle, engine)
        print(browser_parser.transform(copy.deepcopy(parser), 
                                       keep_existant=False))