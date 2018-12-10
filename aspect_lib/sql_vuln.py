"""
This vulnerable program uses an unsanitized SQL execution that is vulnerable to an injection
"""
import sqlite3, sys
# from forbiddenfruit import curse
# from types import FunctionType

import test2 



def create_table():
    # Create table
    try:
        c.execute('''CREATE TABLE people (name text, age text)''')
        return 0

    except:
        return 0

def insert_into_table(name, age):  # Vulnerable
    # Insert a row of data
    c.execute("INSERT INTO people (name, age) VALUES (?, ?)", (name, age))
    return 0

def close_db():
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return 0

def read_db(name):
    c.execute("SELECT * FROM people WHERE name = '%s'" % name)
    print(c.fetchone())
    return 0

def test(*args, **kwargs):
    print("Hello world!")

def main():
    test()
    global conn
    global c
    conn = sqlite3.connect('data.db')
    
    c = conn.cursor()
    # curse(c, "execute", decorator(sqlite3.Cursor.execute))
#    c.test("testing")
#    aspectlib.weave(c, debug.log(print_to=sys.stdout), lazy=True,)

    name = input("Please enter a name\n")
    age = input("Please enter the age\n")


    # SQL
    create_table()
    insert_into_table(name, age)
    read_db(name)
    close_db()

    test2.square(5)



if __name__ == '__main__':
    #aspectlib.weave(sqlite3.Cursor, debug.log(print_to=sys.stdout), lazy=True,)
    #aspectlib.weave(sqlite3.Connection, debug.log(print_to=sys.stdout), lazy=True,)
    #curse(sqlite3, "connect", decorator(sqlite3.connect))
    print(globals())
    from decorate_function import decorate; decorate(globals())

    main()
