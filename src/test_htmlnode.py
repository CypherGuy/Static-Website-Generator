import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "Hello world", [], {})
        self.assertEqual(
            repr(node), f"HTMLNode(None, None, None, None)")

    def test_repr_with_children(self):
        node = HTMLNode("div", "Hello world", ["child1", "child2"], {})
        self.assertEqual(
            repr(node), f"HTMLNode(None, None, None, None)")

    def test_repr_with_props(self):
        node = HTMLNode("div", "Hello world", [], {"class": "my-class"})
        self.assertEqual(
            repr(node), f"HTMLNode(None, None, None, None)")

    def test_repr_with_children_and_props(self):
        node = HTMLNode("div", "Hello world", [
                        "child1", "child2"], {"class": "my-class"})
        self.assertEqual(
            repr(node), f"HTMLNode(None, None, None, None)")

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def parentnode_to_html(self):
        node = ParentNode("div", [LeafNode("p", "Hello, world!")])
        self.assertEqual(node.to_html(), "<div><p>Hello, world!</p></div>")

    def parentnode_to_html_with_props(self):
        node = ParentNode("div", [LeafNode("p", "Hello, world!")], {
                          "class": "my-class"})
        self.assertEqual(
            node.to_html(), "<div class=\"my-class\"><p>Hello, world!</p></div>")


if __name__ == "__main__":
    unittest.main()
