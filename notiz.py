class Notiz:
    def __init__(self, title, content, image=None, note_id=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.image = image
