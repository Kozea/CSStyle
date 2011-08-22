====================
 User Documentation
====================

:Author: Hugo Pastore

:Date: 2010-08-02

:Abstract: This document is a short description for end-user installation and 
  usage of CSStyle.

.. contents::

Installation
============

Dependencies
------------

CSStyle is written in pure python and does not depend on any librabry. It is
known to work on Python from 2.5 to 3.2.

Linux users certainly have Python already installed. For Windows and MacOS
users, please install Python [#]_ thanks to the adequate installer.

.. [#] `Python download page <http://python.org/download/>`_.

CSStyle
-------

CSStyle can be freely downloaded on the `project website, download section
<http://www.csstyle.org/download>`_. Just get the file and unzip it in a
folder of your choice.

You can install it by running ``setup.py``.

On Linux::
  
  python setup.py install

CSStyle is also available with distutils, if you have it you can also install it 
with::

  pip install csstyle

Simple Usage
============

To create CSS pages, just run csstyle.py with python or use the following line::

  csstyle FILE [FILE...] [options]

For example::

  csstyle style.css style2.css -b webkit -b gecko

Advanced Usage with Python Server
=================================

If you want to use CSStyle on your python server, you can simply install csstyle
from pip and then use it as a module:
  
.. code-block:: python

  import csstyle

  for browser in csstyle.BROWSERS:
      parser = csstyle.Parser(text="a { transition: 1s }")
      browser_parser = getattr(csstyle, browser)
      print(browser_parser.transform(parser, keep_existant=False))

Have a look at ``csstyle.py`` for more technical details.
