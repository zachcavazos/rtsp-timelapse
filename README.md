# RTSP Timelapse
*Adapted from git@github.com:zachcavazos/rtsp-timelapse.git
Supports connecting to an rtsp stream, capturing a photo, stiching those photos into a timelapse with ffmpeg
and uploading that timelapse to a Google Photos Album. It will also send a message to your favourite service
 [using Apprise](https://github.com/caronc/apprise) with confirmation or an error notification.

## Hardware
- Personally, I have this running on a Raspberry Pi5 (4GB RAM)
- An IP camera that supports RTSP

## Installation
- Create a python3 virtual environment and install the project's requirements:
```
$ python3 -m venv venv
$ source rtsp_timelapse/bin/activate
(rtsp_timelapse) $ pip install -r requirements.txt
```
- You will also need [ffmpeg](https://ffmpeg.org/) installed on your machine.  This can usually be
installed using a package manager.  For example:
```
$ sudo apt-get install ffmpeg
```
- Open config.py and enter the camera's
  - RTSP username
  - RTSP password
  - IP address
- Also in config.py, enter where you want your timelapse videos to be sent. See
[Apprise's github page](https://github.com/caronc/apprise) for examples. An
example for Telegram and Discord would look something like this:
```
# The list of services to notify
apprise_services = [
    "tgram://bottoken/ChatID",
    "discord://webhook_id/webhook_token",
]
```

Create a file `config.py` based on `example_config.py` with your desired camera/album/and service configuration.

- You should now be able to start the program:
```
(rtsp_timelapse) $ python main.py
```

# Creating the timelapses
The script is intended to be run regularly on a cronjob.  It will connect to the IP camera, take a photo 
and save the image to the **input** folder.

# Crontab Config
Below is an example of my current crontab, which is set up to take photos at regular intervals, before 
compiling those photos and taking the actions described above.
```
* 20-23,0-7 * * *  /bin/bash -c 'source /home/cavazos/src/rtsp-timelapse/venv/bin/activate &&  /home/cavazos/src/rtsp-timelapse/venv/bin/python /home/cavazos/src/rtsp-timelapse/capture_frame.py nursery'
0 8 * * * /bin/bash -c 'source /home/cavazos/src/rtsp-timelapse/venv/bin/activate &&  /home/cavazos/src/rtsp-timelapse/venv/bin/python /home/cavazos/src/rtsp-timelapse/main.py nursery'
* 9-16 * * * /bin/bash -c 'source /home/cavazos/src/rtsp-timelapse/venv/bin/activate && /home/cavazos/src/rtsp-timelapse/venv/bin/python /home/cavazos/src/rtsp-timelapse/capture_frame.py living-room'
0 17 * * * /bin/bash -c 'source /home/cavazos/src/rtsp-timelapse/venv/bin/activate && /home/cavazos/src/rtsp-timelapse/venv/bin/python /home/cavazos/src/rtsp-timelapse/main.py living-room'
0 0 1,15 * * /bin/bash -c 'source /home/cavazos/src/rtsp-timelapse/venv/bin/activate && /home/cavazos/src/rtsp-timelapse/venv/bin/python /home/cavazos/src/rtsp-timelapse/delete_output.py'
```
Note that the files accept a command line argument for which camera config to use, and which input file
location to look for the images in
I also have a delete function separately that is called at regular intervals to remove the output files
