from enum import Enum
from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
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
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
