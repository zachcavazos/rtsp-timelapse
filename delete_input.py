import glob
import os
import sys

import config

absolute_path = "/home/cavazos/src/rtsp-timelapse"


def delete_input(camera_name='nursery'):
    images_directory = f'{absolute_path}/{config.camera_config[camera_name]["directory"]}'
    image_files = glob.glob1(images_directory, "*.png")
    # Delete the images
    print("Starting deletion")
    for image_file in image_files:
        image_filepath = f"{images_directory}/{image_file}"
        if os.path.exists(image_filepath):
            os.remove(image_filepath)
    print(f"Finished deletion of png files in {images_directory}")


if __name__ == '__main__':
    args = sys.argv
    camera_name = args[1] if len(args) > 1 else 'nursery'
    delete_input()

