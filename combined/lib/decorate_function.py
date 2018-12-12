import types
import inspect
import os
import sys

sys.path.append('/home/rjewing/Schoolwork/current/EC521/project/EC521_FinalProject/combined/lib/')

import find_functions

_, d = find_functions.find()
print(d)
funcs = []
for k1, v1 in d.items():
	funcs.append((k1, v1))
print(funcs)
# funcs = ['system', 'exec', 'create_table', 'insert_into_table', 'callExec', 'SQLVuln', 'read_db', 'Sockets']
sanitizers = find_functions.get_sanitizers()
print(sanitizers)

fd = open('/tmp/kodi_analysis.txt', 'w+')
fd.write('--- Kodi Analysis Summary---\n')
fd.close()

def sanitizer(f, var):
	def called(*args, **kwargs):
		with open('/tmp/kodi_analysis.txt', 'a') as file:
			file.write('>>> SANITIZER ' + str(f) + ' using variable ' + str(var) + '\n')
			file.write('args: %s\nkwargs: %s\n' %(args, kwargs))
			file.write('----------------\n')

		# sys.stdout = file 
		result = f(*args, **kwargs)
		with open('/tmp/kodi_analysis.txt', 'a') as file:
			file.write('----------------\n')
			file.write('returned: %s of type %s\n' %(result, type(result)))
			file.write('<<< SANITIZER ' + str(f) + ' using variable ' + str(var) + '\n')
			file.write('\n')
		return result
	return called




def decorator(f, var):
	"""Accept arbitrary arguments, and use them to decorate functions.
	"""
	def called(*args, **kwargs):
		with open('/tmp/kodi_analysis.txt', 'a') as file:
			file.write('>>> ' + str(f) + ' using variable ' + str(var) + '\n')
			file.write('args: %s\nkwargs: %s\n' %(args, kwargs))
			file.write('----------------\n')
		# sys.stdout = file
		result = f(*args, **kwargs)
		with open('/tmp/kodi_analysis.txt', 'a') as file:
			file.write('----------------\n')
			file.write('returned: %s of type %s\n' %(result, type(result)))
			file.write('<<< ' + str(f) + ' using variable ' + str(var) + '\n')
			file.write('\n')
		#print('>>> ' + str(f))
		#print('args: %s\nkwargs: %s' %(args, kwargs))
		#print('----------------')
		#result = f(*args, **kwargs)
		#print('----------------')
		#print('returned: %s of type %s' %(result, type(result)))
		#print('<<< ' + str(f))
		#print('\n')
		return result
	#print("calling %s" %f)
	return called

def decorate(globals=None, decor=None):
	if decor is None:
		decor = ['decorator']
	for name, obj in list(globals.items()):
		if (isinstance(obj, types.FunctionType)
			or isinstance(obj, types.BuiltinFunctionType)
			or isinstance(obj, types.MethodType)
			or isinstance(obj, types.BuiltinMethodType)):
				for i in funcs:
					if name in i[1]:
						i[1].remove(name)
						if name in sanitizers:
							globals[name] = sanitizer(obj, i[0])
						else:
							globals[name] = decorator(obj, i[0])
		# elif inspect.ismethoddescriptor(obj) and name in funcs:
		#     globals[name].__init__ = decorator(globals[name].__init__)
		elif (isinstance(obj, types.ModuleType) or inspect.isclass(obj)) and name not in decor:
			# file.write('\n\n>>>>>>>', name)
			# print(name, obj)
			decor.append(name)
			decorate(obj.__dict__, decor)
