from html import escape
from typing import List, Optional

from textnode import TextType


class HTMLNode:
    def __init__(
        self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[List] = None, props: Optional[dict] = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return NotImplementedError("Not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        # Properly format the attributes, escaping special characters
        return "".join(f' {k}="{escape(str(v))}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode(None, None, None, None)"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required")

        escaped_value = escape(self.value)
        props_html = self.props_to_html()

        # Handle different cases
        if self.tag is None:
            return escaped_value

        else:
            return f"<{self.tag}{props_html}>{escaped_value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props: Optional[dict] = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.children is None:
            raise ValueError("Children are required")

        if self.tag is None:
            raise ValueError("Tag is required")

        else:
            # Convert all children nodes to HTML recursively
            children_html = "".join(child.to_html() for child in self.children)

            # Properly format the attributes, escaping special characters
            props_html = self.props_to_html()

            return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"


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
