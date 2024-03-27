import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

image_re = r"!\[(.*?)\]\((.*?)\)"
link_re = r"\s\[(.*?)\]\((.*?)\)"
ita_re = r"\*(?!\*)"
bold_re = r"\*\*"
code_re = r"`"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if not isinstance(n, TextNode):
            new_nodes.append(n)
        delimiter_checker = re.findall(delimiter, n.text)
        if len(delimiter_checker) == 0:
            new_nodes.append(n)
            continue
        if len(delimiter_checker)%2:
            raise Exception("split_nodes_delimiter: invalid markup format")
        
        split_text = re.split(delimiter, n.text)
        delimiter_start = "^"+delimiter
        delimiter_end = delimiter+"$"
        if re.search(delimiter_end, n.text):
            split_text.pop()
        if re.search(delimiter_start, n.text):
            split_text.pop(0)
            new_text = split_text.pop(0)
            if n.url is None:
                new_nodes.append(TextNode(new_text, text_type))
            else:
                new_nodes.append(TextNode(new_text, text_type, n.url))
        for i in range(0, len(split_text)):
            if i % 2:
                if n.url is None:
                    new_nodes.append(TextNode(split_text[i], text_type))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type, n.url))
            else:
                new_nodes.append(TextNode(split_text[i], n.text_type))
    return new_nodes

def extract_markdown_images(text):
    image_list = re.findall(image_re, text)
    return image_list

def extract_markdown_links(text):
    link_list = re.findall(link_re, text)
    return link_list

def split_nodes_image(old_nodes):  
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        node_images = extract_markdown_images(node.text)
        for image in node_images:
            splitter = f"![{image[0]}]({image[1]})"
            split_text = text.split(splitter, 1)
            if len(split_text) == 2:
                text = split_text[1]
            else:
                text = ""
            new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        node_links = extract_markdown_links(text)
        for link in node_links:
            splitter = f"[{link[0]}]({link[1]})"
            split_text = text.split(splitter, 1)
            if len(split_text) == 2:
                text = split_text[1]
            else:
                text = ""
            new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, bold_re, text_type_bold)
    nodes = split_nodes_delimiter(nodes, ita_re, text_type_italic)
    nodes = split_nodes_delimiter(nodes, code_re, text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes