from database.connection import get_db_connection

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