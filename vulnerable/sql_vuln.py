"""
This vulnerable program uses an unsanitized SQL execution that is vulnerable to an injection
"""

import sqlite3
def create_table():
    # Create table
    try:
        c.execute('''CREATE TABLE people (name text, age text)''')
        return 0

    except:
        return 0

def insert_into_table(name, age):  # Vulnerable
    # Insert a row of data
    c.execute("INSERT INTO people (name, age) values (?, ?)", (name, age))
    return 0

def close_db():
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return 0


def read_db():
    c.execute('SELECT * FROM people')
    print(c.fetchone())
    return 0



def main():
    global conn
    global c
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    name = input("Please enter a name\n")
    age = input("Please enter the age\n")

    # SQL
    create_table()
    insert_into_table(name, age)
    close_db()



if __name__ == '__main__':
    main()
