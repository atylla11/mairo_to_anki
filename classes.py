from abc import ABC
from html.parser import HTMLParser


class Note:
    def __init__(self, deck_name, front, back):
        self.deckName = deck_name
        self.modelName = "Basic"
        self.fields = {"Front": front, "Back": back}
        self.tags = []


class MLStripper(HTMLParser, ABC):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)