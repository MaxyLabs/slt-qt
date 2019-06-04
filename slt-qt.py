#!/usr/bin/env python3

#------------------------------------------
#-- Simple Login Tool using Qt
#-- Created by: Gergely Macoun
#-- Version   : 0.2.1
#-- License   : MIT
#------------------------------------------

__version__ = '0.2.1'

from PySide2.QtGui     import QColor
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout, 
    QLabel,
    QLineEdit, 
    QPushButton, 
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTextEdit
)

import json
import os
import sys

from os.path import expanduser

class App(QWidget):
    #------------------------------------------
    #-- Initialize the Class
    #------------------------------------------
    def __init__(self):
        super(App, self).__init__()

        #-- Home Directory
        self.homeDir = expanduser("~")

        #-- Files
        self.configFile  = self.homeDir + '/.config/slt/config.json'
        self.connectFile = self.homeDir + '/.config/slt/connect.sh'
        self.tableFile   = self.homeDir + '/.config/slt/table.csv'

        self.delimitertableFile = ';'

        #-- Data of Config File (with Default Values)
        self.dataConfigFile = {
            'Message': {
                'FileReadSuccess'   : True,
                'FileReadFailed'    : True,
                'ColorRedefinition' : True
            },
            'Window' : {
                'Left'   : 100,
                'Top'    : 100,
                'Width'  : 640,
                'Height' : 480
            },
            'Title' : {
                'Label' : 'SLT - Simple Login Tool - ' + __version__
            },
            'Button' : {
                'Connect' : {
                    'Label' : 'Connect'
                },
                'Message' : {
                    'Label' : 'X'
                }
            },
            'Table' :{
                'Header' : [
                ],
                'Column' : {
                    'Color'   : 1,      #-- Number of column which used for text matching
                    'Connect' : [9, 1]  #-- These are those column numbers which data picked from the selected row and will be used as connection parameters
                },
                'Cell' : {
                    'Color' : {
                    }
                }
            }
        }

        #-- Data of Table File
        self.dataTableFile = []

        #-- Layout
        self.mainLayout    = None

        #-- Input Box
        self.inputBox      = None

        #-- Connect Button
        self.connectButton = None

        #-- Message Button
        self.messageButton = None

        #-- Message Label
        self.messageLabel  = None
        self.messageList   = []

        #-- My Table
        self.myTable       = None

        #-- Color Dictionary with QColor Elements
        self.colorDict = {}

        #-- Messages
        self.messages = {}
        self.messages['FileReadSuccess']   = 'INFO: File is opened for read: '
        self.messages['FileReadFailed']    = 'ERROR: File could not be opened for read: '
        self.messages['ColorRedefinition'] = 'WARN: Color Redefinition: '
        
        #-- Initialize the UI
        self.initUI()

    #------------------------------------------
    #-- Create Layout
    #------------------------------------------
    def createLayout(self):
        if (self.mainLayout is None):
            self.mainLayout = QGridLayout()

    #------------------------------------------
    #-- Create Text Box
    #------------------------------------------
    def createInputBox(self):
        if (self.inputBox is None):
            self.inputBox = QLineEdit(self)

        #-- Add Search Event if ENTER Pressed
        #self.inputBox.editingFinished.connect(self.searchEvent)

        #-- Add Search Event if Text Changes
        self.inputBox.textChanged.connect(self.searchEvent)

    #------------------------------------------
    #-- Search Event
    #------------------------------------------
    def searchEvent(self):
        #print('Search Event. Look up text is: %s' %(self.inputBox.text()))  #-- Debug
        self.refreshTable(self.inputBox.text())

    #------------------------------------------
    #-- Create Connect Button
    #------------------------------------------
    def createConnectButton(self, text):
        if (self.connectButton is None):
            self.connectButton = QPushButton(text)

        #-- Add Clicked Event
        self.connectButton.clicked.connect(self.connectButtonEvent)

    #------------------------------------------
    #-- Push Event for Connect Button
    #------------------------------------------
    def connectButtonEvent(self):
        connectParameters = ''
        row = 0

        #print('Connect Button Pressed')  #-- Debug

        if (self.myTable.rowCount() == 1):
            for column in self.dataConfigFile['Table']['Column']['Connect']:
                cellTable = self.myTable.item(row, column)
                connectParameters += ' ' + str(cellTable.text())
            
            self.connectExecute(connectParameters)
        #else:
            #print('More than one item in table, therefore cannot decide which one to choose')  #-- Debug

    #------------------------------------------
    #-- Create Message Button
    #------------------------------------------
    def createMessageButton(self, text):
        if (self.messageButton is None):
            self.messageButton = QPushButton(text)

        #-- Add Clicked Event
        self.messageButton.clicked.connect(self.messageButtonEvent)

    #------------------------------------------
    #-- Push Event for Message Button
    #------------------------------------------
    def messageButtonEvent(self):
        length = len(self.messageList)

        if (length > 0):
            del self.messageList[length-1]
            self.updateMessageLabel()

        if (length - 1 == 0):
            self.hideMessageEvent()

    #------------------------------------------
    #-- Hide Message Row Event
    #------------------------------------------
    def hideMessageEvent(self):
        self.messageLabel.hide()
        self.messageButton.hide()

    #------------------------------------------
    #-- Show Message Row Event
    #------------------------------------------
    def showMessageEvent(self):
        if (self.messageLabel is not None):
            self.messageLabel.show()

        if (self.messageButton is not None):
            self.messageButton.show()

    #------------------------------------------
    #-- Create Message Label
    #------------------------------------------
    def createMessageLabel(self):
        if (self.messageLabel is None):
            self.messageLabel = QLabel(self)

    #------------------------------------------
    #-- Add a Text to Message Label
    #------------------------------------------
    def addMessageLabel(self, message):
        self.messageList.append(message)
        self.updateMessageLabel()
        self.showMessageEvent()

    #------------------------------------------
    #-- Update Message Label with Latest Entry
    #------------------------------------------
    def updateMessageLabel(self):
        length  = len(self.messageList)

        if (length > 0):
            message = '(' + str(length) + ') ' + self.messageList[length-1]
        else:
            message = ''

        if (self.messageLabel is not None):
            self.messageLabel.setText(message)

    #------------------------------------------
    #-- Check Table Header
    #------------------------------------------
    def checkHeaderTable(self, hostsList):
        #-- Length of the Header defined in the config file
        lengthHeaderConfigFile = len(self.dataConfigFile['Table']['Header'])

        #-- Length of the First Record
        if (len(hostsList) > 0):
            lengthFirstRecord = len(hostsList[0])
        else:
            lengthFirstRecord = 0

        #-- Append the Header if the list in config file is too short
        if (lengthHeaderConfigFile < lengthFirstRecord):
            for header in range(lengthHeaderConfigFile+1, lengthFirstRecord+1):
                self.dataConfigFile['Table']['Header'].append(str(header))

    #------------------------------------------
    #-- Create Table
    #------------------------------------------
    def createTable(self, hostsList):
        numCell    = 0

        maxTableRow     = len(hostsList)
        maxTableColumn  = len(self.dataConfigFile['Table']['Header'])

        if (self.myTable is None):
            self.myTable = QTableWidget()
        
        #-- Set the Maximum Size of Table
        self.myTable.setColumnCount(maxTableColumn)
        self.myTable.setRowCount(maxTableRow)

        #-- Create the Horizontal Header of Table
        headerTableWidget = self.myTable.horizontalHeader()

        #-- Set the Table Header
        self.myTable.setHorizontalHeaderLabels(self.dataConfigFile['Table']['Header'])

        #-- Hide The Horizontal Table Header
        #sself.myTable.horizontalHeader().setVisible(False)

        #-- Set the Cells to Read Only
        self.myTable.setEditTriggers(QTableWidget.NoEditTriggers)

        #-- Set Table Header Properties
        for numCell in range(0, len(self.dataConfigFile['Table']['Header'])):
            headerTableWidget.setSectionResizeMode(numCell, QHeaderView.ResizeToContents)
        
        #-- Set the First Column to Resizeable
        #headerTableWidget.setSectionResizeMode(0, QHeaderView.Stretch)

        #-- Set the Last Column to Resizeable
        headerTableWidget.setSectionResizeMode(maxTableColumn-1, QHeaderView.Stretch)

        #-- Add Double Clicked Event on Table
        self.myTable.itemDoubleClicked.connect(self.doubleClickedOnCellEvent)

        #-- Insert Data into Table
        self.insertDataIntoTable(self.myTable, hostsList)

    #------------------------------------------
    #-- Double Clicked on Cell Event
    #------------------------------------------
    def doubleClickedOnCellEvent(self):
        connectParameters = ''
        row = self.myTable.currentRow()

        #print('Double Clicked on a Table Cell')  #-- Debug

        for column in self.dataConfigFile['Table']['Column']['Connect']:
            cellTable = self.myTable.item(row, column)
            connectParameters += ' ' + str(cellTable.text())

        self.connectExecute(connectParameters)

    #------------------------------------------
    #-- Insert Data into the Table
    #------------------------------------------
    def insertDataIntoTable(self, inputTable, inputRecords):
        maxHeaderColumn = len(self.dataConfigFile['Table']['Header'])
        maxTableColumn  = len(self.dataConfigFile['Table']['Header'])
        maxTableRow     = len(inputRecords)
        colorColumn     = self.dataConfigFile['Table']['Column']['Color']
        numRecord       = 0
        numCell         = 0
        
        #-- Set the Maximum size of Table
        inputTable.setColumnCount(maxTableColumn)
        inputTable.setRowCount(maxTableRow)

        for record in inputRecords:
            #print('Record : %s' %(str(record)))  #-- Debug
            for cell in record:
                #print('Cell : %s' %(cell))  #-- Debug
                if (numCell < maxHeaderColumn):
                    inputTable.setItem(numRecord, numCell, QTableWidgetItem(cell))

                    #-- Set the Background Color of Cells
                    #if (record[colorColumn] in self.colorCell):
                        #inputTable.item(numRecord, numCell).setBackground(self.colorCell[record[colorColumn]])
                    if (record[colorColumn] in self.dataConfigFile['Table']['Cell']['Color']):
                        nameColor = self.dataConfigFile['Table']['Cell']['Color'][record[colorColumn]]

                        #print('Cell: %s, %s, %s' %(record[colorColumn], nameColor, self.colorDict[nameColor]))  #-- Debug

                        inputTable.item(numRecord, numCell).setBackground(self.colorDict[nameColor])

                numCell += 1
            numCell    = 0
            numRecord += 1

        inputTable.move(0, 0)

    #------------------------------------------
    #-- Refresh Table
    #------------------------------------------
    def refreshTable(self, searchText):
        found             = False
        filteredHostsList = []

        #print('Refresh table data.')  #-- Debug

        #-- Clean the Table
        for row in range (self.myTable.rowCount()-1, -1, -1):
            #print('Remove row: %s' %(str(row))) #-- Debug
            self.myTable.removeRow(row)

        self.myTable.show()

        #-- Update the dataTableFile with searchText
        for record in self.dataTableFile:
            found = False
            for cell in record:
                if (searchText == '' or cell.lower().find(searchText.lower()) != -1):
                    #print('Found: %s' %(str(cell)))  #-- Debug
                    found = True
            
            if (found):
                filteredHostsList.append(record)

        #-- Recreate Table Data with filtered Values
        self.insertDataIntoTable(self.myTable, filteredHostsList)

        #-- Refresh the QTableWidget (required due to screen artifact)
        self.myTable.hide()
        self.myTable.show()

    #------------------------------------------
    #-- Read Config File
    #------------------------------------------
    def readConfigFile(self, filename):
        fileHandle = None
        message = ''

        try:
            fileHandle = open(filename, 'r')
        except IOError:
            message = self.messages['FileReadFailed'] + filename
            print(message)

            #-- Message
            if (self.dataConfigFile['Message']['FileReadFailed'] is True):
                self.addMessageLabel(message)
        else:
            message = self.messages['FileReadSuccess'] + filename
            print(message)

            #-- Update the Default Data Values with the New Ones
            #self.dataConfigFile = json.load(fileHandle)
            self.dataConfigFile.update(json.load(fileHandle))

            #-- Add Colors to the List
            for key, value in self.dataConfigFile['Color'].items():
                #-- Check the Length of Value (must have 3 elements [R,G,B])
                if(len(value) == 3):
                    self.addColor(key, value[0], value[1], value[2])

            #-- Message
            if (self.dataConfigFile['Message']['FileReadSuccess'] is True):
                self.addMessageLabel(message)
            
            #print('JSON: %s' %(self.dataConfigFile))  #-- Debug
        finally:
            if (fileHandle):
                fileHandle.close()

    #------------------------------------------
    #-- Add Color to the Dictionary
    #------------------------------------------
    def addColor(self, name, red, green, blue):
        #print('Add Color: %s [%d,%d,%d]' %(name, red, green, blue))  #-- Debug

        #-- Check Red
        if(type(red) is int):
            if(red < 0 or red > 255):
                red = 255
        else:
            red = 255

        #-- Check Green
        if(type(green) is int):
            if(green < 0 or green > 255):
                green = 255
        else:
            green = 255

        #-- Check Blue
        if(type(blue) is int):
            if(blue < 0 or blue > 255):
                blue = 255
        else:
            blue = 255

        #print('Add Color: %s [%d,%d,%d]' %(name, red, green, blue))  #-- Debug

        #-- Add the Color to the Dictionary
        if(name not in self.colorDict):
            self.colorDict[name] = QColor(red, green, blue)
        else:
            #-- Message
            if (self.dataConfigFile['Message']['ColorRedefinition'] is True):
                self.addMessageLabel(self.messages['ColorRedefinition'] + name)

    #------------------------------------------
    #-- Read CSV File
    #------------------------------------------
    def readCsvFile(self, filename):
        fileHandle = None
        result     = []
        message    = ''

        try:
            fileHandle = open(filename, 'r')
        except IOError:
            message = self.messages['FileReadFailed'] + filename
            print(message)

            #-- Message
            if (self.dataConfigFile['Message']['FileReadFailed'] is True):
                self.addMessageLabel(message)
        else:
            message = self.messages['FileReadSuccess'] + filename
            print(message)

            #-- Message
            if (self.dataConfigFile['Message']['FileReadSuccess'] is True):
                self.addMessageLabel(message)

            fileContent = fileHandle.readlines()

            for line in fileContent:
                strippedLine = line.strip()

                if (strippedLine != ''):
                    if (strippedLine[0] != '#'):
                        #result.append(list(strippedLine.split(self.delimiterTableFile)))  #-- List Items are not Stripped
                        result.append(list(item.strip() for item in strippedLine.split(self.delimitertableFile)))  #-- List Items are Stripped
                        #print(strippedLine)  #-- Debug

            #-- Debug
            #for line in result:
            #    for column in line:
            #        print('[\'%s\']' %(str(column)), end='')
            #    print('')
        finally:
            if (fileHandle):
                fileHandle.close()

        return result
    
    #------------------------------------------
    #-- Execute the Connect Command in Shell
    #------------------------------------------
    def connectExecute(self, parameters):
        #print('Run: %s %s' %(self.connectFile, parameters))  #-- Debug

        os.system(self.connectFile + ' ' + parameters)

    #------------------------------------------
    #-- UI Initialization
    #------------------------------------------
    def initUI(self):
        #-- Read the File
        self.readConfigFile(self.configFile)
        self.dataTableFile = self.readCsvFile(self.tableFile)

        #-- Create GUI Elements
        self.createLayout()
        self.createInputBox()
        self.createConnectButton(self.dataConfigFile['Button']['Connect']['Label'])
        self.checkHeaderTable(self.dataTableFile)
        self.createTable(self.dataTableFile)
        self.createMessageButton(self.dataConfigFile['Button']['Message']['Label'])
        self.createMessageLabel()
        self.updateMessageLabel()

        #-- Set the Window
        #self.setWindowTitle(self.title)
        self.setWindowTitle(self.dataConfigFile['Title']['Label'])
        self.setGeometry(
            self.dataConfigFile['Window']['Left'],
            self.dataConfigFile['Window']['Top'],
            self.dataConfigFile['Window']['Width'],
            self.dataConfigFile['Window']['Height']
        )
        
        #-- Set the Layout
        self.mainLayout.addWidget(self.inputBox,      0,0,1,1)
        self.mainLayout.addWidget(self.connectButton, 0,1,1,1)
        self.mainLayout.addWidget(self.myTable,       1,0,1,2)
        self.mainLayout.addWidget(self.messageLabel,  2,0,1,1)
        self.mainLayout.addWidget(self.messageButton, 2,1,1,1)

        #-- Hide the Bottom Message if the List is Empty
        if (len(self.messageList) == 0):
            self.hideMessageEvent()

        self.setLayout(self.mainLayout)
        self.connectButton.show()
        self.show()

#------------------------------------------
#-- Main
#------------------------------------------
def main():
    app = QApplication(sys.argv)
    gui = App()
    sys.exit(app.exec_())

#------------------------------------------
#-- Entrypoint
#------------------------------------------
if __name__ == '__main__':
    main()
