=============================
CSS New Features for Everyone
=============================

Presentation
============

CSStyle is an easy-to-use CSS converter for browsers using Gecko, Presto or
Webkit engines. It converts CSS values which are experimental in those
engines. It is mainly used for CSS3 new features.

From:

.. code-block:: css

  div {
     border-radius: 1em;
     transition-duration: 1s;
  }

To:

.. code-block:: css

  div {
     border-radius: 1em;
     -webkit-border-top-left-radius: 1em;
     -webkit-border-top-right-radius: 1em;
     -webkit-border-bottom-right-radius: 1em;
     -webkit-border-bottom-left-radius: 1em;
     transition-duration: 1s;
     -moz-transition-duration: 1s;
     -webkit-transition-duration: 1s;
  }


Technical Description
=====================

CSStyle is a very light project with no software dependencies and no
configuration. It can be used as a Python library or as an executable.

CSStyle Project runs on most of the UNIX-like platforms (Linux, \*BSD, MacOS X)
and Windows. It is free and open-source software, written in Python, released
under GPL version 3.


Supported Browsers
==================

- Based on Webkit: Chrome, Safari, Epiphany, Midori, etc.
- Based on Gecko: Firefox, SeaMonkey, Camino, etc.
- Based on Presto: Opera
