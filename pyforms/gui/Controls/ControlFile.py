#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms.gui.Controls.ControlText import ControlText
import pyforms.Utils.tools as tools
from PyQt4 import uic
from PyQt4.QtGui import QFileDialog

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Ricardo Ribeiro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlFile(ControlText):

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__, "fileInput.ui")
        self._form = uic.loadUi(control_path)
        self._form.label.setText(self._label)        
        self._form.pushButton.clicked.connect(self.pushButton_clicked)
	self.file_save_mode = False

    def pushButton_clicked(self):
	if self.file_save_mode:
		value = str(QFileDialog.getSaveFileName(
			self._form, self._label, self.value))
	else:
		value = str(QFileDialog.getOpenFileName(
			self._form, self._label, self.value))
        if value:
            self.value = value

    @property
    def parent(self): return ControlText.parent.fget(self, value)

    @parent.setter
    def parent(self, value):
        ControlText.parent.fset(self, value)


    @property
    def fileSaveMode(self): return self.file_save_mode

    @fileSaveMode.setter
    def fileSaveMode(self, value):
	self.file_save_mode = bool(value)

    @property
    def buttonLabel(self): return self._form.pushButton.text()

    @buttonLabel.setter
    def buttonLabel(self, value):
	self._form.pushButton.setText(str(value))

