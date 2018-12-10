import os
import sys

import find_functions, add_decorates

def main():
    file = sys.argv[1]
    print('************ Running Bandit ************')
    os.system('bandit %s > b_output.txt' %(file))
    os.system('bandit %s' %(file))

    input()

    print('************ Parsing Bandit ************')
    d = find_functions.find()

    input()

    print('************ Patching Files ************')
    for k in d.keys():
        print('Patching %s' % k)
        add_decorates.append_decorate(k)

    input()

    print('************ Executing %s ************' %file)
    to_exec = file[:-3] + '_cpy.py'
    print(to_exec)
    os.system("/Applications/Kodi.app/Contents/MacOS/Kodi")


if __name__ == '__main__':
    main()
