#!/bin/sh

#----------------------
#-- Run the PyInstaller
#----------------------
pyinstaller slt-qt.py \
--icon=slt.icns \
--windowed \
--osx-bundle-identifier "com.maxylabs.slt-qt"

#---------------------------------
#-- Copy the Required Dependencies
#---------------------------------
DIR_SOURCE="/usr/local/Cellar/pyside/5.12.1/lib/python3.7/site-packages"
DIR_TARGET="./dist/slt-qt.app/Contents/MacOS"

LIB_REQ="PySide2
pyside2uic
shiboken2
shiboken2_generator"

for LIB in ${LIB_REQ}
do
  cp -r ${DIR_SOURCE}/${LIB} ${DIR_TARGET}
done
