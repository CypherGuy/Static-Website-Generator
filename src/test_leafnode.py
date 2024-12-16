import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_to_html_with_props(self):
        node = LeafNode("p", "Bye world", {"class": "my-class"})
        self.assertEqual(
            node.to_html(), '<p class="my-class">Bye world</p>')


if __name__ == "__main__":
    unittest.main()
