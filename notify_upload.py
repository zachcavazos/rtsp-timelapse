import apprise
import config
import create_timelapse
import sys


def notify_upload(camera_name='nursery'):
    app = get_app()
    app.notify(body=config.camera_config[camera_name]['message'], title='Timelapse')


def notify_failure(camera_name='nursery'):
    app = get_app()
    app.notify(body='Failed to create timelapse, check credentials or device space', title='Process Failure')


def get_app():
    app = apprise.Apprise()
    for service in config.apprise_services:
        app.add(service)
    return app


if __name__ == "__main__":
    args = sys.argv
    camera_name = args[1] if len(args) > 1 else 'nursery'
    notify_upload()
