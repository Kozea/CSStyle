=====================
 Project Description
=====================

:Author: Hugo Pastore

:Date: 2010-01-22

:Abstract: This document defines the main goals of the CSStyle
 Project, what it covers and what it does not.

.. contents::

Main Goals
==========

The CSStyle Project has for only goal to avoid putting conditions in CSStyle to work
with every browser engines. As differences are always the same, it can be auto generated.
This is what CSStyle does.


What CSStyle Is
===============

Experimental CSS Values conversion
----------------------------------

CSStyle only converts values which are experimental in engines. As those values
might not be experimental any more in the future and new ones become available,
CSStyle ought to be updated often.
CSStyle supports Gecko (Firefox), Webkit (Chrome, Safari, Epiphany) and Presto (Opera).
There is currently no experimental CSS in Trident (IE8).
CSStyle understands @import and multiple level CSS.

What CSStyle will Be
====================

Likely evolution
----------------

IE9 is supposed to have an improved CSS3 understanding. In that case IE9 engine
will be supported by CSStyle.

Ultimate evolution
------------------

The global aim of this project is to be the more easy to use as possible.
So an online user interface may be implemented in further versions.

What CSStyle Is not and will not Be
===================================

Specific CSS issue
------------------

CSStyle is used to generate CSS automatically, there will be no management of
specific cases or CSS check for browsers.
