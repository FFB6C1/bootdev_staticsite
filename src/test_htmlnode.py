import unittest
from htmlnode import (HTMLNode, LeafNode, ParentNode)

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "I am a HTML Node", None, {"href": "http://www.boot.dev"})
        node2 = HTMLNode("h1", "I am a HTML Node", None, {"href": "http://www.boot.dev"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("h1", "I am a HTML Node", None, {"href": "http://www.boot.dev", "target": "_blank"})
        test_str = node.props_to_html(node.props)
        self.assertTrue(test_str)

    def test_leafnode(self):
        node = LeafNode("p", "This is a paragraph")
        node2 = LeafNode("a", "This is a link with no props")
        node3 = LeafNode("a", "This is a link with props", {"href": "http://www.boot.dev"})
        node4 = LeafNode("a", "This is a link with many props", {"href": "http://www.boot.dev", "target": "_blank", "alt": "egg."})
        node5 = LeafNode(None, "This is just text.")
        node6 = LeafNode("b", "This text has unused props.", {"prop": "prop???"})

        print(node4.to_html())
    
    def test_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
)

    def test_nestedparentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode("p", [
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text")
                ])
            ],
        )

        print(node.to_html())
        
    
if __name__ == "__main__":
    unittest.main()