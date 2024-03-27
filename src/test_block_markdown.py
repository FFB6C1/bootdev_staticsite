import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import (
    block_type_code,
    block_type_heading,
    block_type_ol,
    block_type_quote,
    block_type_ul,
    markdown_to_blocks,
    block_to_block_type,
    markdown_stripper,
    quote_to_html,
    ul_to_html,
    ol_to_html,
    code_to_html,
    heading_to_html,
    paragraph_to_html,
    markdown_to_html_node,
    )

class BlockMarkdownTestNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = ("# This is a heading"+"\n\n"+
                "            This is a paragraph of text. It has some **bold** and "+
                "*italic* words inside of it."+"\n\n \n\n"
                "* This is a list item"+"\n"
                "* This is another list item")
        expected = ["# This is a heading",
                "This is a paragraph of text. It has some **bold** and "+
                "*italic* words inside of it.",
                "* This is a list item\n"+
                "* This is another list item"]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_block_to_block_type(self):
        block = "\n".join(["1. Hello",
                           "2. this is",
                           "    3. an ordered list"])
        block_header = "   ### block!"
        self.assertEqual(block_to_block_type(block), block_type_ol)

    def test_markdown_stripper(self):
        text = "\n".join(["* Hello",
                           "* this is",
                           "* an unordered list"])
        expected = ["Hello", "this is", "an unordered list"]
        self.assertEqual(markdown_stripper(text, block_type_ul), expected)

    def test_quote_to_html(self):
        quote = "\n".join(["> Hello,",
                           "> this is",
                           "> a quote."])
        expected = " ".join(["<blockquote>Hello,",
                              "this is",
                              "a quote.</blockquote>"])
        self.assertEqual(quote_to_html(quote).to_html(), expected)
    
    def test_ul_to_html(self):
        ul = "\n".join(["* Hello",
                        "* I am",
                        "* a list."])
        expected = "".join(["<ul><li>Hello</li>",
                              "<li>I am</li>",
                              "<li>a list.</li></ul>"])
        self.assertEqual(ul_to_html(ul).to_html(), expected)

    def test_ol_to_html(self):
        ol = "\n".join(["1. Hello",
                        "2. I am",
                        "3. a list."])
        expected = "".join(["<ol><li>Hello</li>",
                              "<li>I am</li>",
                              "<li>a list.</li></ol>"])
        self.assertEqual(ol_to_html(ol).to_html(), expected)

    def test_code_to_html(self):
        code = "```this is code```"
        expected = "<pre><code>this is code</code></pre>"
        self.assertEqual(code_to_html(code).to_html(), expected)

    def test_heading_to_html(self):
        heading = "### this is a heading (h3)"
        expected = "<h3>this is a heading (h3)</h3>"
        self.assertEqual(heading_to_html(heading).to_html(), expected)

    def test_paragraph_to_html(self):
        paragraph = "this is a paragraph."
        expected = "<p>this is a paragraph.</p>"
        self.assertEqual(paragraph_to_html(paragraph).to_html(), expected)

    def test_markdown_to_html_node(self):
        markdown = ("# This is a heading"+"\n\n"+
                "            This is a paragraph of text. It has some **bold** and "+
                "*italic* words inside of it."+"\n\n \n\n"
                "* This is a list item"+"\n"
                "* This is another list item")
        print(markdown_to_html_node(markdown).to_html())