from enum import Enum


class TextType(Enum):
    TEXT = "TextType.TEXT"
    BOLD = "TextType.BOLD"
    ITALIC = "TextType.ITALIC"
    BOLD_ITALIC = "TextType.BOLD_ITALIC"
    CODE = "TextType.CODE"
    LINK = "TextType.LINK"
    IMAGE = "TextType.IMAGE"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
