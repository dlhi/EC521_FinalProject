"""
This vulnerable program uses an unsanitized SQL execution that is vulnerable to an injection
"""
import aspectlib, sqlite3, sys
from aspectlib import debug

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



def main():

    global conn
    global c
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    

    name = raw_input("Please enter a name\n")
    age = raw_input("Please enter the age\n")


    # SQL
    create_table()
    insert_into_table(name, age)
    read_db(name)
    close_db()



if __name__ == '__main__':
    # aspectlib.weave(sqlite3.Cursor, debug.log(print_to=sys.stdout), lazy=True,)
    main()
