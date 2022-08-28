# GoToWebinar Recording Downloader
Given a GoToWebinar recording download link, POST registration info from creds.json and grab
the embedded CDN link for a direct download using wget.

## Usage
```console
$ python dl.py
Usage: python dl.py <GoToWebinar_recording_link> <creds.json> <output_file>
```
Here is partially redacted example.
```console
$ python dl.py https://register.gotowebinar.com/recording/***************0912 creds.json video_1
Recording ID: ***************0912
Registration info: {'firstName': '********', 'lastName': '********', 'email': '********'}
Registrant Key: ***************3727
Downloading video from: https://cdn.recordingassets.logmeininc.com/***************4564.mp4
100% [....................................................................] 2579071960 / 2579071960
```

