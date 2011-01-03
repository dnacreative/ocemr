#!/usr/bin/python
#
##########################################################################
#
#    This file is part of OCEMR.
#
#    OCEMR is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OCEMR is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OCEMR.  If not, see <http://www.gnu.org/licenses/>.
#
#
#########################################################################
#       Copyright 2011 Philip Freeman <philip.freeman@gmail.com>
##########################################################################
import sys, csv, re

import util_conf
sys.path = [ util_conf.APP_PATH ] + sys.path

from django.core.management import setup_environ

import settings

setup_environ(settings)

#from ocemr.models import ###
from ocemr.models import SymptomType
reader = csv.reader(open("%s/source_data/EngeyeEMRsymptoms.csv"%(settings.APP_PATH), "rb"))

for row in reader:
	if len(row) < 1: continue
	if row[0] =="": continue
	title=row[0]
	print "[%s] "%(title),
	dt, is_new = SymptomType.objects.get_or_create(title=title)
	if is_new:
		print "{NEW} ",
		dt.save()
	else:
		print "{exists} ",
	print ""
	
