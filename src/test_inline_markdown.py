import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)

class MarkdownTestNode(unittest.TestCase):
    def test_delimiter_1(self):
        node = TextNode("This is a **bold part of** the *text", "text")
        new_textnodes = split_nodes_delimiter([node], r"\*\*", "bold")

        expected = [
            TextNode("This is a ", "text"),
            TextNode("bold part of", "bold"),
            TextNode(" the *text", "text")
        ]
        self.assertEqual(new_textnodes, expected)

    def test_delimiter_2(self):
        nodes = [
            TextNode("This is a **bold part of** the text", "text"), 
            TextNode("**bold of you** to start with the formatting", "text"),
            TextNode("let's end this **boldly**", "text")]
        new_nodes = split_nodes_delimiter(nodes, r"\*\*", "bold")

        expected = [
            TextNode("This is a ", "text"),
            TextNode("bold part of", "bold"),
            TextNode(" the text", "text"),
            TextNode("bold of you", "bold"),
            TextNode(" to start with the formatting", "text"),
            TextNode("let's end this ", "text"),
            TextNode("boldly", "bold")
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_markdown_images(self):
        text = "this is text containing two ![image](http://www.imagehost.com/image.jpg) images ![image2](http://www.imagehost.com/image2.png)"
        expected_return = [
            ("image", "http://www.imagehost.com/image.jpg"), 
            ("image2", "http://www.imagehost.com/image2.png")]
        self.assertEqual(extract_markdown_images(text), expected_return)

    def test_markdown_links(self):
        text = "this is text containing two [link1](http://www.imagehost.com/image.jpg) links ![I lied this is an image](http://www.imagehost.come/image2.png)"
        expected_return = [("link1", "http://www.imagehost.com/image.jpg")]
        self.assertEqual(extract_markdown_links(text), expected_return)

    def test_image_split_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )

        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, expected)

    def test_image_split_nodes2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and more text",
            text_type_text,
        )

        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" and more text", text_type_text),
        ]
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, expected)

    def test_link_split_nodes(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )

        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_link, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, expected)

    def test_link_split_nodes2(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png) and more text",
            text_type_text,
        )

        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_link, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" and more text", text_type_text),
        ]
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes(self):
        input_text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected_output = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        actual_output = text_to_textnodes(input_text)
        self.assertEqual(expected_output, actual_output)