'''
**********************************************************************
* Filename    : filedb.py
* Description : A simple file based database.
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
**********************************************************************
'''

import importlib
import os
import mydb

class fileDB(object):
	"""A file based database.

    A file based database, read and write arguements in the specific file.
    """
	def __init__(self, db_file=None):
		'''Init the db_file is a file to save the datas.'''

		# Check if db_file is defined
		if db_file != None:
			self.db_file = db_file.split('.')[0]
			#self.db_file = 'server.' + self.db_file
			self.db = importlib.import_module(self.db_file)
		else:
			self.db = mydb
			db_file = 'mydb.py'
			self.db_path = os.path.join(os.path.dirname(self.db.__file__), db_file)


	def get(self, name, default_value=None):
		"""Get value by data's name. Default value is for the arguemants do not exist"""
		try:
			value = getattr(self.db, name)
		except AttributeError:
			value = default_value
		return value
	
	def set(self, name, value):
		"""Set value by data's name. Or create one if the arguement does not exist"""
	    # Check the value type
		if isinstance(value, str):
			value = "'%s'" % value
		else:
			value = "%s" % str(value)

		# Read the file
		cf = open(self.db_path,'r')
		lines=cf.readlines()
		cf.close()
		file_len=len(lines)-1
		flag = False
		# Find the arguement and set the value
		for i in range(file_len):
			if lines[i][0] != '#':
				if lines[i].split('=')[0].strip() == name:
					lines[i] = '%s = %s\n\n' % (name, value)
					flag = True
		# If arguement does not exist, create one
		if not flag:
			lines.append('%s = %s\n\n' % (name, value))

		# Save the file
		cf = open(self.db_path,'w')
		cf.writelines(lines)
		cf.close()
