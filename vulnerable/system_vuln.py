"""
This vulnerable program uses the Python os.system function which takes in a string, opens a shell and executes the command
"""

import os

def main():
    a = input("Enter a command\n")
    b = 1 + 1                       # Fillers
    c = 1 + b                       # Fillers
    d = b - c                       # Fillers
    os.system(a)



if __name__ == '__main__':
    main()