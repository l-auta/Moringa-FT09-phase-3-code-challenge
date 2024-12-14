from .connection import get_db_connection

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create authors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create magazines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    # Create articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (id)
        )
    ''')

    # Create authors_magazines relationship table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors_magazines (
            author_id INTEGER,
            magazine_id INTEGER,
            PRIMARY KEY (author_id, magazine_id),
            FOREIGN KEY (author_id) REFERENCES authors (id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (id)
        )
    ''')

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the connection
