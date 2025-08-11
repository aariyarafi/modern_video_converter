import os

def get_file_extension(filepath):
    return os.path.splitext(filepath)[1].lower()

def is_valid_video_file(filepath, supported_formats):
    return os.path.isfile(filepath) and get_file_extension(filepath) in supported_formats

def get_output_filepath(input_filepath, output_dir, output_format):
    filename = os.path.splitext(os.path.basename(input_filepath))[0]
    return os.path.join(output_dir, f"{filename}{output_format}")

