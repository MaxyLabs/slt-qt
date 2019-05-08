# slt-qt

# Simple Login Tool

This application makes it easier to search for a specific hostname in a predefined csv file and open a new terminal window for it.
It is written in Python using PySide and Qt.

![Screenshot](/slt-qt-screenshot.png "Screenshot")

# Prerequisites
## Linux

``
$ dnf install python3-pyside
``

## macOS

``
$ brew install pyside
``

# Usage

``
$ python ./slt-qt.py
``

# How-To
**How to issue the connect.sh for a specific row?**
- Double click on a row
- Use the text filed to sort the list to just one item and push the Connect button

**How to change which parameters are passed to the connect.sh?**
- Modify this line: self.connectParamList = [4, 2]
- The default value is [4, 2] which means that it passes the 4th and 2nd column

**How to change the Table Header Names?**
- Modify this line: self.columnHeaders = ['Application', 'Version', 'ENV', 'Hostname', 'FQDN']

**How to change column is connected to colorizing the table records?**
- Modify this line: self.colorColumn = 2
