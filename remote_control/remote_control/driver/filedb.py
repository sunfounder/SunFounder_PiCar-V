import importlib
import os
import mydb

class fileDB(object):
	def __init__(self, db_file=None):
		if db_file != None:
			self.db_file = db_file.split('.')[0]
			#self.db_file = 'server.' + self.db_file
			self.db = importlib.import_module(self.db_file)
		else:
			self.db = mydb
			db_file = 'mydb.py'
			self.db_path = os.path.join(os.path.dirname(self.db.__file__), db_file)

	def get(self, name, default_value=None):
		try:
			value = getattr(self.db, name)
		except AttributeError:
			value = default_value
		return value
	
	def set(self, name, value):
		if isinstance(value, str):
			value = "'%s'" % value
		else:
			value = "%s" % str(value)
		cf = open(self.db_path,'r')
		lines=cf.readlines()
		cf.close()
		file_len=len(lines)-1
		flag = False
		for i in range(file_len):
			if lines[i][0] != '#':
				if lines[i].split('=')[0].strip() == name:
					lines[i] = '%s = %s\n\n' % (name, value)
					flag = True
		if not flag:
			lines.append('%s = %s\n\n' % (name, value))

		cf = open(self.db_path,'w')
		cf.writelines(lines)
		cf.close()
