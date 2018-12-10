import fileinput
from shutil import copyfile
import sys

def append_decorate(filename):
    string = filename[:-3] + '_cpy.py'
    copyfile(filename, string)  
    processing_foo1s = False
    placed_in = 0

    for line in fileinput.input(string, inplace=1):
        if line.startswith("if __name__"):
            processing_foo1s = True
        else:
            if processing_foo1s:
                print "\tfrom decorate_function import decorate; decorate(globals())"
                placed_in = 1
            processing_foo1s = False
        print line,

    if not placed_in:
        with open(string, "a") as myfile:
            myfile.write("from decorate_function import decorate; decorate(globals())")

def main():
    filename = sys.argv[1]
    append_decorate(filename)

if __name__ == '__main__':
    main()
