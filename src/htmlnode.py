from html import escape
from typing import List, Optional

from textnode import TextNode, TextType


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of nodes into multiple nodes if they have the delimiter as text.

    For example, if delimiter is ' ', then the following node:
        <p>Hello   world</p>
    becomes:
        <p>Hello</p>
        <p> </p>
        <p>world</p>

    :param old_nodes: The list of nodes to split.
    :param delimiter: The delimiter to split the text nodes by.
    :param text_type: The text type to use for the new delimiter nodes.
    :return: A new list of nodes with the delimiter nodes inserted.
    """
    new_nodes = []

    for node in old_nodes:
        if isinstance(node, TextNode) and delimiter in node.text:
            parts = node.text.split(delimiter)
            is_inside_delimiter = False  # Tracks whether we are inside a delimiter block

            for i, part in enumerate(parts):
                if part:
                    # Add text as a normal TextNode, alternating types
                    new_nodes.append(
                        TextNode(part, text_type if is_inside_delimiter else TextType.TEXT))
                    is_inside_delimiter = not is_inside_delimiter

                if i < len(parts) - 1:  # This line is to avoid adding the delimiter at the end
                    # Add the delimiter node
                    new_nodes.append(
                        TextNode(delimiter, text_type if is_inside_delimiter else TextType.TEXT))
        else:
            # Non-text nodes are added as-is
            new_nodes.append(node)

    return new_nodes
