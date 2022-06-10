import datetime
import os
import subprocess
import shutil
import config


class TwitchRecorder:
    def __init__(self):
        # global configuration
        self.ffmpeg_path = config.ffmpeg
        if self.ffmpeg_path == "":
            self.disable_ffmpeg = True
        else:
            self.disable_ffmpeg = False
        self.root_path = config.root_path

        # user configuration
        self.username = config.username
        self.quality = "best"

        # twitch configuration
        self.access_token = ""

    def run(self, token):
        # set token
        try:
            self.access_token = token.split(":")[1]
        except:
            pass

        # path to recorded stream
        recorded_path = os.path.join(self.root_path, "recorded")
        # path to finished video, errors removed
        processed_path = os.path.join(self.root_path, "processed")

        # create directory for recordedPath and processedPath if not exist
        if os.path.isdir(recorded_path) is False:
            os.makedirs(recorded_path)
        if os.path.isdir(processed_path) is False:
            os.makedirs(processed_path)

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

        print(f"checking for {self.username} and recording with {self.quality} quality")
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

    def loop_check(self, recorded_path, processed_path):
        while True:
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M") + ".mp4"
            recorded_filename = os.path.join(recorded_path, filename)
            processed_filename = os.path.join(processed_path, filename)
            if self.access_token != "":
                # start streamlink process
                subprocess.call(
                    [
                        "streamlink.exe",
                        "--hls-playlist-reload-attempts",
                        "20",
                        "--quiet",
                        f"--twitch-api-header=Authentication=OAuth {self.access_token}",
                        "--twitch-disable-hosting",
                        "--twitch-low-latency",
                        "twitch.tv/" + self.username,
                        self.quality,
                        "-o",
                        recorded_filename,
                    ],
                    shell=True,
                )
            else:
                subprocess.call(
                    [
                        "streamlink.exe",
                        "--hls-playlist-reload-attempts",
                        "20",
                        "--quiet",
                        "--twitch-disable-hosting",
                        "--twitch-low-latency",
                        "twitch.tv/" + self.username,
                        self.quality,
                        "-o",
                        recorded_filename,
                    ],
                    shell=True,
                )

            if os.path.exists(recorded_filename) is True:
                self.process_recorded_file(recorded_filename, processed_filename)


def main(token):
    twitch_recorder = TwitchRecorder()
    twitch_recorder.run(token)


if __name__ == "__main__":
    token = input("Your token:")
    main(token)
