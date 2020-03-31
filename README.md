# slt-qt

# Simple Login Tool

This application makes it easier to search for a specific hostname in a predefined csv file and open a new terminal window for it.<br/>
It is written in Python using PySide and Qt.

![Screenshot](/screenshot/slt-qt-v0.2.1-mac.png "slt-qt v0.2.1")

# Install Required Dependencies

## Linux

```
#-- PySide2
$ sudo dnf install python3-pyside2

#-- PyQt5
$ sudo dnf install python3-qt5
```

## macOS

Install [brew](https://brew.sh/)

```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Install packages via brew

```
$ brew install python
```

Install python packages via pip

```
$ pip3 install PyInstaller shiboken2 PySide2
```

# Run the App

```
$ python ./slt-qt.py
```

# Create Application Bundle

## macOS

```
$ ./create-app-bundle-mac.sh
```

# Download Application Bundles
- [slt-qt-v0.2.1-mac.zip](https://github.com/MaxyLabs/slt-qt/raw/master/build/slt-qt-v0.2.1-mac.zip)

# How-To
**How to issue the connect.sh for a specific row?**
- Double click on a row
- Use the text filed to sort the list to just one item and push the Connect button

**You can change the following parameters in $HOME/.config/slt/config.json file**
- Enable / Disable bottom pop-up messages
- Color codes in RGB
- Button labels
- Table Header Names
- Which table column used for colorizing
- Which table column used for connection parameters
- Which Table Cell data used for Record Colorizing
