import os
import shutil

def duplicate_tree(filepath, src, dst):
    src_path = filepath + src
    dst_path = filepath + dst
    if not os.path.exists(src_path):
        raise Exception(f"duplicate_tree: source path ({src_path}) does not exist")
    if not os.path.exists(dst_path):
        raise Exception(f"duplicate_tree: destination path ({dst_path}) does not exist")
    shutil.rmtree(dst_path)
    os.mkdir(dst_path)
    files_to_copy = os.listdir(src_path)
    for file in files_to_copy:
        current_path = src_path + file
        if os.path.isfile(current_path):
            print(f"Copying {file} from {src_path} to {dst_path}")
            shutil.copyfile(src_path+file, dst_path+file)
        elif os.path.isdir(current_path):
            print(f"Creating new folder at {dst_path + file + "/"}")
            os.mkdir(dst_path + file + "/")
            duplicate_tree(filepath, src + file + "/", dst + file + "/")