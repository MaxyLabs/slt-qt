#!/bin/sh

FILE_APP="slt-qt.py"
FILE_ICON="icon/slt.icns"
OSX_BUNDLE_ID="com.maxylabs.slt-qt"

#----------------------
#-- Run the PyInstaller
#----------------------
pyinstaller ${FILE_APP} \
--icon=${FILE_ICON} \
--osx-bundle-identifier "${OSX_BUNDLE_ID}" \
--windowed \
--onefile \
--exclude-module='FixTk' \
--exclude-module='tcl' \
--exclude-module='tk' \
--exclude-module='_tkinter' \
--exclude-module='tkinter' \
--exclude-module='Tkinter'

# -- Copy the config folder
cp -r ./config ./dist/slt-qt.app/Contents/MacOS
