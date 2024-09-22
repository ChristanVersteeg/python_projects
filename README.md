# This markdown is only relevant to the specific file in: 
`C:\Users\pooti\Desktop\python_projects\Game Utilities\MC\YouTubeVideoToMusicDisc\DiscDownloader.py`
The current version of pytube (15.0.0) is broken due to YT chaning their JS code, breaking the regex parsing. Here are the steps to fix the library:

Answer gotten from issue on the pytube github: https://github.com/pytube/pytube/issues/1954#issuecomment-2218287594

0. Make sure you've the newest version of pytube, `pip install --upgrade pytube`
1. Open `cmd`
2. Type `pip show pip`
3. Find the `Location` field your `cmd` prints out
4. Copy the `Location` `path`.
5. Press `Win+R`
6. Paste your copied location into the `Win+R` prompt
7. Find `pytube` within your installed packages (either by looking it up in the search bar, or just type it whilst in folder view to get the quick result
8. Open the `pytube` folder
9. Find `cipher.py` (by the same steps as 7)
10. Open `cipher.py`
11. Go to line `264-274`
12. Replace that code with this:
```py
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
```
