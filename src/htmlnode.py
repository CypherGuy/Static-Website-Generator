from html import escape
from typing import List, Optional
from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List] = None, props: Optional[dict] = None):
        # Set defaults for missing arguments
        # You can default to 'div' if necessary
        self.tag = tag if tag is not None else None
        self.value = value if value is not None else None
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        if not self.children:
            return f"<{self.tag}{self.props_to_html()}></{self.tag}>"
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {k}="{escape(str(v))}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode(None, None, None, None)"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            return ""
        escaped_value = escape(self.value) if self.value else ""
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{escaped_value}</{self.tag}>" if self.tag else escaped_value


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props: Optional[dict] = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.children:
            return f"<{self.tag}{self.props_to_html()}></{self.tag}>"
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url})
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    else:
        return LeafNode(None, text_node.text)
