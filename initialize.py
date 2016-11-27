import os


def check(path1, path2, replace, is_folder):
    if is_folder and os.path.isdir(path1):
        if replace:
            return True
        elif os.path.isdir(path2):
            return True
        else:
            return False
    elif not is_folder and os.path.exists(path1):
        if replace:
            return True
        elif os.path.isdir(path2):
            return True
        else:
            return False
    else:
        return False

def folder_convert(compressor, input_path, replace=True, output_path=None):
    for content in os.listdir(input_path):
        if is_valid(content):
            if replace:
                compressor.compress(os.path.join(input_path, content))
            else:
                ip = os.path.join(input_path, content)
                op = os.path.join(output_path, content)
                compressor.compress(ip, replace=False, save_path=op)


def file_convert(compressor, input_path, replace=True, output_path=None):
    if is_valid(input_path):
        if replace:
            compressor.compress(input_path)
        else:
            fname = input_path.rsplit('/', 1)
            op = os.path.join(output_path, fname[1])
            compressor.compress(input_path, replace=False, save_path=op)


def is_valid(path):
    p = path.lower()
    return p.endswith('.jpg') or p.endswith('.jpeg') or p.endswith('.png')
