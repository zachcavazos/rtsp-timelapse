import config
import glob
import os
import subprocess
import sys

from datetime import datetime
from pathlib import Path


UID = 1000
GID = 1002

absolute_path = "/home/cavazos/src/rtsp-timelapse"
# timelapse_directory = f"{absolute_path}/output"
timelapse_directory = "/mnt/hd1/data/cavazos/files/Timelapses"

def create_timelapse(camera_name='nursery'):
    images_directory = f'{absolute_path}/{config.camera_config[camera_name]["directory"]}'
    print(f"Creating a timelapse from {images_directory}")
    timelapse_filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp4"
    timelapse_filepath = f"{timelapse_directory}/{timelapse_filename}"
    subprocess.run(
        [
            "ffmpeg",
            "-pattern_type",
            "glob",
	    "-framerate",
	    "10",
	    "-i",
            f"{images_directory}/*.png",
            f"{timelapse_filepath}",
        ]
    )
    if not Path(timelapse_filepath).is_file():
        print(f'Failed to create timelapse, check input directory')
        return None
    else:
        print(f'wrote file successfully {timelapse_filepath}, updating owner')
        os.chown(timelapse_filepath, UID, GID)
    return timelapse_filepath


if __name__ == '__main__':
    args = sys.argv
    camera_name = args[1] if len(args) > 1 else 'nursery'
    create_timelapse(camera_name)

