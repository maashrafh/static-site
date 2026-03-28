from enum import Enum

class Bender(Enum):
    AIR_BENDER = "air"
    WATER_BENDER = "water"
    EARTH_BENDER = "earth"
    FIRE_BENDER = "fire"

class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        equal_text = (self.text == other.text)
        equal_type = (self.text_type == other.text_type)
        equal_url = (self.url == other.url)
        if equal_text and equal_type and equal_url:
            return True
        return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
