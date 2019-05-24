# slt-qt

# Simple Login Tool

This application makes it easier to search for a specific hostname in a predefined csv file and open a new terminal window for it.<br/>
It is written in Python using PySide and Qt.

![Screenshot](/screenshot/slt-qt-v0.1.png "slt-qt v0.1")

# Install Required Dependencies
## Linux

``
$ dnf install python3-pyside2
``

## macOS

``
$ brew install python pyside 
``

# Create Application Bundle
## macOS

``
$ ./create-app-bundle-mac.sh
``

# Download Application Bundles
- [slt-qt-v0.2-mac.zip](https://github.com/MaxyLabs/slt-qt/blob/master/build/slt-qt-v0.2-mac.zip)

# Run the App

``
$ python ./slt-qt.py
``

# How-To
**How to issue the connect.sh for a specific row?**
- Double click on a row
- Use the text filed to sort the list to just one item and push the Connect button

**How to change which parameters are passed to the connect.sh?**
- Modify this variable: self.connectParamList
- The default value is [4, 2] which means that it passes the 4th and 2nd columns

**How to change the Table Header Names?**
- Modify this variable: self.columnHeaders

**How to change which column is connected to colorizing the table records?**
- Modify this variable: self.colorColumn

**How to change which text uses which color?**
- Modify this variable: self.colorCell
