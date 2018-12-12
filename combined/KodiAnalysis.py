#!/usr/bin/env python3
import os
import sys

lib_path = os.path.abspath('./lib')
sys.path.append(lib_path)
sys.path.append(lib_path + '/xmbc_dummy')
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[1])))
sys.path.append('/home/rjewing/.kodi/addons/script.module.covenant/lib/')

import find_functions, add_decorates

def main():
	full_file = sys.argv[1]
	path, file = os.path.split(sys.argv[1])
    

	print('************ Running Bandit ************')
	os.system('bandit -ll %s > b_output.txt' %(full_file))
	os.system('bandit -ll %s' %(full_file))

	# raw_input()
	input()

	print('************ Parsing Bandit ************')
	d, v = find_functions.find()

	# raw_input()
	input()

	print('************ Patching Files ************')
	for k in d.keys():
		print('Patching %s' % k)
		add_decorates.append_decorate(k)

	if len(sys.argv) > 2:
		f = open('./lib/sanitizers.txt', 'w+')
		for i in sys.argv[2].split(' '):
			f.write(i)
		f.close()

	# raw_input()
	input()

	print('************ Executing %s ************' %file)
	to_exec = path + '/' + file[:-3] + '_cpy.py'
	# print(to_exec)
	print(path)
	os.system('/bin/cp %s %s' %(lib_path + '/decorate_function.py', path))
	#os.system('PYTHONPATH=%s ' %(lib_path) + 'python3 ' + to_exec)


if __name__ == '__main__':
	main()
