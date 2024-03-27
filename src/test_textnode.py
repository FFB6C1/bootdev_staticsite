import unittest

from textnode import (TextNode)
from htmlnode import (HTMLNode, LeafNode, ParentNode)

class TestTextMode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", "bold")
        node2 = TextNode("this is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("this is a text node", "bold", "http://www.test.url")
        node2 = TextNode("this is a text node", "bold", "http://www.test.url")
        self.assertEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This textnode has no url", "italic")
        node2 = TextNode("This textnode has no url", "italic", None)
        self.assertEqual(node, node2)

    def test_falsy_url(self):
        node = TextNode("This textnode has no url", "italic")
        node2 = TextNode("This textnode has no url", "italic", "")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()