koala-desktop-interface
=======================

*Everything is subject to change at this moment**

Introduction
------------
This desktop interface utilize a couple of python components
- virtualenv
- pyserial
- minimalModBus
- PyQt4
- sip
- twisted

Prerequisite
------------
For development, Qt4 is required so it will have to be installed. I not sure if Qt4 is needed if it's just for deployment
*at the moment*.

The setup script should be able to take care of most dependencies. **However**, PyQt4 and SIP will need to be installed
manually since they are not available to pip or easy_install. **Note** that SIP need to be installed before PyQt4([Link]
(http://pyqt.sourceforge.net/Docs/PyQt4/installation.html)).

Setup
-----
1. Install SIP and PyQt4 (*instruction stub*)
2. create virtual environment
3. run setup.py

(Detail will be updated later)