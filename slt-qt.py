#!/usr/bin/env python3

#------------------------------------------
#-- Simple Login Tool using Qt
#-- Created by: Gergely Macoun
#-- Version   : 0.1
#-- License   : MIT
#------------------------------------------

__version__ = '0.1'

from PySide2.QtGui     import QColor
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout, 
    QLineEdit, 
    QPushButton, 
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTextEdit
)

import os
import sys

class App(QWidget):
    #------------------------------------------
    #-- Initialize the Class
    #------------------------------------------
    def __init__(self):
        super(App, self).__init__()

        #-- Window
        self.title  = 'SLT - Simple Login Tool - ' + __version__
        self.left   =  10
        self.top    =  10
        self.width  = 640
        self.height = 480

        #-- Hosts File
        self.listHosts          = []
        self.hostsFileName      = './slt.csv'
        self.hostsFileDelimiter = ';'

        #-- Connect File
        self.connectFileName  = './connect.sh'
        self.connectParamList = [4, 2] #-- These are those column numbers which data picked from the selected row and will be used as connection parameters

        #-- Layout
        self.mainLayout      = None

        #-- Input Box
        self.inputBox        = None

        #-- Search Button
        self.pushButton      = None
        self.namePushButton  = 'Connect'

        #-- My Table
        self.myTable         = None

        self.columnHeaders   = ['Application', 'Version', 'ENV', 'Hostname', 'FQDN']

        self.colorLightBlue  = QColor(173,216,230)
        self.colorLightGreen = QColor(144,238,144)
        self.colorCrimson    = QColor(220, 20, 60)
        self.colorIndianRed  = QColor(205, 92, 92)
        self.colorSalmon     = QColor(250,128,114)

        self.colorColumn          = 2  #-- Number of column which used for text matching 

        self.colorCell            = {}
        self.colorCell['PROD']    = self.colorSalmon
        self.colorCell['PREPROD'] = self.colorLightBlue
        self.colorCell['DEV']     = self.colorLightGreen

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

        #self.inputBox.editingFinished.connect(self.searchEvent)
        self.inputBox.textChanged.connect(self.searchEvent)

    #------------------------------------------
    #-- Create Push Button
    #------------------------------------------
    def createPushButton(self, text):
        if (self.pushButton is None):
            self.pushButton = QPushButton(text)

        #-- Add Clicked Event
        self.pushButton.clicked.connect(self.pushButtonEvent)

    #------------------------------------------
    #-- Search Event
    #------------------------------------------
    def searchEvent(self):
        #print('Search Event. Look up text is: %s' %(self.inputBox.text()))  #-- Debug
        self.refreshTable(self.inputBox.text())

    #------------------------------------------
    #-- Event for Push Button Pushed
    #------------------------------------------
    def pushButtonEvent(self):
        connectParameters = ''
        row = 0

        #print('Button Pressed')  #-- Debug

        if (self.myTable.rowCount() == 1):
            for column in self.connectParamList:
                cellTable = self.myTable.item(row, column)
                connectParameters += ' ' + str(cellTable.text())
            
            self.runConnect(connectParameters)
        #else:
            #print('More than one item in table, therefore cannot decide which one to choose')  #-- Debug

    #------------------------------------------
    #-- Event for Table Cell Double Clicked
    #------------------------------------------
    def myTableCellDoubleClickedEvent(self):
        connectParameters = ''
        row = self.myTable.currentRow()

        #print('Double Clicked on a Table Cell')  #-- Debug

        for column in self.connectParamList:
            cellTable = self.myTable.item(row, column)
            connectParameters += ' ' + str(cellTable.text())

        self.runConnect(connectParameters)

    #------------------------------------------
    #-- Run the Connect Command in Shell
    #------------------------------------------
    def runConnect(self, parameters):
        #print('Run: %s %s' %(self.connectFileName, parameters))  #-- Debug

        os.system(self.connectFileName + ' ' + parameters)

    #------------------------------------------
    #-- Create Table
    #------------------------------------------
    def createTable(self, listHosts):
        numCell    = 0

        maxTableRow     = len(listHosts)
        maxTableColumn  = len(self.columnHeaders)

        if (self.myTable is None):
            self.myTable = QTableWidget()
        
        #-- Set the Maximum Size of Table
        self.myTable.setColumnCount(maxTableColumn)
        self.myTable.setRowCount(maxTableRow)

        #-- Create the Horizontal Header of Table
        headerTableWidget = self.myTable.horizontalHeader()

        #-- Set the Table Header
        self.myTable.setHorizontalHeaderLabels(self.columnHeaders)
        #sself.myTable.horizontalHeader().setVisible(False)

        #-- Set the Cells to Read Only
        self.myTable.setEditTriggers(QTableWidget.NoEditTriggers)

        #-- Set Table Header Properties
        for item in self.columnHeaders:
            headerTableWidget.setSectionResizeMode(numCell, QHeaderView.ResizeToContents)
            numCell += 1
        
        #-- Set the First Column to Resizeable
        #headerTableWidget.setSectionResizeMode(0, QHeaderView.Stretch)

        #-- Set the Last Column to Resizeable
        headerTableWidget.setSectionResizeMode(numCell-1, QHeaderView.Stretch)

        #-- Set Double Clicked Event on Table
        self.myTable.itemDoubleClicked.connect(self.myTableCellDoubleClickedEvent)

        #-- Insert Data into Table
        self.insertDataIntoTable(self.myTable, self.listHosts)

    #------------------------------------------
    #-- Insert Data into the Table
    #------------------------------------------
    def insertDataIntoTable(self, inputTable, inputRecords):
        maxHeaderColumn = len(self.columnHeaders)
        maxTableColumn  = len(self.columnHeaders)
        maxTableRow     = len(inputRecords)
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
                    if (record[self.colorColumn] in self.colorCell):
                        inputTable.item(numRecord, numCell).setBackground(self.colorCell[record[self.colorColumn]])

                numCell += 1
            numCell    = 0
            numRecord += 1

        inputTable.move(0, 0)

    #------------------------------------------
    #-- Refresh Table
    #------------------------------------------
    def refreshTable(self, searchText):
        found             = False
        filteredListHosts = []

        #print('Refresh table data.')  #-- Debug

        #-- Clean the Table
        #self.myTable.clearContents()
        for row in range (self.myTable.rowCount()-1, -1, -1):
            #print('Remove row: %s' %(str(row))) #-- Debug
            self.myTable.removeRow(row)

        self.myTable.show()
        #-- Update the listHosts with searchText
        for record in self.listHosts:
            found = False
            for cell in record:
                if (searchText == '' or cell.lower().find(searchText.lower()) != -1):
                    #print('Found: %s' %(str(cell)))  #-- Debug
                    found = True
            
            if (found):
                filteredListHosts.append(record)

        #-- Recreate Table Data with filtered Values
        self.insertDataIntoTable(self.myTable, filteredListHosts)

        #-- Refresh the QTableWidget (required due to screen artifact)
        self.myTable.hide()
        self.myTable.show()

    #------------------------------------------
    #-- Read File
    #------------------------------------------
    def readFile(self, filename):
        fileHandle = None
        result     = []

        try:
            fileHandle = open(filename, 'r')
        except IOError:
            print('> ERROR: Could open file for read: %s' %(filename) )
            sys.exit(1)
        else:
            print('> File is opened for read: %s' %(filename) )
            fileContent = fileHandle.readlines()
            
            for line in fileContent:
                strippedLine = line.strip()

                if (strippedLine != ''):
                    if (strippedLine[0] != '#'):
                        #result.append(list(strippedLine.split(self.hostsFileDelimiter)))  #-- List Items are not Stripped
                        result.append(list(item.strip() for item in strippedLine.split(self.hostsFileDelimiter)))  #-- List Items are Stripped
                        #print(strippedLine)  #-- Debug

            #-- Debug
            #for line in result:
            #    for column in line:
            #        print('[\'%s\']' %(str(column)), end='')
            #    print('')
        finally:
            if fileHandle:
                fileHandle.close()

        return result

    #------------------------------------------
    #-- UI Initialization
    #------------------------------------------
    def initUI(self):
        #-- Read the File
        self.listHosts = self.readFile(self.hostsFileName)

        #-- Create GUI Elements
        self.createLayout()
        self.createInputBox()
        self.createPushButton(self.namePushButton)
        self.createTable(self.listHosts)

        #-- Set the Window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #-- Set the Layout
        self.mainLayout.addWidget(self.inputBox,   0,0,1,1)
        self.mainLayout.addWidget(self.pushButton, 0,1,1,1)
        self.mainLayout.addWidget(self.myTable,    1,0,1,2)
        
        self.setLayout(self.mainLayout)
        self.pushButton.show()
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
