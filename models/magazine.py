class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"Magazine(id={self.id}, name={self.name}, category={self.category})"
