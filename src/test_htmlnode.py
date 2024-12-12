import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
