import glob
import os
import sys

import config

absolute_path = "/home/cavazos/src/rtsp-timelapse"


def delete_output():
    output_directory = f'{absolute_path}/output'
    video_files = glob.glob1(output_directory, "*.mp4")
    # Delete the timelapses
    print("Starting deletion")
    for file in video_files:
        filepath = f"{output_directory}/{file}"
        if os.path.exists(filepath):
            os.remove(filepath)
    print(f"Finished deletion of mp4 files in {output_directory}")


if __name__ == '__main__':
    delete_output()

