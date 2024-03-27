import re

from htmlnode import (HTMLNode, ParentNode, LeafNode)

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

valid_types = [
    text_type_text, text_type_bold, text_type_italic,
    text_type_code, text_type_link, text_type_image
]

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(textnode):
    if textnode.text_type not in valid_types:
        raise Exception("Text node's text_type is invalid.")
    if textnode.text_type == text_type_text:
        return LeafNode(None, textnode.text)
    if textnode.text_type == text_type_bold:
        return LeafNode("b", textnode.text)
    if textnode.text_type == text_type_italic:
        return LeafNode("i", textnode.text)
    if textnode.text_type == text_type_code:
        return LeafNode("code", textnode.text)
    if textnode.text_type == text_type_link:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    if textnode.text_type == text_type_image:
        return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})