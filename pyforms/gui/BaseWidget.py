#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: Ricardo Ribeiro
@credits: Ricardo Ribeiro
@license: MIT
@version: 0.0
@maintainer: Ricardo Ribeiro
@email: ricardojvr@gmail.com
@status: Development
@lastEditedBy: Carlos Mão de Ferro (carlos.maodeferro@neuro.fchampalimaud.org)
'''

from pyforms.gui.Controls.ControlBase import ControlBase
from pyforms.gui.Controls.ControlProgress import ControlProgress
import os
import json
import subprocess
import time, sys
from datetime import datetime, timedelta
from PyQt4 import QtGui, QtCore
from pysettings import conf


class FlushFile(object):
	"""Write-only flushing wrapper for file-type objects."""
	def __init__(self, f):
		self.f = f
	def write(self, x):
		self.f.write(x)
		self.f.flush()



class BaseWidget(QtGui.QFrame):
	"""
	The class implements the most basic widget or window.
	"""

	def __init__(self, title='Untitled', parentWindow=None, flag=None):
		if parentWindow is not None and flag is None:
			flag = QtCore.Qt.Dialog

		if parentWindow is None:
			QtGui.QFrame.__init__(self)
		else:
			QtGui.QFrame.__init__(self, parentWindow, flag)

		#self.setObjectName(self.__class__.__name__)
		

		layout = QtGui.QVBoxLayout()
		self.setLayout(layout)
		self.layout().setMargin(0)

		self.title = title

		self._mainmenu = []
		self._splitters = []
		self._tabs = []
		self._formset = None
		self._formLoaded = False
		self.uid = id(self)

		self.setAccessibleName('BaseWidget')

	##########################################################################
	############ Module functions  ###########################################
	##########################################################################


	def initForm(self):
		"""
		Generate the module Form
		"""
		if not self._formLoaded:

			if conf.PYFORMS_MODE in ['GUI-OPENCSP']:
				self._progress = ControlProgress("Progress", 0, 100)
				self._progress.hide()
				if self._formset != None:
					self._formset += ['_progress']

			if self._formset is not None:
				control = self.generatePanel(self._formset)
				self.layout().addWidget(control)
			else:
				allparams = self.formControls
				for key, param in allparams.items():
					param.parent = self
					param.name = key
					self.layout().addWidget(param.form)
			self._formLoaded = True

	def generateTabs(self, formsetDict):
		"""
		Generate QTabWidget for the module form
		@param formset: Tab form configuration
		@type formset: dict
		"""
		tabs = QtGui.QTabWidget(self)
		for key, item in sorted(formsetDict.items()):
			ctrl = self.generatePanel(item)
			tabs.addTab(ctrl, key[key.find(':') + 1:])
		return tabs

	def generatePanel(self, formset):
		"""
		Generate a panel for the module form with all the controls
		formset format example: [('_video', '_arenas', '_run'), {"Player":['_threshold', "_player", "=", "_results", "_query"], "Background image":[(' ', '_selectBackground', '_paintBackground'), '_image']}, "_progress"]
		tuple: will display the controls in the same horizontal line
		list: will display the controls in the same vertical line
		dict: will display the controls in a tab widget
		'||': will plit the controls in a horizontal line
		'=': will plit the controls in a vertical line
		@param formset: Form configuration
		@type formset: list
		"""
		control = None
		if '=' in formset:
			control = QtGui.QSplitter(QtCore.Qt.Vertical)
			tmp = list(formset)
			index = tmp.index('=')
			firstPanel = self.generatePanel(formset[0:index])
			secondPanel = self.generatePanel(formset[index + 1:])
			control.addWidget(firstPanel)
			control.addWidget(secondPanel)
			self._splitters.append(control)
			return control
		elif '||' in formset:
			control = QtGui.QSplitter(QtCore.Qt.Horizontal)
			tmp = list(formset)
			rindex = lindex = index = tmp.index('||')
			rindex -= 1
			rindex += 2
			if isinstance(formset[lindex - 1], int):
				lindex = lindex - 1
			if len(formset) > rindex and isinstance(formset[index + 1], int):
				rindex += 1
			firstPanel = self.generatePanel(formset[0:lindex])
			secondPanel = self.generatePanel(formset[rindex:])
			if isinstance(formset[index - 1], int):
				firstPanel.setMaximumWidth(formset[index - 1])
			if isinstance(formset[index + 1], int):
				secondPanel.setMaximumWidth(formset[index + 1])
			control.addWidget(firstPanel)
			control.addWidget(secondPanel)
			self._splitters.append(control)
			return control
		control = QtGui.QFrame(self)
		layout = None
		if type(formset) is tuple:
			layout = QtGui.QHBoxLayout()
			for row in formset:
				if isinstance(row, (list, tuple)):
					panel = self.generatePanel(row)
					layout.addWidget(panel)
				elif row == " ":
					spacer = QtGui.QSpacerItem(
						40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
					layout.addItem(spacer)
				elif type(row) is dict:
					c = self.generateTabs(row)
					layout.addWidget(c)
					self._tabs.append(c)
				else:
					param = self.formControls.get(row, None)
					if param is None:
						label = QtGui.QLabel()
						label.setSizePolicy(
							QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
						#layout.addWidget( label )

						if row.startswith('info:'):
							label.setText(row[5:])
							font = QtGui.QFont()
							font.setPointSize(10)
							label.setFont(font)
							label.setAccessibleName('info')
						elif row.startswith('h1:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(17)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h1')
						elif row.startswith('h2:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(16)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h2')
						elif row.startswith('h3:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(15)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h3')
						elif row.startswith('h4:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(14)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h4')
						elif row.startswith('h5:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(12)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h5')
						else:
							label.setText(row)
							font = QtGui.QFont()
							font.setPointSize(10)
							label.setFont(font)
							label.setAccessibleName('msg')

						layout.addWidget(label)
					else:
						param.parent = self
						param.name = row
						layout.addWidget(param.form)
		elif type(formset) is list:
			layout = QtGui.QVBoxLayout()
			for row in formset:
				if isinstance(row, (list, tuple)):
					panel = self.generatePanel(row)
					layout.addWidget(panel)
				elif row == " ":
					spacer = QtGui.QSpacerItem(
						20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
					layout.addItem(spacer)
				elif type(row) is dict:
					c = self.generateTabs(row)
					layout.addWidget(c)
					self._tabs.append(c)
				else:
					param = self.formControls.get(row, None)
					if param is None:
						label = QtGui.QLabel()
						label.setSizePolicy(
							QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
						label.resize(30, 30)
						#layout.addWidget( label )

						if row.startswith('info:'):
							label.setText(row[5:])
							font = QtGui.QFont()
							font.setPointSize(10)
							label.setFont(font)
							label.setAccessibleName('info')
						elif row.startswith('h1:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(17)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h1')
						elif row.startswith('h2:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(16)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h2')
						elif row.startswith('h3:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(15)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h3')
						elif row.startswith('h4:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(14)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h4')
						elif row.startswith('h5:'):
							label.setText(row[3:])
							font = QtGui.QFont()
							font.setPointSize(12)
							font.setBold(True)
							label.setFont(font)
							label.setAccessibleName('h5')
						else:
							label.setText(row)
							font = QtGui.QFont()
							font.setPointSize(10)
							label.setFont(font)
							label.setAccessibleName('msg')

						layout.addWidget(label)
					else:
						param.parent = self
						param.name = row
						layout.addWidget(param.form)
		layout.setMargin(0)
		control.setLayout(layout)
		return control

	##########################################################################
	############ Parent class functions reemplementation #####################
	##########################################################################

	def show(self):
		"""
		It shows the 
		"""
		self.initForm()
		super(BaseWidget, self).show()


	##########################################################################
	############ Properties ##################################################
	##########################################################################

	@property
	def formControls(self):
		"""
		Return all the form controls from the the module
		"""
		result = {}
		for name, var in vars(self).items():
			try:
				if isinstance(var, ControlBase): 
					result[name] = var
			except:
				pass
		return result

	def start_progress(self, total=100):
		self._progress.max = total
		self._progress.min = 0
		self._progress.value = 0
		self._processing_count = 0
		self._processing_initial_time = time.time()
		self._progress.show()

	def update_progress(self, progress=1):
		self._progress.value = self._processing_count
		self._processing_count += progress

		div = int(self._progress.max / 400)
		if div == 0:
			div = 1
		if (self._processing_count % div) == 0:
			self._processing_last_time = time.time()
			total_passed_time = self._processing_last_time - \
				self._processing_initial_time
			remaining_time = (
				(self._progress.max * total_passed_time) / self._processing_count) - total_passed_time
			time_remaining = datetime(
				1, 1, 1) + timedelta(seconds=remaining_time)
			time_elapsed = datetime(
				1, 1, 1) + timedelta(seconds=(total_passed_time))

			values = (time_elapsed.day - 1, time_elapsed.hour, time_elapsed.minute, time_elapsed.second,
					  time_remaining.day -
					  1, time_remaining.hour, time_remaining.minute, time_remaining.second,
					  (float(self._processing_count) / float(self._progress.max)
					   ) * 100.0, self._processing_count, self._progress.max,
					  self._processing_count / total_passed_time)
			self._progress.label = "Elapsed: %d:%d:%d:%d; Remaining: %d:%d:%d:%d; Processed %0.2f %%  (%d/%d); Cicles per second: %0.3f" % values

		QtGui.QApplication.processEvents()

	def end_progress(self):
		# self.update_progress()
		self._progress.value = self._progress.max
		self._progress.hide()

	def executeCommand(self, cmd, cwd=None):
		if cwd is not None:
			currentdirectory = os.getcwd()
			os.chdir(cwd)

		out = FlushFile(sys.__stdout__)

		proc = subprocess.Popen(cmd, stdout=out, stderr=out)
		(output, error) = proc.communicate()
		if cwd is not None:
			os.chdir(currentdirectory)
		if error:
			print('Error: ' + error)
		return output

	@property
	def form(self):
		return self

	@property
	def title(self): return self.windowTitle()

	@title.setter
	def title(self, value): self.setWindowTitle(value)

	@property
	def mainmenu(self): return self._mainmenu

	@mainmenu.setter
	def mainmenu(self, value): self._mainmenu = value

	@property
	def formset(self): return self._formset

	@formset.setter
	def formset(self, value): self._formset = value

	@property
	def uid(self): return self._uid

	@uid.setter
	def uid(self, value): self._uid = value

	def save(self, data):
		allparams = self.formControls
		for name, param in allparams.items():
			data[name] = {}
			param.save(data[name])

	def saveWindow(self):
		allparams = self.formControls
		data = {}
		self.save(data)

		filename = QtGui.QFileDialog.getSaveFileName(self, 'Select file')

		with open(filename, 'w') as output_file:
			json.dump(data, output_file)

	def loadWindowData(self, filename):
		with open(filename, 'r') as pkl_file:
			project_data = json.load(pkl_file)
		data = dict(project_data)
		self.load(data)

	def load(self, data):
		allparams = self.formControls
		for name, param in allparams.items():
			if name in data:
				param.load(data[name])
		self.initForm()

	def loadWindow(self):
		filename = QtGui.QFileDialog.getOpenFileNames(self, 'Select file')
		self.loadWindowData(str(filename[0]))

	def closeEvent(self, event):
		self.beforeClose()
		super(BaseWidget, self).closeEvent(event)

	def beforeClose(self):
		""" 
		Do something before closing widget 
		Note that the window will be closed anyway    
		"""
		pass
