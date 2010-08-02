===================
 Technical Choices
===================

:Author: Hugo Pastore

:Date: 2010-01-22

:Abstract: This document describes the global technical choices of the
 CSStyle Project and the global architectures of its different parts.

.. contents::

Global Technical Choices
========================

General Description
-------------------

The CSStyle Project aims to be easy to use. 
As a consequence, it doesn't need any software dependencies other than python.

The Radicale Project runs on most of the UNIX-like platforms (Linux,
\*BSD, MacOS X) and Windows. It is free and open-source software under GPLv3 
license.

Language
--------

The different parts of the CSStyle Project are written in
Python. This is a high-level language, fully object-oriented,
available for the main operating systems and released with a lot of
useful libraries.

Architectures
=============

General Architecture
--------------------

The project uses a Parser class to read CSS sheet which is uses by each transform()
function for each engine converter.
Then a new sheet is generated with modified values to be understood by those engines.