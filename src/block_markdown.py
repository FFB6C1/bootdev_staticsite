import re
from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered list"
block_type_ol = "ordered list"

def markdown_to_blocks(markdown):
    if type(markdown) is not str:
        raise ValueError("markdown-to-blocks: expected string input")
    blocks = markdown.split("\n\n")
    return_blocks = []
    for block in blocks:
        if block.strip() == "":
            continue
        block = block.strip()
        return_blocks.append(block)
    return return_blocks

def block_to_block_type(block):
    if heading_checker(block.lstrip()):
        return block_type_heading
    if block[0:3] == "```" and block[-3::] == "```":
        return block_type_code
    if block[0] in ">*-1":
        split_block = re.split(r"\n", block)
        return line_checker(split_block, block[0])
    return block_type_paragraph

def block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html(block)
    if block_type == block_type_quote:
        return quote_to_html(block)
    if block_type == block_type_code:
        return code_to_html(block)
    if block_type == block_type_heading:
        return heading_to_html(block)
    if block_type == block_type_ol:
        return ol_to_html(block)
    if block_type == block_type_ul:
        return ul_to_html(block)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    content = []
    for block in blocks:
        content.append(block_to_html(block))

    return ParentNode("div", content)

#helper functions
def heading_checker(block):
    if (block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")):
        return True
    return False

def line_checker(lines, check):
    if check == "*" or check == "-":
        check = "*-"
    if check == "1":
        list_num = 1
        for line in lines:
            line = line.lstrip()
            if not line.startswith(f"{list_num}. "):
                return block_type_paragraph
            list_num += 1
        return block_type_ol
    for line in lines:
        line = line.lstrip()
        if line == "" or line[0] not in check or line[1] != " ":
            return block_type_paragraph
    if check == "*-":
        return block_type_ul
    if check == ">":
        return block_type_quote

def create_children(content):
    nodes = text_to_textnodes(content)
    children = []
    for node in nodes:
        child = text_node_to_html_node(node)
        children.append(child)
    return children

def quote_to_html(block):
    lines = block.split("\n")
    content_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("quote_to_html: expected quote to begin each line with '>'")
        content_lines.append(line.lstrip(">").strip())
    content = create_children(" ".join(content_lines))
    return ParentNode("blockquote", content)

def ul_to_html(block):
    items = markdown_stripper(block, block_type_ul)
    content = []
    for item in items:
        content.append(ParentNode("li", create_children(item)))
    return ParentNode("ul", content)

def ol_to_html(block):
    items = markdown_stripper(block, block_type_ol)
    content = []
    for item in items:
        content.append(ParentNode("li", create_children(item)))
    return ParentNode("ol", content)

def code_to_html(block):
    code = markdown_stripper(block, block_type_code)
    content = [ParentNode("code", create_children(code))]
    return ParentNode("pre", content)

def heading_to_html(block):
    heading = markdown_stripper(block, block_type_heading)
    content = create_children(heading[1:])
    return ParentNode(f"h{heading[0]}", content)

def paragraph_to_html(block):
    lines = block.split("\n")
    para = " ".join(lines)
    content = create_children(para)
    return ParentNode("p", content)

def find_h1(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == block_type_heading:
            if markdown_stripper(block, block_type_heading)[0] == "1":
                return markdown_stripper(block, block_type_heading)[1:]
    return False

def markdown_stripper(block, blocktype):
    #returns a string for paragraph, heading, code and quotes and an array for lists
    block = block.lstrip()
    if blocktype == block_type_paragraph:
        return block
    if blocktype == block_type_heading:
        if block.startswith("# "):
            return "1" + block[2::]
        if block.startswith("## "):
            return "2" + block[3::]
        if block.startswith("### "):
            return "3" + block[4::]
        if block.startswith("#### "):
            return "4" + block[5::]
        if block.startswith("##### "):
            return "5" + block[6::]
        if block.startswith("###### "):
            return "6" + block[7::]
    if blocktype == block_type_code:
        return block[3:-3]
    block_lines = block.split("\n")
    if blocktype == block_type_quote or blocktype == block_type_ul:
        for i in range(len(block_lines)):
            block_lines[i] = block_lines[i].lstrip()[2:]
        if blocktype == block_type_quote:
            return "\n".join(block_lines)
        return block_lines
    if blocktype == block_type_ol:
        for i in range(len(block_lines)):
            block_lines[i] = block_lines[i].split(". ")[1]
        return block_lines