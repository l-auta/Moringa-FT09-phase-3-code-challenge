from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if len(title) == 0:
            raise ValueError("Title must be longer than 0 characters")
        self._title = title
        
        if not isinstance(content, str):
            raise ValueError("Content must be a string")
        self._content = content
        
        self._author_id = author_id
        self._magazine_id = magazine_id

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       (self._title, self._content, self._author_id, self._magazine_id))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def title(self):
        if not hasattr(self, '_title'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM articles WHERE id = ?", (self._id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._title = result[0]
            else:
                raise ValueError("Title not found in database")
        return self._title

    @property
    def content(self):
        if not hasattr(self, '_content'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM articles WHERE id = ?", (self._id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._content = result[0]
            else:
                raise ValueError("Content not found in database")
        return self._content

    @property
    def author(self):
        if not hasattr(self, '_author'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT authors.name
                FROM articles
                INNER JOIN authors ON articles.author_id = authors.id
                WHERE articles.id = ?
            ''', (self._id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._author = result[0]
            else:
                raise ValueError("Author not found in database")
        return self._author

    @property
    def magazine(self):
        if not hasattr(self, '_magazine'):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT magazines.name
                FROM articles
                INNER JOIN magazines ON articles.magazine_id = magazines.id
                WHERE articles.id = ?
            ''', (self._id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self._magazine = result[0]
            else:
                raise ValueError("Magazine not found in database")
        return self._magazine
    
    def __repr__(self):
        return f'<Article {self.title}>'

class Author:
    def __init__(self, id, name):
        self._id = id
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = name

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._fetch_name()
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = value
    
    def _fetch_name(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM authors WHERE id = ?', (self._id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            self._name = result[0]
        else:
            raise ValueError("Name not found in database")
    
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]
    
    
    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine['id'], magazine['name'], magazine['category']) for magazine in magazines]

    def __repr__(self):
        return f'<Author {self.name}>'

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self.name = name
        
        if not isinstance(category, str):
            raise ValueError("Category must be a string")
        if len(category) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self.category = category

    def update_category(self, new_category, cursor):
        if not isinstance(new_category, str):
            raise ValueError("Category must be a string")
        if len(new_category) <= 0:
            raise ValueError("Category must be longer than 0 characters")
        
        cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (new_category, self.id))

    def articles(self, cursor):
        from models.article import Article
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        return [Article(article['id'], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]
    
    def contributors(self, cursor):
        from models.author import Author
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors = cursor.fetchall()
        return [Author(author['id'], author['name']) for author in authors]

    def article_titles(self, cursor):
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles = [row['title'] for row in cursor.fetchall()]
        return titles
    
    def contributing_authors(self, cursor):
        from models.author import Author
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        return [Author(author['id'], author['name']) for author in authors]

    def __repr__(self):
        return f'<Magazine {self.name}>'
