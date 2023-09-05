"""droneframe - a tool to generate high fidelity frames from a drone video
along with their EXIF data at a desired framerate. Currently works with MP4 
for the footage and SRT for the metadata. 

System Dependencies (Required):
    `ffmpeg` -- used for frame extraction
    `exiftool` -- used for saving EXIF data into frames

"""
import os
import subprocess
import re

def calculate_frame_number(frame_number_str, frame_rate, difftime_ms):
    """Calculate the frame number based on the frame number string, frame rate,
    and difftime in milliseconds.

    Args:
        frame_number_str (str): The frame number string from the SRT.
        frame_rate (int): The frame rate of the video.
        difftime_ms (int): The DiffTime in milliseconds.

    Returns:
        frame_number (int): The calculated frame number.
    """
    # Parse the frame number string to an integer
    frame_number = int(frame_number_str)

    # Calculate frame number based on frame rate and difftime
    frame_number += (frame_rate * difftime_ms) // 1000

    return frame_number

def parse_srt_metadata(srt_path, frame_rate, frames_dir):
    """Preserve SRT metadata relevant for photogrammetry.

    srt_path -- path to SRT file for metadata
    frame_rate -- frame rate for picking which frames to cache metadata for
    frames_dir -- directory containing extracted frames

    Returns:
        frame_metadata –– dictionary to hold metadata (key, value - frame #, dict of metadata)
    """
    metadata = {}

    # Extract text from SRT
    with open(srt_path, encoding='utf-8') as srt_file:
        srt_content = srt_file.read()

    # Define the regular expression pattern
    metadata_pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})\n<font size=\"28\">SrtCnt : \d+, DiffTime : (\d+)ms\n(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}.\d{3})\n\[iso\s*:\s*\d+] \[shutter\s*:\s*\d+\/\d+\.\d+] \[fnum\s*:\s*\d+].*?\[latitude:\s*([\d.-]+)] \[longitude:\s*([\d.-]+)](?: \[rel_alt:\s*([\d.-]+) abs_alt:\s*([\d.-]+)])?")
    # Tracks timestamp across frames in the SRT based on their frame durations
    total_diff_time = 0
    # Bring in the list of extracted frames
    frame_files = [f for f in os.listdir(frames_dir) if f.endswith(".jpg")]
    frame_files.sort()  # Sort the files to ensure the correct order
    # Match all the frames in the SRT to extract their data
    for match in metadata_pattern.finditer(srt_content):
        (
            frame_number_str, _, _,
            diff_time_ms, timestamp,
            latitude, longitude,
            rel_alt, abs_alt
        ) = match.groups()
        # Keep track of current time in video
        total_diff_time += int(diff_time_ms)
        # Calculate the relative frame number based on the DiffTime and frame rate
        expected_frame_number = int(total_diff_time * frame_rate / 1000)
        # Only process frames that match the expected frame number
        if expected_frame_number < len(frame_files):
            # Store the relevant metadata for the frame based on the file name
            frame_filename = frame_files[expected_frame_number]
            # Currently saving the most crucial metadata in mind for photogrammetry usecase
            metadata[frame_filename] = {
                "DateTimeOriginal": timestamp,
                "GPSLatitude": latitude,
                "GPSLongitude": longitude,
            }
            if abs_alt:
                metadata[frame_filename]["GPSAltitude"] = abs_alt
            elif rel_alt:
                metadata[frame_filename]["GPSAltitude"] = rel_alt
            # print(expected_frame_number, frame_filename, metadata[frame_filename])

    return metadata

def process_frames(output, metadata):
    """Using exiftool, populates frames with their cached metadata from the SRT file.

    output -- path to directory containing video frames
    metadata -- dict containing metadata for each relevant frame
    """
    for frame_file, frame_metadata in metadata.items():
        frame_path = os.path.join(output, frame_file)
        args = ["-overwrite_original"]
        for key, value in frame_metadata.items():
            args.append(f"-{key}={value}")
        subprocess.call(["exiftool"] + args + [frame_path])


def run(args):
    """Extracts frames from a given drone video (at provided frame rate) using ffmpeg,
    then calls on util methods to (1) extract metadata from video's SRT file
    and (2) populate frames with their corresponding metadata using exiftool.

    args -- dict containing arguments passed from CLI
    """
    # Set the path to the input drone footage
    input_path = args.video
    # Set the path to the input footage's SRT file
    srt_path = args.meta
    # Set the output directory for the extracted frames
    output = args.output
    print(output, type(output))
    # Set the frame rate (number of frames per second) to extract
    frame_rate = args.frame_rate


    # Use ffmpeg to extract frames from the input footage
    subprocess.call(["ffmpeg", "-i", input_path, "-q:v", "1", "-r", str(frame_rate),
                     os.path.join(output, "frame_%04d.jpg")])

    # Read the SRT file and extract the GPS coordinates and date/time for each frame
    frame_metadata = parse_srt_metadata(srt_path, frame_rate, output)

    # Use exiftool to copy the metadata from the SRT file to each extracted frame
    process_frames(output, frame_metadata)
