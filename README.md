# Ky's Twitch Stream Recorder
This exe allows you to record twitch streams live to .mp4 files.
## Requirements
- Network
- Brain
- Your Love to Namin

## 安裝步驟
0) 安裝[Streamlink](https://github.com/streamlink/windows-builds/releases) (最新版本就好，全部按下一步就好了)

>步驟 0) 例子: `streamlink-5.0.1-1-py310-x86_64.exe`

1) 請確定 `C:\Program Files\Streamlink\ffmpeg\` 有 ffmpeg.exe (正常來說安裝streamlink就會有了)

2) 下載我弄的[程式](https://github.com/Kylezhk/twitch-stream-recorder/releases/download/v300/twitch-recorder-v300.exe) (廢話)

3) 找一個/開一個空白資料夾

4) 把程式放進去

5) 請到這個[網站](https://twitchapps.com/tmi/)拿你自己的Token (按Connect然後複製那段字) (這Token = 無廣告下載VOD) 
>注: 如果不懂或者擔心這個網站的安全，可以跳過步驟5。~~沒Token也好像沒有廣告~~ 待驗證

6) 開起來！程式會先問你要不要選其他的streamer, 如果想下載金主播的話就直接按Enter鍵吧

>步驟 6) 例子: `Enter streamer: hellaya1111`

>注: 第一次會自動生成processed資料夾跟recorded資料夾

7) 然後程式會問你Token, 你可以複製並貼上你剛剛在5)的步驟Token，沒有Token的話就直接按Enter鍵就好了

>步驟 7) 例子: `Your token: oauth:1234565ep62w5yyh108d52juqq0euul`



程式會持續顯示出`namin1004 doesn't streaming now`來稽查namin有沒有開播

金主播下播後然後等程式回到`namin1004 doesn't streaming now`, .mp4檔會在processed資料夾出現

>注: 當金主播下播後程式會繼續運行24/7，如果不想佔用網絡跟電腦資訊請關閉程式

>注: 這是獨立程式，可以跟twitchlink，twitchleecher一起開

## Changed
- Only Windows OS
- No Log file
- Refresh time around a second
- Date + time as file name
- Fixed shell error
- Namin1004 as target streammer
- Enable low-latency
- No longer record when hosing
- Timeout set to 5 second
- ffmpeg process will not affect streamlink anymore
- Applied Twitch authentication typed by user 
- Delete args in main() for exe purpose only
- Checking method change to Streamlink rather than using Twitch API
- Customize your other streamer

If there any bugs, please find me Ky1ez#5989 through the Discord 

[![namin banner](banner.jpg)](https://marpple.shop/en/namin?page=0)