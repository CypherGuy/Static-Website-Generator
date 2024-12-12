from typing import List


class HTMLNode:
    def __init__(self, tag=None, value=None, children: List = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        return NotImplementedError("Not implemented")

    def props_to_html(self):
        return " ".join([f" {k}= {v}" for k, v in self.props.items()])

    def __repr__(self):
        return f"HTMLNode(None, None, None, None)"
