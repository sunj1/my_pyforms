#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from pyforms import settings
from pysettings import conf;

conf += settings

__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = '0.1.7.3'
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Production"

logger = logging.getLogger(__name__)

if conf.PYFORMS_MODE in ['GUI', 'GUI-OPENCSP']:

	from pyforms.gui import Controls
	from pyforms.gui.BaseWidget import BaseWidget

	if conf.PYFORMS_MODE in ['GUI-OPENCSP']:
		from pyforms.gui.appmanager import startApp
	else:
		from pyforms.gui.standaloneManager import startApp

elif conf.PYFORMS_MODE in ['TERMINAL']:

	from pyforms.terminal import Controls
	from pyforms.terminal.BaseWidget import BaseWidget
	from pyforms.terminal.appmanager import startApp


elif conf.PYFORMS_MODE in ['WEB']:

	from pyforms_web.web import Controls
	from pyforms_web.web.BaseWidget import BaseWidget
	from pyforms_web.web.appmanager import startApp
