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
    sleep_time = 10
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
        "The default streamer is namin1004, if you want to change it please input another streamer name. Otherwise, press Enter to continue.\n \n默認直播主是 namin1004，如果要更改它，請輸入另一個直播主的名稱。否則，按 Enter 繼續"
    )
    streamer = str(input("Enter streamer: ") or "namin1004")
    clear()
    token = input("Your token 輸入Token (覺得麻煩的話可以不用輸入): ")
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
