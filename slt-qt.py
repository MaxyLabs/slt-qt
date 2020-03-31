#!/usr/bin/env python3

# ------------------------------------------
# -- Simple Login Tool using Qt
# -- Created by: Gergely Macoun
# -- License   : MIT
# ------------------------------------------

import json
import os
import sys

from os.path import expanduser

try:
    from PySide2.QtGui import QColor, QIcon
    from PySide2.QtWidgets import (
        QApplication,
        QFrame,
        QGridLayout,
        QHeaderView,
        QLabel,
        QLineEdit,
        QMainWindow,
        QPushButton,
        QStatusBar,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QWidget,
    )
except ImportError:
    from PyQt5.QtGui import QColor, QIcon
    from PyQt5.QtWidgets import (
        QApplication,
        QFrame,
        QHeaderView,
        QGridLayout,
        QLabel,
        QLineEdit,
        QMainWindow,
        QPushButton,
        QStatusBar,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QWidget,
    )

__version__ = '0.2.4'


class VLine(QFrame):
    # -- A simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine)


class App(QMainWindow):
    # ------------------------------------------
    # -- Initialize the Class
    # ------------------------------------------
    def __init__(self):
        super(App, self).__init__()

        # -- Home Directory
        self.home_path = expanduser("~")

        # -- Base Path
        # self.app_path = os.path.abspath(__file__)
        self.app_path = sys.argv[0]
        self.base_path_split = self.app_path.split('/')
        self.base_path = str('/').join(self.base_path_split[0:-1])

        # -- Files under config
        self.config_file = self.base_path + '/config/config.json'
        self.connect_file = self.base_path + '/config/connect.sh'
        self.table_file = self.base_path + '/config/table.csv'

        self.delimiter_table_row = ';'

        # -- Data of Config File (with Default Values)
        self.config_data_file = {
            'Message': {
                'FileReadSuccess': True,
                'FileReadFailed': True,
                'ColorRedefinition': True
            },
            'Window': {
                'Left': 100,
                'Top': 100,
                'Width': 640,
                'Height': 480
            },
            'Margin': {
                'Left': 11,
                'Top': 11,
                'Right': 11,
                'Bottom': 11
            },
            'Title': {
                'Label': 'SLT - Simple Login Tool - ' + __version__
            },
            'Button': {
                'Connect': {
                    'Label': 'Connect'
                },
                'Message': {
                    'Label': 'X'
                }
            },
            'Table': {
                'Header': [
                ],
                'Column': {
                    'Color': 1,        # -- Number of column which used for text matching
                    'Connect': [9, 1]  # -- These are those column numbers which data picked from the selected row and will be used as connection parameters
                },
                'Cell': {
                    'Color': {
                    }
                }
            }
        }

        # -- Data of Table File
        self.table_data_file = []

        # -- Dictionary of Colors with QColor Elements
        self.color_data = {}

        # -- Central Widget
        self.central_widget = None

        # -- Main Layout
        self.main_layout = None

        # -- Input Box
        self.input_box = None

        # -- Connect Button
        self.connect_button = None

        # -- Message Button
        self.message_button = None

        # -- Message Label
        self.message_label = None
        self.message_label_count = None

        # -- Message List
        self.message_list = []

        # -- Main Table
        self.main_table = None

        # -- Status Bar
        self.status_bar = None

        # -- Messages
        self.messages = {
            'FileReadSuccess': 'INFO: File is opened for read: ',
            'FileReadFailed': 'ERROR: File could not be opened for read: ',
            'ColorRedefinition': 'WARN: Color Redefinition: '
        }

        # -- Initialize the UI
        self.initUI()

    # ------------------------------------------
    # -- Create Main Window
    # ------------------------------------------
    # def createMainWindow(self):
    #     if (self.main_window is None):
    #         self.main_window = QMainWindow(self)

    # ------------------------------------------
    # -- Create Central Widget
    # ------------------------------------------
    def createCentralWidget(self):
        if (self.central_widget is None):
            self.central_widget = QWidget()

        # -- Set Central Widget for QMainWindow
        self.setCentralWidget(self.central_widget)

    # ------------------------------------------
    # -- Create Layout
    # ------------------------------------------
    def createLayout(self):
        if (self.main_layout is None):
            self.main_layout = QGridLayout()

    # ------------------------------------------
    # -- Create Input Box
    # ------------------------------------------
    def createInputBox(self):
        if (self.input_box is None):
            self.input_box = QLineEdit()

        # -- Enable Clear Button
        self.input_box.setClearButtonEnabled(True)

        # -- Create Event if enter pressed
        # self.input_box.editingFinished.connect(self.eventSearchInTable)
        self.input_box.editingFinished.connect(self.eventConnectButtonClicked)

        # -- Create Event if text changed
        self.input_box.textChanged.connect(self.eventSearchInTable)

    # ------------------------------------------
    # -- Search Event
    # ------------------------------------------
    def eventSearchInTable(self):
        # print('Search Event. Look up text is: %s' %(self.input_box.text()))  # -- Debug
        self.refreshTable(self.input_box.text().strip())

    # ------------------------------------------
    # -- Create Connect Button
    # ------------------------------------------
    def createConnectButton(self, text):
        if (self.connect_button is None):
            self.connect_button = QPushButton(text)

        # -- Add Clicked Event
        self.connect_button.clicked.connect(self.eventConnectButtonClicked)

    # ------------------------------------------
    # -- Event for Connect Button Clicked
    # ------------------------------------------
    def eventConnectButtonClicked(self):
        connectParameters = ''
        row = 0

        # print('Connect Button Pressed')  # -- Debug

        if (self.main_table.rowCount() == 1):
            for column in self.config_data_file['Table']['Column']['Connect']:
                cellTable = self.main_table.item(row, column)
                connectParameters += ' ' + str(cellTable.text())

            self.connectExecute(connectParameters)
        # else:
            # print('More than one item in table, therefore cannot decide which one to choose')  # -- Debug

    # ------------------------------------------
    # -- Create Status Bar
    # ------------------------------------------
    def createStatusBar(self):
        if (self.status_bar is None):
            self.status_bar = QStatusBar()

        self.status_bar.addWidget(self.message_label_count, 0)
        self.status_bar.addWidget(VLine(), 0)
        self.status_bar.addWidget(self.message_label, 1)
        self.status_bar.addWidget(self.message_button, 0)

    # ------------------------------------------
    # -- Update Status Bar
    # ------------------------------------------
    def updateStatusBar(self):
        if (self.status_bar is not None):
            # -- Hide the Status Bar if the Message List is empty
            if (len(self.message_list) > 0):
                self.status_bar.show()
            else:
                self.status_bar.hide()

    # ------------------------------------------
    # -- Get Latest Message
    # ------------------------------------------
    def getLatestMessage(self):
        result = None
        length = len(self.message_list)

        if (length > 0):
            result = self.message_list[length - 1]

        return result

    # ------------------------------------------
    # -- Create Message Label
    # ------------------------------------------
    def createMessageLabel(self):
        if (self.message_label is None):
            self.message_label = QLabel(self)

        # -- Add a Text to Message Label
        # self.message_label.setText(self.getLatestMessage())
        self.updateMessageLabel()

    # ------------------------------------------
    # -- Update Message Label with Latest Entry
    # ------------------------------------------
    def updateMessageLabel(self):
        message = ''
        length = len(self.message_list)

        if (self.message_label is not None):
            if (length > 0):
                message = self.message_list[-1]

            self.message_label.setText(message)

    # ------------------------------------------
    # -- Create Message Label Count
    # ------------------------------------------
    def createMessageLabelCount(self):
        if (self.message_label_count is None):
            self.message_label_count = QLabel(self)

        self.updateMessageLabelCount()

    # ------------------------------------------
    # -- Update Message Label Count
    # ------------------------------------------
    def updateMessageLabelCount(self):
        message = ''
        length = len(self.message_list)

        if (self.message_label_count is not None):
            if (length > 0):
                message = '  ' + str(length)

            self.message_label_count.setText(message)

    # ------------------------------------------
    # -- Create Message Button
    # ------------------------------------------
    def createMessageButton(self, text):
        if (self.message_button is None):
            self.message_button = QPushButton(text)

        # -- Add Clicked Event
        self.message_button.clicked.connect(self.eventMessageButtonClicked)

    # ------------------------------------------
    # -- Event for Message Button Clicked
    # ------------------------------------------
    def eventMessageButtonClicked(self):
        length = len(self.message_list)

        # -- Remove the latest item in Message List
        if (length > 0):
            del self.message_list[length-1]

        # -- Update Message Labels
        self.updateMessageLabel()
        self.updateMessageLabelCount()

        # -- Update the Status Bar
        self.updateStatusBar()

    # ------------------------------------------
    # -- Add a New Message to List
    # ------------------------------------------
    def addNewMessage(self, message):
        self.message_list.append(message)
        self.updateMessageLabel()

        # -- Update Status Bar
        self.updateStatusBar()

    # ------------------------------------------
    # -- Check Table Header
    # ------------------------------------------
    def checkMainTableHeader(self, hostsList):
        # -- Length of the Header defined in the config file
        lengthHeaderconfig_file = len(self.config_data_file['Table']['Header'])

        # -- Length of the First Record
        if (len(hostsList) > 0):
            lengthFirstRecord = len(hostsList[0])
        else:
            lengthFirstRecord = 0

        # -- Append the Header if the list in config file is too short
        if (lengthHeaderconfig_file < lengthFirstRecord):
            for header in range(lengthHeaderconfig_file+1, lengthFirstRecord+1):
                self.config_data_file['Table']['Header'].append(str(header))

    # ------------------------------------------
    # -- Create Table
    # ------------------------------------------
    def createMainTable(self, hostsList):
        numCell = 0

        maxTableRow = len(hostsList)
        maxTableColumn = len(self.config_data_file['Table']['Header'])

        if (self.main_table is None):
            self.main_table = QTableWidget()

        # -- Set the Maximum Size of Table
        self.main_table.setColumnCount(maxTableColumn)
        self.main_table.setRowCount(maxTableRow)

        # -- Create the Horizontal Header of Table
        headerTableWidget = self.main_table.horizontalHeader()

        # -- Set the Table Header
        self.main_table.setHorizontalHeaderLabels(self.config_data_file['Table']['Header'])

        # -- Hide The Horizontal Table Header
        # self.main_table.horizontalHeader().setVisible(False)

        # -- Set the Cells to Read Only
        self.main_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # -- Set Table Header Properties
        for numCell in range(0, len(self.config_data_file['Table']['Header'])):
            headerTableWidget.setSectionResizeMode(numCell, QHeaderView.ResizeToContents)

        # -- Set the First Column to Resizeable
        # headerTableWidget.setSectionResizeMode(0, QHeaderView.Stretch)

        # -- Set the Last Column to Resizeable
        headerTableWidget.setSectionResizeMode(maxTableColumn-1, QHeaderView.Stretch)

        # -- Add Double Clicked Event on Table
        self.main_table.itemDoubleClicked.connect(self.eventMainTableDoubleClickedOnCell)

        # -- Insert Data into Table
        self.insertDataIntoTable(self.main_table, hostsList)

    # ------------------------------------------
    # -- Double Clicked on Cell Event
    # ------------------------------------------
    def eventMainTableDoubleClickedOnCell(self):
        connectParameters = ''
        row = self.main_table.currentRow()

        # print('Double Clicked on a Table Cell')  # -- Debug

        for column in self.config_data_file['Table']['Column']['Connect']:
            cellTable = self.main_table.item(row, column)
            connectParameters += ' ' + str(cellTable.text())

        self.connectExecute(connectParameters)

    # ------------------------------------------
    # -- Insert Data into the Table
    # ------------------------------------------
    def insertDataIntoTable(self, inputTable, inputRecords):
        maxHeaderColumn = len(self.config_data_file['Table']['Header'])
        maxTableColumn = len(self.config_data_file['Table']['Header'])
        maxTableRow = len(inputRecords)
        colorColumn = self.config_data_file['Table']['Column']['Color']
        numRecord = 0
        numCell = 0

        # -- Set the Maximum size of Table
        inputTable.setColumnCount(maxTableColumn)
        inputTable.setRowCount(maxTableRow)

        for record in inputRecords:
            # print('Record : %s' %(str(record)))  # -- Debug
            for cell in record:
                # print('Cell : %s' %(cell))  # -- Debug
                if (numCell < maxHeaderColumn):
                    inputTable.setItem(numRecord, numCell, QTableWidgetItem(cell))

                    # -- Set the Background Color of Cells
                    # if (record[colorColumn] in self.colorCell):
                    #     inputTable.item(numRecord, numCell).setBackground(self.colorCell[record[colorColumn]])
                    if (record[colorColumn] in self.config_data_file['Table']['Cell']['Color']):
                        nameColor = self.config_data_file['Table']['Cell']['Color'][record[colorColumn]]

                        # print('Cell: %s, %s, %s' %(record[colorColumn], nameColor, self.color_data[nameColor]))  # -- Debug

                        inputTable.item(numRecord, numCell).setBackground(self.color_data[nameColor])

                numCell += 1
            numCell = 0
            numRecord += 1

        inputTable.move(0, 0)

    # ------------------------------------------
    # -- Refresh Table
    # ------------------------------------------
    def refreshTable(self, searchText):
        found = False
        filteredHostsList = []

        # print('Refresh table data.')  # -- Debug

        # -- Clean the Table
        for row in range(self.main_table.rowCount()-1, -1, -1):
            # print('Remove row: %s' %(str(row))) # -- Debug
            self.main_table.removeRow(row)

        self.main_table.show()

        # -- Update the table_data_file with searchText
        for record in self.table_data_file:
            found = False
            for cell in record:
                if (searchText == '' or cell.lower().find(searchText.lower()) != -1):
                    # print('Found: %s' %(str(cell)))  # -- Debug
                    found = True

            if (found):
                filteredHostsList.append(record)

        # -- Recreate Table Data with filtered Values
        self.insertDataIntoTable(self.main_table, filteredHostsList)

        # -- Refresh the QTableWidget (required due to screen artifact)
        self.main_table.hide()
        self.main_table.show()

    # ------------------------------------------
    # -- Read Config File
    # ------------------------------------------
    def readConfigFile(self, filename):
        fileHandle = None
        message = ''

        try:
            fileHandle = open(filename, 'r')
        except IOError:
            message = self.messages['FileReadFailed'] + filename
            print(message)

            # -- Message
            if (self.config_data_file['Message']['FileReadFailed'] is True):
                self.addNewMessage(message)
        else:
            message = self.messages['FileReadSuccess'] + filename
            print(message)

            # -- Update the Default Data Values with the New Ones
            # self.config_data_file = json.load(fileHandle)
            self.config_data_file.update(json.load(fileHandle))

            # -- Add Colors to the List
            for key, value in self.config_data_file['Color'].items():
                # -- Check the Length of Value (must have 3 elements [R,G,B])
                if(len(value) == 3):
                    self.addColor(key, value[0], value[1], value[2])

            # -- Message
            if (self.config_data_file['Message']['FileReadSuccess'] is True):
                self.addNewMessage(message)

            # print('JSON: %s' %(self.config_data_file))  # -- Debug
        finally:
            if (fileHandle):
                fileHandle.close()

    # ------------------------------------------
    # -- Add Color to the Dictionary
    # ------------------------------------------
    def addColor(self, name, red, green, blue):
        # print('Add Color: %s [%d,%d,%d]' %(name, red, green, blue))  # -- Debug

        # -- Check Red
        if(type(red) is int):
            if(red < 0 or red > 255):
                red = 255
        else:
            red = 255

        # -- Check Green
        if(type(green) is int):
            if(green < 0 or green > 255):
                green = 255
        else:
            green = 255

        # -- Check Blue
        if(type(blue) is int):
            if(blue < 0 or blue > 255):
                blue = 255
        else:
            blue = 255

        # print('Add Color: %s [%d,%d,%d]' %(name, red, green, blue))  # -- Debug

        # -- Add the Color to the Dictionary
        if(name not in self.color_data):
            self.color_data[name] = QColor(red, green, blue)
        else:
            # -- Message
            if (self.config_data_file['Message']['ColorRedefinition'] is True):
                self.addNewMessage(self.messages['ColorRedefinition'] + name)

    # ------------------------------------------
    # -- Read CSV File
    # ------------------------------------------
    def readCsvFile(self, filename):
        fileHandle = None
        result = []
        message = ''

        try:
            fileHandle = open(filename, 'r')
        except IOError:
            message = self.messages['FileReadFailed'] + filename
            print(message)

            # -- Message
            if (self.config_data_file['Message']['FileReadFailed'] is True):
                self.addNewMessage(message)
        else:
            message = self.messages['FileReadSuccess'] + filename
            print(message)

            # -- Message
            if (self.config_data_file['Message']['FileReadSuccess'] is True):
                self.addNewMessage(message)

            fileContent = fileHandle.readlines()

            for line in fileContent:
                strippedLine = line.strip()

                if (strippedLine != ''):
                    if (strippedLine[0] != '#'):
                        # result.append(list(strippedLine.split(self.delimiter_table_row)))  # -- List Items are not Stripped
                        result.append(list(item.strip() for item in strippedLine.split(self.delimiter_table_row)))  # -- List Items are Stripped
                        # print(strippedLine)  # -- Debug

            # -- Debug
            # for line in result:
            #    for column in line:
            #        print('[\'%s\']' %(str(column)), end='')
            #    print('')
        finally:
            if (fileHandle):
                fileHandle.close()

        return result

    # ------------------------------------------
    # -- Execute the Connect Command in Shell
    # ------------------------------------------
    def connectExecute(self, parameters):
        # print('Run: %s %s' %(self.connect_file, parameters))  # -- Debug

        os.system(self.connect_file + ' ' + parameters)

    # ------------------------------------------
    # -- UI Initialization
    # ------------------------------------------
    def initUI(self):
        # -- Read the Config File
        self.readConfigFile(self.config_file)

        # -- Read the Table CSV File
        self.table_data_file = self.readCsvFile(self.table_file)

        # -- Create GUI Elements
        self.createCentralWidget()
        self.createLayout()

        self.createInputBox()
        self.createConnectButton(self.config_data_file['Button']['Connect']['Label'])
        self.checkMainTableHeader(self.table_data_file)
        self.createMainTable(self.table_data_file)

        self.createMessageLabel()
        self.createMessageLabelCount()
        self.createMessageButton(self.config_data_file['Button']['Message']['Label'])

        self.createStatusBar()

        # -- Set Window Title
        self.setWindowTitle(self.config_data_file['Title']['Label'])

        # -- Set Window Geometry
        self.setGeometry(
            self.config_data_file['Window']['Left'],
            self.config_data_file['Window']['Top'],
            self.config_data_file['Window']['Width'],
            self.config_data_file['Window']['Height']
        )

        # -- Set Layout Margins
        self.main_layout.setContentsMargins(
            self.config_data_file['Margin']['Left'],
            self.config_data_file['Margin']['Top'],
            self.config_data_file['Margin']['Right'],
            self.config_data_file['Margin']['Bottom']
        )

        # -- Set Layout
        self.central_widget.setLayout(self.main_layout)

        # -- Add Widgets to Layout
        self.main_layout.addWidget(self.input_box, 0, 0, 1, 1)
        self.main_layout.addWidget(self.connect_button, 0, 1, 1, 1)
        self.main_layout.addWidget(self.main_table, 1, 0, 1, 2)

        # -- Set Status Bar for QMainWindow
        self.setStatusBar(self.status_bar)


# ------------------------------------------
# -- Main
# ------------------------------------------
def main():
    app = QApplication(sys.argv)
    gui = App()
    gui.show()
    sys.exit(app.exec_())


# ------------------------------------------
# -- Entrypoint
# ------------------------------------------
if __name__ == '__main__':
    main()
