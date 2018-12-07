import aspectlib, sys
from aspectlib import debug
import sqlite3

import sql_vuln

aspectlib.weave(sqlite3.Cursor, debug.log(print_to=sys.stdout, stacktrace=None,), lazy=True,)

sql_vuln.main()