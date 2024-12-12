import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            repr(node), "TextNode(This is a text node, TextType.BOLD, None)")

    def test_repr_with_url(self):
        node = TextNode("This is a text node",
                        TextType.BOLD, "https://example.com")
        self.assertEqual(
            repr(node), "TextNode(This is a text node, TextType.BOLD, https://example.com)")

    def test_repr_with_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(
            repr(node), "TextNode(This is a text node, TextType.BOLD, None)")


if __name__ == "__main__":
    unittest.main()
