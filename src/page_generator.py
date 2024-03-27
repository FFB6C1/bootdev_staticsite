from block_markdown import (
    find_h1,
    markdown_to_html_node
)
from pathlib import Path
import os

def extract_title(markdown):
    title = find_h1(markdown)
    if title == False:
        raise Exception("extract_title: markdown doc contains no h1")
    return title

def generate_page(src_path, template_path, dst_path):
    print(f"Generating page at {dst_path}.\nSource: {src_path}\n Template: {template_path}")
    markdown = ""
    page = ""

    src = str(Path().absolute()) + src_path
    dst = str(Path().absolute()) + dst_path

    with open(src) as current_file:
        markdown = current_file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    with open(template_path) as current_file:
        page = current_file.read().replace("{{ Title }}", title).replace("{{ Content }}", content)

    dst_dir_levels = dst_path.split("/")[1:]
    #this code checks each level of the directory exists and creates directories if they do not.
    #theoretically, this should let it create a page several levels deep, even if those levels did not previously exist.
    path_so_far = str(Path().absolute()) + "/"
    for i in range(len(dst_dir_levels)-1):
        path_so_far += dst_dir_levels[i]
        if not os.path.exists(path_so_far):
            os.mkdir(path_so_far)
    if os.path.isfile(dst):
        os.remove(dst)

    new_page = open(dst, "w")
    new_page.write(page)

