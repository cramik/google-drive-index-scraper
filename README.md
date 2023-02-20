# google-drive-index-scraper / redacted-scraper

Scrapes download links from Google-Drive-Index (https://gitlab.com/GoogleDriveIndex/Google-Drive-Index) based websites through the use of selenium

Unfortunately, the website I use this on has a download quota. Because of this, I will not be releasing the name of this website publicly on this repo until it is down in hopes to not bombard them with tons of requests from people who can't handle themselves. If you ask I might tell though.

# Requirements
```
selenium (available via pip)
chrome (for chromedriver to work)
```

# Usage

```
Usage:
- Search (Example: "python redactedscraper.py search Infinity War")
- Home (Example: "python redactedscraper.py home")
```

# Borrowed code
https://gist.github.com/primaryobjects/70b4864815cf25a40525972d598563f6 - Saves user from having to install chromedriver to path
