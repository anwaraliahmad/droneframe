"""Handles the CLI facing logic of the program.

Raises:
    OSError: Valid file/directory doesn't exist at path
    argparse.ArgumentTypeError: Invalid argument
"""
import argparse
import os
import sys
import subprocess
from .droneframe import run

ARG_MSG = '''Extract frames (JPG) into a folder from drone footage (MP4 at a specific framerate and
populate them with matching metadata (from the corresponding SRT file).'''
VID_MSG = 'Path to the drone video.'
SRT_MSG = '''Path to the SRT metadata file. Assumes same name and location as video by default
(e.g. path/to/DJI_0001.MP4 --> /path/to/DJI_0001.SRT).'''
FR_MSG = 'Frame extraction framerate. Assumes %(default)s by default.'
OUT_MSG = "Directory for frames output."
DEFAULT_OUTPUT_NAME = 'frames'


def get_file_name(file_path):
    """Returns the extensionless file name at the given file path.

    Assumes the file is a valid, conforming to <name>.<extension> format.

    Args:
        file_path -- file path
    Returns 
        file -- extensionless file name
    """
    # os split returns head tail pair of parent path - file name 
    file_dir_name_pair = os.path.split(file_path)
    # File name is the tail
    file_name = file_dir_name_pair[1] 
    # Extract name without extension
    file = os.path.splitext(file_name)[0]
    return file

def check_dependencies():
    """Ensure that the system has the required CLI tools.

    Raises:
        OSError: Either the required ffmpeg or exiftool are not found
    """
    try:
        subprocess.check_output(['ffmpeg', '-version'])
        subprocess.check_output(['exiftool', '-ver'])
    except FileNotFoundError as not_found_error:
        raise OSError("Required dependencies not found.") from not_found_error

def check_valid_file(path, ext):
    """Checks if file at path exist (returns it), otherwise throws exception.
    Args:
        path -- file path
    Returns:
        file found -- path
        file not found -- raises argparse.ArgumentTypeError
    """
    if not os.path.isfile(path) or not path.lower().endswith(ext):
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid file with extension {ext}.")
    return path

def check_frame_rate(frame_rate):
    """Checks if the frame_rate is a positive integer

    Args:
        frame_rate -- the frame rate

    Returns:
        frame_rate -- a positive integer
    """
    frame_rate = int(frame_rate)
    if isinstance(int(frame_rate), int) and frame_rate > 0:
        return frame_rate
    else:
        raise argparse.ArgumentTypeError("Frame rate must be a positive integer.")

def check_valid_output(output):
    """Checks if output directory path provided exists

    Args:
        output -- output directory path

    Returns:
        output -- a valid output directory path
    """
    if not os.path.isdir(output):
        raise argparse.ArgumentTypeError(f"'{output}' is not a valid directory.")
    return output

def mk_output_dir(target_path, output_dir_name):
    """Attempts to generate an output directory unless the path
    provided is already an existing one.

    Args:
        target_path -- the path (if provided) to where the output folder will be
    """
    # Set output folder name
    output_name = output_dir_name or DEFAULT_OUTPUT_NAME
    # Set the output folder path, defaulting to current working directory
    output_path = os.path.join(target_path or os.getcwd(), output_name)
    # Check if the provided output directory already exists.
    if os.path.exists(output_path):
        print(f"'{output_path}' already exists. Using the existing directory.")
    # Create output folder if doesn't already exist
    else:
        os.makedirs(output_path)
    return output_path

def get_default_srt_path(video_file_path):
    """Generates the default .SRT file path based on the video file path.
    E.g. /path/to/DJI_0001.MP4 --> /path/to/DJI_0001.SRT
    Args:
        video_file_path  -- the path to the video file
    Returns:
        str -- the default .SRT file path
    """
    video_file_dir, video_file_name = os.path.split(video_file_path)
    srt_file_name = os.path.splitext(video_file_name)[0] + '.srt'
    srt_path = os.path.join(video_file_dir, srt_file_name)
    # Check if the default .SRT file path exists
    check_valid_file(srt_path, '.srt')
    return srt_path

def main():
    """CLI entrypoint for droneframe, handles arguments before initiating program
    """
    check_dependencies()
    parser = argparse.ArgumentParser(prog='droneframe', description=ARG_MSG)
    parser.add_argument('video', type=lambda f: check_valid_file(f, '.mp4'), help=VID_MSG)
    parser.add_argument("-m", "--meta", type=lambda f: check_valid_file(f, '.srt'), help=SRT_MSG)
    parser.add_argument("-f", "--frame_rate", help=FR_MSG, default=30, type=check_frame_rate)
    parser.add_argument("-o", "--output", help=OUT_MSG)
    args = parser.parse_args()
    # If 'meta' is not provided, set it to the default .SRT file path
    if args.meta is None:
        args.meta = get_default_srt_path(args.video)
    # Output folder is named after the input video file
    output_dir_name = get_file_name(args.video)
    # Set the output directory (or create one) for the frames
    args.output = mk_output_dir(args.output, output_dir_name)
    # Call the main entrypoint with the parsed arguments
    run(args)

if __name__ == '__main__':
    main()
    