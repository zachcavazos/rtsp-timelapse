import config
import subprocess
import sys

from datetime import datetime


absolute_path = "/home/cavazos/src/rtsp-timelapse"


def capture_frame(camera_name = 'nursery'):
    camera_config = config.camera_config[camera_name]
    images_directory = f"{absolute_path}/{camera_config['directory']}"
    rtsp_username = camera_config['rtsp_username']
    rtsp_password = camera_config['rtsp_password']
    rtsp_ip_address = camera_config['rtsp_ip_address']
    rtsp_path = f"rtsp://{rtsp_username}:{rtsp_password}@{rtsp_ip_address}/stream1"

    # Use ffmpeg to connect to the rtsp stream and save 1 frame
    # ffmpeg -i <stream> -vframes 1 <output>
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            rtsp_path,
            "-vframes",
            "1",
            f"{images_directory}/{datetime.now().strftime('%Y%m%d-%H%M%S')}.png",
        ]
    )


if __name__ == '__main__':
    args = sys.argv
    camera_name = args[1] if len(args) > 1 else 'nursery'
    capture_frame(camera_name)

