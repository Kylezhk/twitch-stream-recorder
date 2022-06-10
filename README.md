# Ky's Twitch Stream Recorder
This exe allows you to record twitch streams live to .mp4 files.
## Requirements
- Network
- Brain
- Your Love to Namin

## Step
0) 安裝[Streamlink](https://streamlink.github.io/)  (最新版本就最好，全部按下一步就好了)
1) 請確定 `C:\Program Files\Streamlink\ffmpeg\` 有 ffmpeg.exe (安裝streamlink就會有了)
2) 下載我弄的[程式](https://github.com/Kylezhk/twitch-stream-recorder/releases/download/v200/ky1-twitch-recorder-v200.exe) (廢話)
3) 找一個/開一個空白資料夾
4) 把程式放進去
5) 開起來! (第一次會自動生成processed資料夾跟recorded資料夾)

程式會持續顯示出`error: No playable streams found on this URL: twitch.tv/namin1004`來稽查namin有沒有開播

金主播下播後然後等程式回到`error: No playable streams found on this URL: twitch.tv/namin1004`, .mp4檔會在processed資料夾出現

>注: 當金主播下播後程式會繼續運行24/7，如果不想佔用網絡請關閉程式

>注: 這是獨立程式，可以跟twitchlink，twitchleecher一起開

>~~注: 正常情況下，這個程式下載來的VOD是沒有開始的20秒，所以有用info的請小心~~ 未知有沒有掉，待測試

## Changed
- Only Windows OS
- No Log file
- Refresh time around a second
- Date + time as file name
- Fixed shell error
- Namin1004 as target streammer
- Enable low-latency
- No longer record when hosing
- Reload attempts increased to 20 times
- Applied Twitch authentication
- Delete args in main() for exe purpose only
- Checking method change to Streamlink rather than using Twitch API

If there any bugs, please find me Ky1ez#5989 through the Discord 

[![namin banner](banner.jpg)](https://marpple.shop/en/namin?page=0)