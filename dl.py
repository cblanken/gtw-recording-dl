from sys import argv
from wget import download
import requests
import json

HEADERS1 = {
    "Host": "globalattspa.gotowebinar.com",
    "Accept": "*/*",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type",
    "Origin": "https://register.gotowebinar.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Referer": "https://register.gotowebinar.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
}

HEADERS2 = {
    "Host": "globalattspa.gotowebinar.com",
    "Sec-Ch-Ua": '"Chromium";v="93", " Not;A Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://register.gotowebinar.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "http://register.gotowebinar.com/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
}

if __name__ == "__main__":
    if len(argv) != 4:
        print("Usage: python dl.py <GoToWebinar link> <creds.json> <output>")
    else:
        # Parse recording ID from URL
        page_url = str(argv[1])
        recording_id = page_url.split("/")[-1]
        print("Recording ID:", recording_id)

        # Provide registration info, name and email, to api
        reg_info = {"firstName":"firstName","lastName":"lastName","email":"email"}
        with open(argv[2]) as f:
            reg_info = json.load(f)
        print("Registration info:", reg_info)
        recording_page_url = "https://globalattspa.gotowebinar.com/api/recordings/" + recording_id + "/registrants"

        # Send OPTIONS request to allow registration
        r1 = requests.options(url=recording_page_url, headers=HEADERS1)

        # Send POST with registration creds
        r2 = requests.post(url=recording_page_url, data=json.dumps(reg_info), headers=HEADERS2)

        registrant_key = str(r2.json()["registrantKey"])
        print("Registrant Key:", registrant_key)

        # Send GET to retrieve CDN link to video file 
        get_vid_url = "https://api.services.gotomeeting.com/registrationservice/api/v1/webinars/{0}/registrants/{1}/recordingAssets?type=OFFLINEWEBINAR&client=spa".format(recording_id, registrant_key)
        r3 = requests.get(url=get_vid_url, headers=HEADERS2)
        vid_url = str(r3.json()["cdnLocation"])
        
        # Download recording with wget
        print("Downloading video from:", vid_url.split("?")[0])
        download(vid_url, out=argv[3])
        print()

