#!/bin/sh

FILE_APP="slt-qt.py"
FILE_ICON="icon/slt.icns"
OSX_BUNDLE_ID="com.maxylabs.slt-qt"

#----------------------
#-- Run the PyInstaller
#----------------------
pyinstaller ${FILE_APP} \
--icon=${FILE_ICON} \
--windowed \
--osx-bundle-identifier "${OSX_BUNDLE_ID}"

# -- Copy the config folder
cp -r ./config ./dist/slt-qt.app/Contents/MacOS