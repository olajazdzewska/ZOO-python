class Comment:

    def __init__(self):
        self.text = " "

    def add_comment(self, comment):
        self.text += comment + "\n"

    def clear_comment(self):
        self.text = " "