import json
import os
import subprocess
import datetime as dt
import threading
import time

status = ["checking", "downloading", "converting"]
import pyperclip


class Recorder:
    def __init__(self, streamer, token):
        self.streamer = streamer
        self.current = status[0]
        self.token = token
        self.offine = True

        threading.Thread(target=self.check_loop).start()
        threading.Thread(target=self.downlaod_loop).start()

    def check_loop(self):
        while True:
            if self.current != status[1]:
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
                if "error" not in result:
                    self.offine = False
                else:
                    self.offine = True
                    print(f"{self.streamer} is offine")

    def downlaod_loop(self):
        while True:
            if self.offine == False and self.current != status[1]:
                self.current = status[1]
                threading.Thread(target=self.main).start()
            continue

    def loop(self):
        while True:
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
            print(result)
            if "error" in result and self.current != status[1]:
                print(f"{self.streamer} is offine")
            elif self.current != status[1]:
                threading.Thread(target=self.main).start()
            continue

    def main(self):
        filename = dt.datetime.now().strftime("%Y%m%d-%H%M")
        subprocess.run(
            [
                r"C:\Program Files\Streamlink\bin\streamlink.exe",
                "--quiet",
                "--hls-playlist-reload-attempts",
                "1",
                "--stream-timeout",
                "5",
                "--stream-segment-timeout",
                "5",
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


def get_name():
    name = (
        input(
            "Default streamer is Namin,\nIf you want to change it please input another streamer name below.\nOtherwise, press Enter to continue: \n\nExample 1: https://www.twitch.tv/namin1004\nExample 2: teenggg__\n\nStreamer: "
        )
        or "namin1004"
    )
    if name.startswith("https"):
        name = name.split("/")[-1]
    return name


def get_token():
    if os.path.exists("token"):
        with open("token", "r") as t:
            old_token = t.read()
        token = (
            input(
                f"Your old Token: {old_token}\n\nIf you dont want to change please press Enter\n\nOtherwise type the new token here: "
            )
            or old_token
        )
    else:
        pyperclip.copy(
            'document.cookie.split("; ").find(item=>item.startsWith("auth-token="))?.split("=")[1]'
        )
        token = input(
            f"""The get token code has been copied.\nYou may go to Twitch page and login,\nthen press F12 and CTRL+V in the console page. It shows the token.\n\nExample 1: "pugqq9cz5weasr76c2ddd1234k3vvq"\nExample 2: 'pugqq9cz5weasr76c2ddd1234k3vvq'\nExample 3: pugqq9cz5weasr76c2ddd1234k3vvq\n\nToken: """
        )
        if token.startswith('"'):
            token = token[1:-1]
        elif token.startswith("'"):
            token = token[1:-1]
        if token:
            with open("token", "w") as t:
                t.write(token)
    if token == "":
        get_token()
    return token


if __name__ == "__main__":
    name = get_name()
    os.system("cls")
    token = get_token()
    os.system("cls")
    Recorder(name, token)
