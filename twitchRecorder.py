import json
import os
import subprocess
import datetime as dt
import threading
import time

status = ["checking", "downloading", "converting"]


class Recorder:
    def __init__(self, streamer, token):
        self.streamer = streamer
        self.current = status[0]
        self.token = token
        self.loop()

    def loop(self):
        while True:
            # try:
            raw = subprocess.run(
                [
                    r"C:\Program Files\Streamlink\bin\streamlink.exe",
                    "-j",
                    f"twitch.tv/{self.streamer}",
                    "best",
                ],
                encoding="utf-8",
                stdout=subprocess.PIPE,
            )
            result = json.loads(raw.stdout)
            if "error" in result and self.current != status[1]:
                print(f"{self.streamer} is offine")
            elif self.current != status[1]:
                threading.Thread(target=self.main).start()
            continue
        # except KeyboardInterrupt:
        #     exit()

    def main(self):
        self.current = status[1]
        filename = dt.datetime.now().strftime("%Y%m%d-%H%M")
        subprocess.run(
            [
                r"C:\Program Files\Streamlink\bin\streamlink.exe",
                "--quiet",
                "--hls-playlist-reload-attempts",
                "1",
                "--twitch-disable-reruns",
                "--twitch-low-latency",
                f"--twitch-api-header=Authorization=OAuth {self.token}",
                f"twitch.tv/{self.streamer}",
                "best",
                "-o",
                filename + ".ts",
            ],
        )

        self.current = status[2]
        subprocess.run(
            [
                r"C:\Program Files\Streamlink\ffmpeg\ffmpeg.exe",
                "-y",
                "-err_detect",
                "ignore_err",
                "-i",
                filename + ".ts",
                "-c",
                "copy",
                filename + ".mp4",
                "-y",
            ],
        )
        time.sleep(5)
        os.remove(f"{filename}.ts")
        self.current = status[0]


if __name__ == "__main__":
    name = (
        input(
            "The default streamer is namin1004,\nif you want to change it please input another streamer name.\nOtherwise, press Enter to continue: \n\n"
        )
        or "namin1004"
    )
    if name.startswith("https"):
        name = name.split("/")[-1]
    if os.path.exists("token"):
        with open("token", "r") as t:
            token = t.read()
    else:
        os.system("cls")
        token = input("Please enter the token: \n\n")
        if token.startswith('"'):
            token = token[1:-1]
        if token:
            with open("token", "w") as t:
                t.write(token)
    os.system("cls")
    recorder = Recorder(name, token)
