#!/home/david/Desktop/EC521_Project/pytaint/Python-2.7.5-pytaint/python

"""
This vulnerable program uses the Python os.system function which takes in a string, opens a shell and executes the command

Works with Pytaint - taint error triggered
"""

import os
# import taint
import pipes
class temp():
    def tempor():
        return 0

    def ticktick():
        return 1

# class ShellMerit(Merit):
#   '''A string has been cleaned for usage as a shell parameter'''
#   propagation = Merit.FullPropagation

# input() for user input does not work with taint analysis

def fake_sanitize(s):
    return s

def inputed():
    return raw_input()

def main():
    # taint.enable('simple_vuln_config.json')

    e = inputed()
    f = fake_sanitize(e)
    print("Printing e: ", e)

    b = 1 + 1                       # Fillers
    c = 1 + b                       # Fillers
    d = b - c                       # Fillers
    os.system(f)

if __name__ == '__main__':
    main()
    x = 1 + 2
    y = 2 + x 
    
