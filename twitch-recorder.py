import datetime
import enum
import getopt
import os
import subprocess
import sys
import shutil
import time

import requests
import config


class TwitchResponseStatus(enum.Enum):
    ONLINE = 0
    OFFLINE = 1
    NOT_FOUND = 2
    UNAUTHORIZED = 3
    ERROR = 4


class TwitchRecorder:
    def __init__(self):
        # global configuration
        self.ffmpeg_path = config.ffmpeg
        if self.ffmpeg_path == "":
            self.disable_ffmpeg = True
        else:
            self.disable_ffmpeg = False
        self.refresh = 1
        self.root_path = config.root_path

        # user configuration
        self.username = config.username
        self.quality = "best"

        # twitch configuration
        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.token_url = (
            "https://id.twitch.tv/oauth2/token?client_id="
            + self.client_id
            + "&client_secret="
            + self.client_secret
            + "&grant_type=client_credentials"
        )
        self.url = "https://api.twitch.tv/helix/streams"
        self.access_token = self.fetch_access_token()

    def fetch_access_token(self):
        token_response = requests.post(self.token_url, timeout=1)
        token_response.raise_for_status()
        token = token_response.json()
        return token["access_token"]

    def run(self):
        # path to recorded stream
        recorded_path = os.path.join(self.root_path, "recorded")
        # path to finished video, errors removed
        processed_path = os.path.join(self.root_path, "processed")

        # create directory for recordedPath and processedPath if not exist
        if os.path.isdir(recorded_path) is False:
            os.makedirs(recorded_path)
        if os.path.isdir(processed_path) is False:
            os.makedirs(processed_path)

        # make sure the interval to check user availability is not less than 1 seconds
        if self.refresh < 1:
            print("check interval should not be lower than 1 seconds")
            self.refresh = 1
            print("system set check interval to 1 seconds")

        # fix videordins from previous recog session
        try:
            video_list = [
                f
                for f in os.listdir(recorded_path)
                if os.path.isfile(os.path.join(recorded_path, f))
            ]
            if len(video_list) > 0:
                print("processing previously recorded files")
            for f in video_list:
                recorded_filename = os.path.join(recorded_path, f)
                processed_filename = os.path.join(processed_path, f)
                self.process_recorded_file(recorded_filename, processed_filename)
        except Exception as e:
            print(e)

        print(
            f"checking for {self.username} every {self.refresh} seconds, recording with {self.quality} quality"
        )
        self.loop_check(recorded_path, processed_path)

    def process_recorded_file(self, recorded_filename, processed_filename):
        if self.disable_ffmpeg:
            print("moving: ", recorded_filename)
            shutil.move(recorded_filename, processed_filename)
        else:
            print("fixing: ", recorded_filename)
            self.ffmpeg_copy_and_fix_errors(recorded_filename, processed_filename)

    def ffmpeg_copy_and_fix_errors(self, recorded_filename, processed_filename):
        try:
            subprocess.call(
                [
                    self.ffmpeg_path,
                    "-err_detect",
                    "ignore_err",
                    "-i",
                    recorded_filename,
                    "-c",
                    "copy",
                    processed_filename,
                ],
                shell=True,
            )
            os.remove(recorded_filename)
        except Exception as e:
            print(e)

    def check_user(self):
        info = None
        status = TwitchResponseStatus.ERROR
        try:
            headers = {
                "Client-ID": self.client_id,
                "Authorization": "Bearer " + self.access_token,
            }
            r = requests.get(
                self.url + "?user_login=" + self.username, headers=headers, timeout=15
            )
            r.raise_for_status()
            info = r.json()
            if info is None or not info["data"]:
                status = TwitchResponseStatus.OFFLINE
            else:
                status = TwitchResponseStatus.ONLINE
        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.status_code == 401:
                    status = TwitchResponseStatus.UNAUTHORIZED
                if e.response.status_code == 404:
                    status = TwitchResponseStatus.NOT_FOUND
        return status, info

    def loop_check(self, recorded_path, processed_path):
        while True:
            status, info = self.check_user()
            if status == TwitchResponseStatus.NOT_FOUND:
                print("username not found, invalid username or typo")
                time.sleep(self.refresh)
            elif status == TwitchResponseStatus.ERROR:
                print(
                    "unexpected error. will try again in 10s",
                    datetime.datetime.now().strftime("%Hh%Mm%Ss"),
                )
                time.sleep(10)
            elif status == TwitchResponseStatus.OFFLINE:
                print(
                    f"{config.username} currently offline, checking again in 1 seconds"
                )
                time.sleep(self.refresh)
            elif status == TwitchResponseStatus.UNAUTHORIZED:
                print("unauthorized, will attempt to log back in immediately")
                self.access_token = self.fetch_access_token()
            elif status == TwitchResponseStatus.ONLINE:
                print(f"{config.username} online, stream recording in session")

                filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".mp4"

                recorded_filename = os.path.join(recorded_path, filename)
                processed_filename = os.path.join(processed_path, filename)

                # start streamlink process
                subprocess.call(
                    [
                        "streamlink.exe",
                        "--hls-playlist-reload-attempts",
                        "10",
                        "--twitch-disable-hosting",
                        "--twitch-low-latency",
                        "--twitch-disable-ads",
                        "twitch.tv/" + self.username,
                        self.quality,
                        "-o",
                        recorded_filename,
                    ],
                    shell=True,
                )

                print("recording stream is done, processing video file")
                if os.path.exists(recorded_filename) is True:
                    self.process_recorded_file(recorded_filename, processed_filename)
                else:
                    print("skip fixing, file not found")

                print("processing is done, going back to checking...")
                time.sleep(5)


def main(argv):
    twitch_recorder = TwitchRecorder()
    usage_message = "twitch-recorder.py -u <username> -q <quality>"

    try:
        opts, args = getopt.getopt(
            argv,
            "hu:q:l:",
            ["username=", "quality=", "log=", "logging=", "disable-ffmpeg"],
        )
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(usage_message)
            sys.exit()
        elif opt in ("-u", "--username"):
            twitch_recorder.username = arg
        elif opt in ("-q", "--quality"):
            twitch_recorder.quality = arg
        elif opt in ("-l", "--log", "--logging"):
            pass
        elif opt == "--disable-ffmpeg":
            twitch_recorder.disable_ffmpeg = True
            print("ffmpeg disabled")

    twitch_recorder.run()


if __name__ == "__main__":
    main(sys.argv[1:])
