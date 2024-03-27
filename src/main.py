from copy_tree import duplicate_tree
from pathlib import Path
from textnode import TextNode
from page_generator import generate_page_recursive

def main():
    duplicate_tree(str(Path().absolute()), "/static/", "/public/")
    generate_page_recursive("/content/", "template.html", "/public/")


main()