"""
This vulnerable program uses the Python exec function which takes in a string and executes it using python3
"""

import aspectlib, sys
import __builtin__
from aspectlib import debug


def main():
	a = input("Enter a command\n")

	b = 1 + 1                       # Fillers
	c = 1 + b                       # Fillers
	d = b - c                       # Fillers
	exec(a)



if __name__ == '__main__':
	aspectlib.weave(exec, debug.log(print_to=sys.stdout), lazy=True,)
	main()