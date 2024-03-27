from block_markdown import (
    find_h1,
    markdown_to_html_node
)
from pathlib import Path
import os
import shutil

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
    #this functionality is no longer necessary, as this function will only be called via generate_page_recursive, which handles this
    #however I have chosen to leave it in so that this function can generate a standalone page in a nested directory, because I think it's neat and this is my code.
    path_so_far = str(Path().absolute()) + "/"
    for i in range(len(dst_dir_levels)-1):
        path_so_far += dst_dir_levels[i]
        if not os.path.exists(path_so_far):
            os.mkdir(path_so_far)
    if os.path.isfile(dst):
        os.remove(dst)

    new_page = open(dst, "w")
    new_page.write(page)

def generate_page_recursive(dir_path_content, template_path, dst_dir_path):
    base_path = str(Path().absolute())
    #check to make sure source path and template exist.
    if not os.path.exists(base_path + dir_path_content):
        raise Exception("generate_page_recursive: source path does not exist.")
    if not os.path.exists(base_path + "/" + template_path):
        raise Exception("generate_page_recursive: template does not exist")
    #if destination path does not exist (n/a in this situation, but could happen if this was run without copying the contents of static to public first)
    if not os.path.exists(base_path + dst_dir_path):
        print(f"creating new directory: {dst_dir_path}...")
        os.mkdir(base_path + dst_dir_path)
    #use listdir to get a list of files in the content directory
    files = os.listdir(base_path + dir_path_content)
    #iterate through files in the content directory
    for file in files:
        if os.path.isfile(base_path + dir_path_content + file):
            #get the filename without extention using split
            filename = file.split(".")[0]
            #use that filename to create a target file for the generate_page function
            generate_page(dir_path_content + file, template_path, dst_dir_path + filename + ".html")
        elif os.path.isdir(base_path + dir_path_content + file):
            #make a directory, then use it as the destination for generate_page_recursive
            print(f"creating directory {file} at {dst_dir_path}")
            os.mkdir(base_path + dst_dir_path + file)
            generate_page_recursive(dir_path_content + file + "/", template_path, dst_dir_path + file + "/")



