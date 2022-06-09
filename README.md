# Ky's Twitch Stream Recorder
This exe allows you to record twitch streams live to .mp4 files.
This is fork by [ancalentari](https://github.com/ancalentari/twitch-stream-recorder) twitch-stream-recorder
## Requirements
- [streamlink](https://streamlink.github.io/) (ffmpeg need to be installed together)
- Brain

## Step
0) 安裝Streamlink (全部按下一步就好了)
1) 請確定 `C:\Program Files\Streamlink\ffmpeg\` 有 ffmpeg.exe (安裝streamlink就會有了)
2) 下載[程式](https://github.com/Kylezhk/twitch-stream-recorder/releases/download/V101/ky1-twitch-recorder.exe) (廢話)
3) 找一個/開一個空白資料夾
4) 把程式放進去
5) 開起來! (第一次會自動生成processed資料夾跟recorded資料夾)
6) 程式會持續顯示出`error: No playable streams found on this URL: twitch.tv/namin1004`來稽查namin有沒有開播

金主播下播後然後等程式回到`error: No playable streams found on this URL: twitch.tv/namin1004`, .mp4檔會在processed資料夾出現

>注: 當金主播下播後程式會繼續運行，如果不想佔用網絡請關閉程式

>注: 這是獨立程式，可以跟twitchlink，twitchleecher一起開

>~~注: 正常情況下，這個程式下載來的VOD是沒有開始的20秒，所以有用info的請小心~~ 未知

## Changed
- Only Windows OS
- No Log file
- Refresh time = ASAP
- Date + time as file name
- Fixed shell error
- Namin1004 as target streammer
- Enable low-latency
- No longer record when hosing
- Reload attempts increased to 10 times
- Applied Twitch authentication
- Delete args in main() for exe purpose only
- Checking method related to Streamlink rather than  Twitch API

If there any bugs, please find me Ky1ez#5989 through the Discord 

[![namin banner](banner.jpg)](https://marpple.shop/en/namin?page=0)