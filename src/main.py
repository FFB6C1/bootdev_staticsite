from copy_tree import duplicate_tree
from pathlib import Path
from textnode import TextNode
from page_generator import generate_page

def main():
    duplicate_tree(str(Path().absolute()), "/static/", "/public/")
    generate_page("/content/index.md", "template.html", "/public/index.html")


main()