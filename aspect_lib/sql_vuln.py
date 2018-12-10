"""
This vulnerable program uses an unsanitized SQL execution that is vulnerable to an injection
"""
import aspectlib, sqlite3, sys
from aspectlib import debug
from forbiddenfruit import curse
from types import FunctionType

# check if an object should be decorated
def do_decorate(attr, value):
    return ('__' not in attr and
            isinstance(value, FunctionType) and
            getattr(value, 'decorate', True))

# decorate all instance methods (unless excluded) with the same decorator
def decorate_all(decorator):
    class DecorateAll(type):
        def __new__(cls, name, bases, dct):
            for attr, value in dct.iteritems():
                if do_decorate(attr, value):
                    dct[attr] = decorator(value)
            return super(DecorateAll, cls).__new__(cls, name, bases, dct)
        def __setattr__(self, attr, value):
            if do_decorate(attr, value):
                value = decorator(value)
            super(DecorateAll, self).__setattr__(attr, value)
    return DecorateAll

# decorator to exclude methods
def dont_decorate(f):
    f.decorate = False
    return f


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

def decorator(f):
    """Accept arbitrary arguments, and use them to decorate functions.
    """
    # print("Decorator: ")
    print('>>> ', f)
    def called(*args, **kwargs):
        print('\t', args, kwargs)
        print('----------------')
        result = f(*args, **kwargs)
        print('----------------')
        print('\t', result)
        return result
    # print("calling")
    return called

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



if __name__ == '__main__':
    #aspectlib.weave(sqlite3.Cursor, debug.log(print_to=sys.stdout), lazy=True,)
    #aspectlib.weave(sqlite3.Connection, debug.log(print_to=sys.stdout), lazy=True,)
    #curse(sqlite3, "connect", decorator(sqlite3.connect))

    # curse(sqlite3.Connection, "cursor", decorator(sqlite3.Connection.cursor))
    # decorate_all(decorator)
    # sqlite3.Cursor.execute = decorator(sqlite3.Cursor.execute)
    test = decorator(test)
    main()
