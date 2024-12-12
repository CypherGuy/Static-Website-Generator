from html import escape
from typing import List, Optional


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
        super().__init__(tag, value, props)

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
