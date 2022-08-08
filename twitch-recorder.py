import os
import subprocess
import time
from multiprocessing import Process, freeze_support
import datetime as dt
from glob import glob

clear = lambda: os.system("cls")


def loop_streamlink(token, streamer):
    while True:
        try:
            subprocess.check_output(["streamlink", "twitch.tv/" + streamer])
            if token == None:
                current_time = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
                subprocess.call(
                    [
                        "streamlink.exe",
                        "--hls-timeout",
                        "10",
                        "--quiet",
                        "--twitch-disable-hosting",
                        "--twitch-low-latency",
                        "twitch.tv/" + streamer,
                        "best",
                        "-o",
                        "recorded/" + current_time + ".mp4",
                    ],
                )
            else:
                current_time = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
                subprocess.call(
                    [
                        "streamlink.exe",
                        "--hls-timeout",
                        "10",
                        "--quiet",
                        "--twitch-disable-hosting",
                        "--twitch-low-latency",
                        f"--twitch-api-header=Authentication=OAuth {token}",
                        "twitch.tv/" + streamer,
                        "best",
                        "-o",
                        "recorded/" + current_time + ".mp4",
                    ],
                )
        except subprocess.CalledProcessError:
            print(f"{streamer} doesn't streaming now")


def loop_ffmpeg(streamer):
    sleep_time = 5
    while True:
        try:
            subprocess.check_output(["streamlink", "twitch.tv/" + streamer])
            time.sleep(sleep_time)
            pass
        except:
            recordedFolder = glob("recorded/*.mp4")
            if recordedFolder == []:
                time.sleep(sleep_time)
                pass
            else:
                for r in recordedFolder:
                    subprocess.call(
                        [
                            "C:\\Program Files\\Streamlink\\ffmpeg\\ffmpeg.exe",
                            "-y",
                            "-err_detect",
                            "ignore_err",
                            "-i",
                            r,
                            "-c",
                            "copy",
                            "processed\\" + r.split("\\")[1],
                        ],
                    )
                    try:
                        os.remove(r)
                    except PermissionError:
                        time.sleep(sleep_time)
                        pass


def main():
    if os.path.isdir("recorded/") is False:
        os.makedirs("recorded/")
    if os.path.isdir("processed\\") is False:
        os.makedirs("processed\\")

    print(
        "Defualt streamer is namin1004, if you want to change, please input another streamer name. Otherise, press enter to continue."
    )
    streamer = str(input("Enter streamer: ") or "namin1004")
    clear()
    token = input("Your token: ")
    clear()
    Process(
        target=loop_streamlink,
        args=(
            token,
            streamer,
        ),
    ).start()
    Process(target=loop_ffmpeg, args=(streamer,)).start()


if __name__ == "__main__":
    freeze_support()
    main()
