#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlList

"""
import logging
import os

from PyQt4 import uic, QtCore
from PyQt4.QtGui import QWidget, QIcon, QTableWidgetItem, QAbstractItemView

import pyforms
from pyforms.gui.Controls.ControlBase import ControlBase

__author__ = pyforms.__author__
__credits__ = pyforms.__credits__
__license__ = pyforms.__license__
__version__ = pyforms.__version__
__maintainer__ = pyforms.__maintainer__
__email__ = pyforms.__email__
__status__ = pyforms.__status__
__updated__ = "2016-08-03"

logger = logging.getLogger(__name__)


class ControlList(ControlBase, QWidget):
    """ This class represents a wrapper to the table widget
        It allows to implement a list view
    """

    CELL_VALUE_BEFORE_CHANGE = None  # store value when cell is double clicked

    def __init__(self, label="", defaultValue="", plusFunction=None,
                 minusFunction=None):
        QWidget.__init__(self)

        self._plusFunction = plusFunction
        self._minusFunction = minusFunction
        ControlBase.__init__(self, label, defaultValue)

    def __repr__(self):
        return "ControlList " + str(self._value)

    def initForm(self):
        plusFunction = self._plusFunction
        minusFunction = self._minusFunction

        # Get the current path of the file
        rootPath = os.path.dirname(__file__)
        # Load the UI for the self instance
        uic.loadUi(os.path.join(rootPath, "list.ui"), self)

        self.label = self._label
	self.tableWidget._selectionChangedFname = None
        self.tableWidget.currentCellChanged.connect(
            self.tableWidgetCellChanged)
        self.tableWidget.currentItemChanged.connect(
            self.tableWidgetItemChanged)
        self.tableWidget.itemSelectionChanged.connect(
            self.tableWidgetItemSelectionChanged)
        self.tableWidget.cellDoubleClicked.connect(self.tableWidgetCellDoubleClicked)
        self.tableWidget.model().dataChanged.connect(self._dataChangedEvent)

        if plusFunction is None and minusFunction is None:
            self.bottomBar.hide()
        elif plusFunction is None:
            self.plusButton.hide()
            self.minusButton.pressed.connect(minusFunction)
        elif minusFunction is None:
            self.minusButton.hide()
            self.plusButton.pressed.connect(plusFunction)
        else:
            self.plusButton.pressed.connect(plusFunction)
            self.minusButton.pressed.connect(minusFunction)

    def empty_signal(self, *args, **kwargs):
        """
        Use this function if you want to disconnect a signal temporarily
        """
        pass

    def _dataChangedEvent(self, item):
        self.dataChangedEvent(
            item.row(), item.column(), self.tableWidget.model().data(item))
        self.changed()

    def dataChangedEvent(self, row, col, item):
        pass

    def tableWidgetCellChanged(self, nextRow, nextCol, previousRow,
                               previousCol):
        self.currentCellChanged(nextRow, nextCol, previousRow, previousCol)
        self.changed()

    def tableWidgetItemChanged(self, current, previous):
        self.currentItemChanged(current, previous)
        self.changed()

    def tableWidgetItemSelectionChanged(self):
        self.itemSelectionChanged()

    def itemSelectionChanged(self):
	func_name = self.tableWidget._selectionChangedFname
	if callable(func_name):
		try:
			func_name()
		except:
			import sys
			print sys.exc_info([0])
        pass

    def currentCellChanged(
            self, nextRow, nextCol, previousRow, previousCol):
        pass

    def currentItemChanged(self, current, previous):
        pass

    def tableWidgetCellDoubleClicked(self, row, column):
        """
        (From PyQt) This signal is emitted whenever a cell in the table is double clicked.
        The row and column specified is the cell that was double clicked.

        Besides firing this signal, we save the current value, in case the user needs to know the old value.
        :param row:
        :param column:
        :return:
        """
        self.CELL_VALUE_BEFORE_CHANGE = self.getValue(column, row)
        logger.debug("Cell double clicked. Stored value: %s", self.CELL_VALUE_BEFORE_CHANGE)
        self.cellDoubleClicked(row, column)

    def cellDoubleClicked(self, row, column):
        pass

    def clear(self, headers=False):
        if headers:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)

    def __add__(self, other):

        index = self.tableWidget.rowCount()

        self.tableWidget.insertRow(index)
        if self.tableWidget.currentColumn() < len(other):
            self.tableWidget.setColumnCount(len(other))

        for i in range(0, len(other)):
            v = other[i]
            if isinstance(v, QWidget):
                self.tableWidget.setCellWidget(index, i, v)
            else:
                args = [str(v)] if not hasattr(v, 'icon') else [QIcon(v.icon), str(v)]
                self.tableWidget.setItem(index, i, QTableWidgetItem(*args))

        self.tableWidget.resizeColumnsToContents()
        return self

    def __sub__(self, other):

        if isinstance(other, int):
            if other < 0:
                indexToRemove = self.tableWidget.currentRow()
            else:
                indexToRemove = other
            self.tableWidget.removeRow(indexToRemove)
        return self

    @property
    def horizontalHeaders(self):
        return self._horizontalHeaders

    @horizontalHeaders.setter
    def horizontalHeaders(self, horizontalHeaders):
        """Set horizontal headers in the table list."""

        self._horizontalHeaders = horizontalHeaders

        self.tableWidget.setColumnCount(len(horizontalHeaders))
        self.tableWidget.horizontalHeader().setVisible(True)

        for idx, header in enumerate(horizontalHeaders):
            item = QTableWidgetItem()
            item.setText(header)
            self.tableWidget.setHorizontalHeaderItem(idx, item)

    def setValue(self, column, row, value):
        self.tableWidget.item(row, column).setText(str(value))

    def getValue(self, column, row):
        try:
            return str(self.tableWidget.item(row, column).text())
        except AttributeError as err:
            return self.tableWidget.cellWidget(row, column)
        except AttributeError as err:
            return ''

    def resizeRowsToContents(self):
        self.tableWidget.resizeRowsToContents()

    @property
    def word_wrap(self): return self.tableWidget.wordWrap()
    @word_wrap.setter
    def word_wrap(self, value):
        self.tableWidget.setWordWrap(value)


    def getCurrentRowValue(self):
        currentRow = self.tableWidget.currentRow()
        if not currentRow < 0:
            return self.value[currentRow]
        else:
            return []

    def getCell(self, column, row):
        return self.tableWidget.item(row, column)

    @property
    def readOnly(self):
        return self.tableWidget.editTriggers()

    @readOnly.setter
    def readOnly(self, value):
        if value:
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.tableWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

    @property
    def selectEntireRow(self):
        return self.tableWidget.selectionBehavior()

    @selectEntireRow.setter
    def selectEntireRow(self, value):
        if value:
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        else:
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)

    @property
    def count(self):
        return self.tableWidget.rowCount()

    @property
    def value(self):
        if hasattr(self, 'tableWidget'):
            results = []
            for row in range(self.tableWidget.rowCount()):
                r = []
                for col in range(self.tableWidget.columnCount()):
                    try:
                        r.append(self.getValue(col, row))
                    except Exception as err:
                        logger.debug(str(err))
                        r.append("")
                results.append(r)
            return results
        return self._value

    @value.setter
    def value(self, value):
        self.clear()
        for row in value:
            self += row

    # TODO: implement += on self.value? I want to add a list of tuples to
    # self.value

    @property
    def mouseSelectedRowsIndexes(self):
        result = []
        for index in self.tableWidget.selectedIndexes():
            result.append(index.row())
        return list(set(result))

    @property
    def mouseSelectedRowIndex(self):
        indexes = self.mouseSelectedRowsIndexes
        if len(indexes) > 0:
            return indexes[0]
        else:
            return None

    @property
    def label(self):
        return self.labelWidget.getText()

    @label.setter
    def label(self, value):
        if value != '':
            self.labelWidget.setText(value)
        else:
            self.labelWidget.hide()

    @property
    def form(self):
        return self

    @property
    def iconSize(self):
        return self.tableWidget.iconSize()

    @iconSize.setter
    def iconSize(self, value):
        if isinstance(value, (tuple, list)):
            self.tableWidget.setIconSize(QtCore.QSize(*value))
        else:
            self.tableWidget.setIconSize(QtCore.QSize(value, value))

    @property
    def selectionChangedFname(self): return self.tableWidget._selectionChangedFname

    @selectionChangedFname.setter
    def selectionChangedFname(self, value):
        self.tableWidget._selectionChangedFname = value



