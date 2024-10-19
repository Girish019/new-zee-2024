import re
import os
import json
import requests
import subprocess
import threading
import time
import argparse
import sys
import json
import xmltodict
import requests
import base64
import time
from pywv.device import Device
from pywv.pssh import PSSH
from pywv.cdm import Cdm

proxy_url = ""


proxies = {
    "https": proxy_url,
    "http": proxy_url
} if proxy_url and proxy_url.strip() else None

colored_text_config = False

MESSAGE = "\n[+] {}\n[+] {} : {}"

GROUP_TAG = "chung-C"

filename_format = "p2p"  # p2p or non-p2p

p2p_audio_bitrate = "K"

non_p2p_audio_bitrate = "Kbps"

underscore_before_after_group_tag = "__"

language_order = ['hi', 'ta', 'te', 'bn', 'gu', 'pa', 'as', 'or',
                  'ml', 'mr', 'kn', 'en', 'th', 'ja', 'th', 'id', 'ms', 'ko', 'bho']


script_directory = os.path.dirname(os.path.abspath("__file__"))

if os.name == "nt":
    iswin = "1"
else:
    iswin = "0"


ytdlp = os.path.join(script_directory, "binaries",
                     "yt-dlp") + (".exe" if iswin != "0" else "")
mp4decrypt = os.path.join(script_directory, "binaries",
                          "mp4decrypt") + (".exe" if iswin != "0" else "")
aria2c = os.path.join(script_directory, "binaries",
                      "aria2c") + (".exe" if iswin != "0" else "")
wvd_file_path = os.path.join(script_directory, "static",
                             "google_sdk_google_atv_x86_15.0.0_27cfa318_8162_l3.wvd")
dl_folder = os.path.join(script_directory, "downloads")

languages_info_file_path = os.path.join(script_directory, "static",
                                        "languages_info.json")


if iswin == "0":
    os.system(f"chmod 777 {ytdlp} {mp4decrypt} {aria2c}")


class ZEE5API:
    def __init__(self, hevc=True):
        self.hevc = hevc
        self.x_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDIzLTEwLTE1VDA2OjMxOjI2LjE0MVoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTY5NzM1MTQ4Nn0.ITgD4KwHd1mU9g6JDC0LESJpfjJeyD15kGojHLtpkDg"

        self.authorization = "eyJraWQiOiJlNmxfbGYweHpwYVk4VzBNcFQzWlBzN2hyOEZ4Y0trbDhDV0JaekVKT2lBIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJBNTgwMTgzMC04N0I4LTQ5QTItOEQ3Qy1DRDU3RkRBMTgzMUEiLCJzdWJzY3JpcHRpb25zIjoiW3tcImlkXCI6XCJkNzU0YjVmYS02MDdmLTExZWUtYjE2My02Zjg2NjQ0MTI1OWVcIixcInVzZXJfaWRcIjpcImE1ODAxODMwLTg3YjgtNDlhMi04ZDdjLWNkNTdmZGExODMxYVwiLFwiaWRlbnRpZmllclwiOlwiQ1JNXCIsXCJzdWJzY3JpcHRpb25fcGxhblwiOntcImlkXCI6XCIwLTExLTIwNzJcIixcImFzc2V0X3R5cGVcIjoxMSxcInN1YnNjcmlwdGlvbl9wbGFuX3R5cGVcIjpcIlNWT0RcIixcInRpdGxlXCI6XCJQcmVtaXVtXCIsXCJvcmlnaW5hbF90aXRsZVwiOlwiUHJlbWl1bVwiLFwic3lzdGVtXCI6XCJaNVwiLFwiZGVzY3JpcHRpb25cIjpcIlByZW1pdW0gLSAzIG1vbnRocyAtIHByZXBhaWQgY29kZXNcIixcImJpbGxpbmdfY3ljbGVfdHlwZVwiOlwiZGF5c1wiLFwiYmlsbGluZ19mcmVxdWVuY3lcIjo5MCxcInByaWNlXCI6Mzk5LFwiY3VycmVuY3lcIjpcIklOUlwiLFwiY291bnRyaWVzXCI6W1wiSU5cIl0sXCJzdGFydFwiOlwiMjAyMi0wMy0xNFQxNzowMzowMFpcIixcImVuZFwiOlwiMjAyNC0xMi0zMVQyMzo1OTowMFpcIixcIm9ubHlfYXZhaWxhYmxlX3dpdGhfcHJvbW90aW9uXCI6ZmFsc2UsXCJyZWN1cnJpbmdcIjpmYWxzZSxcInBheW1lbnRfcHJvdmlkZXJzXCI6W3tcIm5hbWVcIjpcIlplZTVcIixcInByb2R1Y3RfcmVmZXJlbmNlXCI6bnVsbH1dLFwicHJvbW90aW9uc1wiOltdLFwiYXNzZXRfdHlwZXNcIjpbMCw2LDldLFwiYXNzZXRfaWRzXCI6W1wiXCJdLFwiZnJlZV90cmlhbFwiOjAsXCJidXNpbmVzc190eXBlXCI6XCJmcmVlXCIsXCJiaWxsaW5nX3R5cGVcIjpcInByZW1pdW1cIixcIm51bWJlcl9vZl9zdXBwb3J0ZWRfZGV2aWNlc1wiOjIsXCJtb3ZpZV9hdWRpb19sYW5ndWFnZXNcIjpbXSxcInR2X3Nob3dfYXVkaW9fbGFuZ3VhZ2VzXCI6W10sXCJjaGFubmVsX2F1ZGlvX2xhbmd1YWdlc1wiOltdLFwiZHVyYXRpb25fdGV4dFwiOlwiXCIsXCJ2YWxpZF9mb3JfYWxsX2NvdW50cmllc1wiOnRydWUsXCJhbGxvd2VkX3BsYXliYWNrX2R1cmF0aW9uXCI6NixcIm9mZmVyX2lkXCI6MCxcImNhdGVnb3J5XCI6XCJcIixcImFjdHVhbF92YWx1ZVwiOjAsXCJiZWZvcmVUdlwiOnRydWV9LFwic3Vic2NyaXB0aW9uX3N0YXJ0XCI6XCIyMDIzLTEwLTAxVDE3OjI3OjQ4LjAwMFpcIixcInN1YnNjcmlwdGlvbl9lbmRcIjpcIjIwMjMtMTItMzBUMjM6NTk6NTlaXCIsXCJzdGF0ZVwiOlwiYWN0aXZhdGVkXCIsXCJyZWN1cnJpbmdfZW5hYmxlZFwiOmZhbHNlLFwicGF5bWVudF9wcm92aWRlclwiOm51bGwsXCJmcmVlX3RyaWFsXCI6bnVsbCxcImNyZWF0ZV9kYXRlXCI6bnVsbCxcImlwX2FkZHJlc3NcIjpudWxsLFwiY291bnRyeVwiOlwiSU5cIixcImFkZGl0aW9uYWxcIjp7XCJyZWdpb25cIjpcIk1BSEFSQVNIVFJBXCIsXCJjb3VudHJ5XCI6XCJJTlwiLFwicGFydG5lclwiOlwiWkVFNVwiLFwic3Vic190eXBlXCI6XCJpbnRlcm5hbF9zdWJzXCIsXCJjb3Vwb25jb2RlXCI6XCJaNVBQQVAyM1FEU1I2XCIsXCJpcF9hZGRyZXNzXCI6XCIyNDA1OjIwMTo2MDFjOmUwYjU6MzljMzo1NjI3OmE2NmM6MWE2MywgMTg0Ljg1LjIyMC4yMjUsIDQ5LjQ0LjIxNi41LDEwLjI0My42OS43NlwiLFwicGF5bWVudG1vZGVcIjpcIlByZXBhaWRDb2RlXCJ9LFwiYWxsb3dlZF9iaWxsaW5nX2N5Y2xlc1wiOjAsXCJ1c2VkX2JpbGxpbmdfY3ljbGVzXCI6MH1dIiwiYWN0aXZhdGlvbl9kYXRlIjoiMjAyMy0xMC0wMVQxNzoyNzoxOC45MTZaIiwiYW1yIjpbImRlbGVnYXRpb24iXSwiaXNzIjoiaHR0cHM6Ly91c2VyYXBpLnplZTUuY29tIiwiY3VycmVudF9jb3VudHJ5IjoiSU4iLCJjbGllbnRfaWQiOiJyZWZyZXNoX3Rva2VuIiwiYWNjZXNzX3Rva2VuX3R5cGUiOiJEZWZhdWx0UHJpdmlsZWdlIiwidXNlcl90eXBlIjoiUmVnaXN0ZXJlZCIsInNjb3BlIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sImF1dGhfdGltZSI6MTY5NzI5NDAzNSwiZXhwIjoxNjk5OTI0MDM1LCJpYXQiOjE2OTcyOTQwMzUsImp0aSI6ImMxMzc4NmEyLTU3NjgtNDhkYi1hYjU1LTNhYzZiMmUwNDVjOSIsInVzZXJfZW1haWwiOiJtb3ZpZXNhdmluZ2RyaXZlMUBnbWFpbC5jb20iLCJkZXZpY2VfaWQiOiI3NzI4ZDIwNC1hMGIzLTQzZDAtOTY0OS02Nzc0ZTk5OTEzNzgiLCJyZWdpc3RyYXRpb25fY291bnRyeSI6IklOIiwidmVyc2lvbiI6NSwiYXVkIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sInN5c3RlbSI6Ilo1IiwibmJmIjoxNjk3Mjk0MDM1LCJpZHAiOiJsb2NhbCIsInVzZXJfaWQiOiJhNTgwMTgzMC04N2I4LTQ5YTItOGQ3Yy1jZDU3ZmRhMTgzMWEiLCJjcmVhdGVkX2RhdGUiOiIyMDIzLTEwLTAxVDE3OjI3OjE4LjkxNloiLCJhY3RpdmF0ZWQiOnRydWV9.dafCHQhtNLixn0lIEmsuiUZvl2-PWUEYyr73e2W6EZHZj1pGuFjQkdN2rU8TwoPmscZlCKI-8KdxFCDVOWV3UbjKoPBOpjhIYDKPV_APSM2jVl_A9UYWbP8TytpIXB0PYR4fw_233x3_mOnynKCA4vz9xdBdx_jgR4AX2KGlO-IQSetUS9RFRgLuMqYiq7i8_B6hqFjL_Q1XakjcE3p_sgBMBLDzZwe-76643WyJqvI95uVsHaHPkbeyG_T_Gscty_2QWdTPl1v6MR48olkzg441g8jrk9IwQOxzES260m5tXP-VJaUYsHFRgJLIOXTSA5xOqGwXF14_-mfx8joCIw"

        self.x_dd_token = "eyJzY2hlbWFfdmVyc2lvbiI6IjEiLCJvc19uYW1lIjoiTi9BIiwib3NfdmVyc2lvbiI6Ik4vQSIsInBsYXRmb3JtX25hbWUiOiJDaHJvbWUiLCJwbGF0Zm9ybV92ZXJzaW9uIjoiMTA0IiwiZGV2aWNlX25hbWUiOiIiLCJhcHBfbmFtZSI6IldlYiIsImFwcF92ZXJzaW9uIjoiMi41Mi4zMSIsInBsYXllcl9jYXBhYmlsaXRpZXMiOnsiYXVkaW9fY2hhbm5lbCI6WyJTVEVSRU8iXSwidmlkZW9fY29kZWMiOlsiSDI2NCJdLCJjb250YWluZXIiOlsiTVA0IiwiVFMiXSwicGFja2FnZSI6WyJEQVNIIiwiSExTIl0sInJlc29sdXRpb24iOlsiMjQwcCIsIlNEIiwiSEQiLCJGSEQiXSwiZHluYW1pY19yYW5nZSI6WyJTRFIiXX0sInNlY3VyaXR5X2NhcGFiaWxpdGllcyI6eyJlbmNyeXB0aW9uIjpbIldJREVWSU5FX0FFU19DVFIiXSwid2lkZXZpbmVfc2VjdXJpdHlfbGV2ZWwiOlsiTDMiXSwiaGRjcF92ZXJzaW9uIjpbIkhEQ1BfVjEiLCJIRENQX1YyIiwiSERDUF9WMl8xIiwiSERDUF9WMl8yIl19fQ==ott"

        self.json_data = {
            'x-access-token': self.x_access_token,
            'Authorization': 'bearer {}'.format(self.authorization),
            'x-dd-token': self.x_dd_token,
        }

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        self.headers2 = {
            'authority': 'gwapi.zee5.com',
            'accept': '*/*',
            'accept-language': 'en,en-US;q=0.9,en-IN;q=0.8',
            'origin': 'https://www.zee5.com',
            'referer': 'https://www.zee5.com/',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-access-token': self.x_access_token,
        }

    def fetch_episodes_data(self, seriesID, seasonIndex=1):

        params = {
            'translation': 'en',
            'country': 'IN'
        }

        response = requests.get(
            f'https://gwapi.zee5.com/content/tvshow/{seriesID}', params=params, headers=self.headers2).json()

        if int(seasonIndex) == response['season_details']['index']:
            seasonID = response['season_details']['id']

        else:
            print("Requested Season Not Available...")

        episodes_data = []

        url = "https://gwapi.zee5.com/content/tvshow/?season_id={}&type=episode&translation=en&country=IN&asset_subtype=tvshow&page=1&limit=10".format(
            seasonID)

        response = requests.get(url, headers=self.headers2)

        data = response.json()
        total_episodes = data['total_episodes']
        limit = data['limit']

        total_pages = -(-total_episodes // limit)

        for page in range(total_pages + 1):
            sys.stdout.write(
                "\r[+] Extracting Episodes - {}/{}".format(page + 1, total_pages + 1))
            sys.stdout.flush()

            url = url.replace("&page=1", "")
            page_url = f"{url}&page={page}"
            response = requests.get(page_url, headers=self.headers2)
            page_data = response.json()

            if 'episode' in page_data:
                episodes = page_data['episode']
                for ep in episodes:
                    episode_number = ep["episode_number"]

                    # Check if the episode number is not in the set of seen episode numbers

                    episode_info = {
                        'showTitle': ep["tvshow_details"]["title"],
                        'contentID': ep["id"],
                        'seasonNumber': ep["season_details"]["index"],
                        'episodeNumber': episode_number,
                        'episodeTitle': ep["original_title"],
                        'episodeDesc': ep["description"],
                        'thumb': ep["image_url"],
                    }
                    episodes_data.append(episode_info)

        # Sort episodes_data by 'episodeNumber' in ascending order
        episodes_data.sort(key=lambda x: x['episodeNumber'])
        return episodes_data

    def extract_streams(self, contentID):
        response = requests.post(
            f"https://spapi.zee5.com/singlePlayback/getDetails/secure?content_id={contentID}&device_id=iseJrXNCJ3kMOao3drB2000000000000&platform_name=mobile_web&translation=en&user_language=en,hi&country=IN&state=WB&app_version=4.2.2&user_type=premium&check_parental_control=false&uid=111cc006-997e-410f-a12a-0f00fee418fe&ppid=iseJrXNCJ3kMOao3drB2000000000000&version=12", headers=self.headers, json=self.json_data, proxies=proxies).json()

        nl = response.get('keyOsDetails', {}).get('nl')
        sdrm = response.get('keyOsDetails', {}).get('sdrm')

        lic_headers = {}
        lic_url = ""

        if nl and sdrm:
            lic_headers = {'nl': nl, 'customdata': sdrm}
            lic_url = "https://spapi.zee5.com/widevine/getLicense"

        if response.get("error_msg") == "Token Expired":
            raise("ZEE5 TOKEN EXPIRED")

        data = {
            "seriesTitle": response['assetDetails']['title'],
            "mpd": self.get_mpd_url(response['assetDetails']['video_url']['mpd']),
            "license_headers": lic_headers,
            "license": lic_url,
            "seasonNumber": 0,
            "episodeNumber": 0,
            "releaseYear": response['assetDetails']['release_date'][:4],
            "synopsis": response['assetDetails']['description'],
            "name": None,
            "ott": "ZEE5",
        }

        if response['assetDetails'].get("tvshow_name"):
            data["seriesTitle"] = response['assetDetails']['tvshow_name']
            data["episodeName"] = response['assetDetails']['original_title']
            data["episodeNumber"] = int(response['assetDetails']['orderid'])

            for season in response['showDetails']['seasons']:
                if season["id"] == response['showDetails']['season']:
                    data["seasonNumber"] = int(season["orderid"])

            data["name"] = "{} S{:02d}E{:02d} {}".format(
                response['assetDetails']['tvshow_name'].strip(),
                data['seasonNumber'],
                data['episodeNumber'],
                data["episodeName"]
            )

            data["name"] = data["name"].replace(
                "/", "_").replace("~", "").replace(":", "").replace(" - ", "")
        else:
            data["name"] = "{} {}".format(
                response['assetDetails']['title'], response['assetDetails']['release_date'][:4]).replace("/", "_").replace("~", "").replace(":", "")

        return data

    def get_mpd_url(self, mpd_url):
        if "/4K/" in mpd_url and "v2-prime" not in mpd_url:
            mpd = mpd_url.replace("manifest.mpd", "manifest-connected-4k.mpd")
        else:
            mpd = mpd_url

        if self.hevc == True:
            if "connected" in mpd:
                return mpd
            else:
                return mpd
        else:
            return mpd.replace("manifest-connected-4k.mpd", "manifest.mpd")


def extract_pssh(text):
    try:
        pattern = rb"<cenc:pssh>(.*?)</cenc:pssh>"
        matches = re.findall(pattern, text)
        if matches:
            smaller_pssh = min(matches, key=len)
            return smaller_pssh.strip().decode()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred while making the request:", e)
        return None


def extract_pssh_ytdlp(url):
    command = [
        ytdlp,
        "--allow-unplayable-formats",
        "--skip-download",
        "--dump-pages",
        url
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Capture the output as text
            check=True  # Raise an exception if the command fails
        )

        return extract_pssh(base64.b64decode(result.stdout.split("\n")[3]))

    except subprocess.CalledProcessError as e:
        return None


def get_pssh(url):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }, proxies=proxies
        )
        text = response.text
        # print(text)
        pattern = r"<cenc:pssh>(.*?)</cenc:pssh>"
        matches = re.findall(pattern, text)
        if matches:
            smaller_pssh = min(matches, key=len)
            return smaller_pssh.strip()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred while making the request:", e)
        return None


def find_keys_wvclone_api(mpd, lic_url, custom_headers=None):

    # pssh = extract_pssh_ytdlp(mpd)
    pssh = get_pssh(mpd)

    headers = {
        'authority': 'wvclone.fly.dev',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,en-US;q=0.9,en-IN;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://wvclone.fly.dev',
        'referer': 'https://wvclone.fly.dev/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    if custom_headers:

        formatted_lic_headers = ''
        for key, value in custom_headers.items():
            formatted_lic_headers += f'{key} : {value}\n'

        json_data = {
            'password': '',
            'license': lic_url,
            'headers': formatted_lic_headers.rstrip('\n'),
            'pssh': pssh,
            'buildInfo': '',
            'cache': False,
        }

    else:
        json_data = {
            'password': '',
            'license': lic_url,
            'headers': '',
            'pssh': pssh,
            'buildInfo': '',
            'cache': False,
        }

    response = requests.post('https://wvclone.fly.dev/wv',
                             headers=headers, json=json_data)
    return extract_keys_from_text(response.text)


def find_keys(mpd, lic_url, custom_headers=None):
    pssh = PSSH(get_pssh(mpd))
    device_path = wvd_file_path
    license_manager = WidevineLicenseManager(pssh, device_path)
    keys_data = license_manager.extract_keys(lic_url, custom_headers)

    return keys_data


def extract_keys_from_text(data):
    pattern = r"[a-fA-F0-9]{32}:[a-fA-F0-9]{32}"
    keys = re.findall(pattern, data)
    return keys


def mpd_table(url, init_file_name, ott, keys, lic_url):
    videoslist, audioslist, subtitlelist, baseurl, pssh = MPD(
        url, init_file_name, ott, custom_group_tag=GROUP_TAG).parse()

    table_audio_data = ['- {language} ({languageCode}) [{formatID}] [{audio_info}]'.format(
        language=language_mapping(audio['lang'], return_key="en"),
        languageCode=audio['lang'],
        formatID=audio['id'],
        audio_info=audio['audio_codec_release_name'] +
        f" - {audio['bandwidth_release_name']}bps"

    ) for audio in audioslist]

    table_videos_list = ['- {resolution} {vcodec} [{formatID}] - {bandwidth}Kbps'.format(
        resolution="{}x{}".format(video['width'], video['height']),
        vcodec=video['video_codec_release_name'],
        formatID=video['id'],
        bandwidth=int(video['bandwidth']) / 1000
    ) for video in videoslist]

    if subtitlelist is not None:
        table_subs_list = ['- {lang} {url}'.format(
            lang=subtitle['lang'],
            url=subtitle['url']
        ) for subtitle in subtitlelist]

    else:
        table_subs_list = None

    table = ''

    if table_audio_data:
        table += 'Audio:\n'
        table += '\n'.join(table_audio_data) + '\n\n'

    if table_videos_list:
        table += 'Video:\n'
        table += '\n'.join(table_videos_list) + '\n\n'

    if table_subs_list:
        table += 'Subtitle:\n'
        table += '\n'.join(table_subs_list) + '\n\n'

    if baseurl:
        table += 'BASE URL:\n'
        table += baseurl + '\n\n'

    if pssh:
        table += 'PSSH:\n'
        table += pssh + '\n\n'

    if keys:
        table += 'KEYS:\n'
        table += "\n".join(keys) + "\n\n" if isinstance(keys,
                                                        list) else keys + '\n\n'

    if lic_url:
        table += 'LICENSE URL:\n'
        table += lic_url + '\n\n'

    return table


class WidevineLicenseManager:
    def __init__(self, pssh, device_path):
        self.pssh = pssh
        self.device_path = device_path
        self.device = None
        self.cdm = None
        self.session_id = None

    def initialize(self):
        self.device = Device.load(self.device_path)
        self.cdm = Cdm.from_device(self.device)

    def open_session(self):
        self.session_id = self.cdm.open()

    def get_license_challenge(self):
        challenge = self.cdm.get_license_challenge(self.session_id, self.pssh)
        return challenge

    def parse_license(self, license_data):
        self.cdm.parse_license(self.session_id, license_data)

    def get_keys_data(self):
        keys_data = ""
        for key in self.cdm.get_keys(self.session_id):
            if key.type != "SIGNING":
                keys_data += f"{key.kid.hex}:{key.key.hex()}\n"
        return keys_data.strip().split()

    def close_session(self):
        self.cdm.close(self.session_id)

    def extract_keys(self, license_url, custom_headers=None):
        self.initialize()
        self.open_session()

        challenge = self.get_license_challenge()

        license_response = requests.post(
            license_url, data=challenge, headers=custom_headers)
        license_response.raise_for_status()

        self.parse_license(license_response.content)

        keys_data = self.get_keys_data()

        self.close_session()

        return keys_data


class FilenameGenerator:
    def __init__(self, audioslist, videoslist, subtitleslist, init_file_name, ott, custom_group_tag, resolution, language_order):
        self.audioslist = audioslist
        self.videoslist = videoslist
        self.subtitleslist = subtitleslist
        self.init_file_name = init_file_name
        self.ott = ott
        self.custom_group_tag = custom_group_tag
        self.resolution = resolution
        self.language_order = language_order

    def get_subtitle_write_data(self):

        if self.subtitleslist is not None:
            if len(self.subtitleslist) == 1:
                if filename_format == "p2p":
                    subs_write = ".ESub"
                else:
                    subs_write = "ESub"
            else:
                if filename_format == "p2p":
                    subs_write = ".MSubs"
                else:
                    subs_write = "MSubs"
        else:
            subs_write = ""

        return subs_write

    def generate_filename(self):
        subtitle_write_data = self.get_subtitle_write_data()
        unique_audio_configs = self._group_unique_audio_configs()
        audio_groups = self._group_languages_by_audio_config(
            unique_audio_configs)

        filename_parts = self._generate_filename_parts(audio_groups)
        video_codec = self.videoslist['video_codec_release_name']
        video_resolution = f"{self.videoslist['height']}p"

        video_quality = (
            "." + self.videoslist["quality"] if "quality" in self.videoslist and self.videoslist["quality"] != "" else "")
        video_codec_v2 = "x264" if video_codec == "H264" else (
            "x265" + (" 10bit" if "10bit" in video_codec else "") if "H265" or "HEVC" in video_codec else "")

        if filename_format == "p2p":
            filename = f"{self.init_file_name}.{video_resolution}{video_quality}.{self.ott}.WEB-DL.{'-'.join(filename_parts)}.{video_codec}{subtitle_write_data}-{self.custom_group_tag}.mkv"
            filename.replace(" ", ".").replace(
                "/", "").replace(":", "").replace(",", "")
        else:
            filename = f"{self.init_file_name} {video_resolution}{video_quality.replace('.' , ' ')} {self.ott} WEB-DL {video_codec_v2} [{' - '.join(filename_parts)}] {subtitle_write_data}{underscore_before_after_group_tag}{self.custom_group_tag}{underscore_before_after_group_tag}.mkv"
            filename.replace("/", "").replace(":", "").replace(",", "")

        return filename

    def _group_unique_audio_configs(self):
        unique_audio_configs = {}
        for audio in self.audioslist:
            config = (audio['audio_codec_release_name'].rsplit(
                '.', 1)[0], audio['bandwidth_release_name'])
            if config not in unique_audio_configs:
                unique_audio_configs[config] = []
            unique_audio_configs[config].append(audio)
        return unique_audio_configs

    def _group_languages_by_audio_config(self, unique_audio_configs):
        audio_groups = {}
        for config, audio_data in unique_audio_configs.items():
            langs = sorted(
                set([audio['lang'] for audio in audio_data]), key=self._custom_sort_key)
            # lang_concatenated = "-".join(langs)
            lang_concatenated = "-".join(langs)
            audio_groups[lang_concatenated] = audio_data
        return audio_groups

    def _custom_sort_key(self, lang):
        return self.language_order.index(lang)

    def _generate_filename_parts(self, audio_groups):
        filename_parts = []
        for lang_group, audio_data in audio_groups.items():
            audio_codec = audio_data[0]['audio_codec_release_name']
            audio_bandwidths = audio_data[0]['bandwidth_release_name']

            lang_group = [language_mapping(
                lang.strip(), "639-2").upper() for lang in lang_group.split("-")]
            if filename_format == "p2p":
                lang_group = "-".join(lang_group)
            else:
                lang_group = " + ".join(lang_group)
            if filename_format == "p2p":
                filename_parts.append(
                    f"{lang_group}.{audio_codec}.{audio_bandwidths}")
            else:
                filename_parts.append(
                    f"{lang_group} ({audio_codec} - {audio_bandwidths})")
        return filename_parts


def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result


def get_zee5_id(url):
    id_pattern = r'/details/[^/]+/([^/]+)/?$'
    match = re.search(id_pattern, url)
    if match:
        return match.group(1).split("?")[0]
    else:
        return None


def save_file(data, file_name):
    json_object = json.dumps(data, indent=4)

    dest = f"{file_name}"

    # Writing to extracted_keys.json
    with open(dest, "w+") as outfile:
        outfile.write(json_object)


class ZEE5:
    def __init__(self, args):
        self.ott_api_slug = "zee5"
        self.parsed_args = args

        if "web-series" in self.parsed_args.url:
            self.setup_episode_start_end()
        if "tv-shows" in self.parsed_args.url:
            self.setup_episode_start_end()

        self.parsed_args.hevc_value = str(
            self.parsed_args.hevc_value).strip().lower()

        # # Check if the input is "true" (case-insensitive)
        self.parsed_args.hevc_value = True if self.parsed_args.hevc_value == "true" else (
            False if self.parsed_args.hevc_value == "false" else sys.exit())

    def extract_all_episodes(self):
        seriesID = get_zee5_id(self.parsed_args.url)

        self.eps = ZEE5API(
            hevc=self.parsed_args.hevc_value).fetch_episodes_data(seriesID, self.parsed_args.season)

    def setup_episode_start_end(self):

        self.extract_all_episodes()

        if self.parsed_args.episode is None:
            self.episode_start = 1
            self.episode_end = int(len(self.eps))
        elif "-" in self.parsed_args.episode:
            self.episode_start, self.episode_end = map(
                int, self.parsed_args.episode.split("-")
            )
        else:
            self.episode_start = int(self.parsed_args.episode)
            self.episode_end = 0

    def single_index_processor(self, index):

        # print(self.parsed_args)

        if "movies" in self.parsed_args.url:
            contentID = get_zee5_id(self.parsed_args.url)

        else:
            # Assuming ZEE5 Actually has all the Episodes
            contentID = next((episode['contentID'] for episode in self.eps if episode.get(
                'episodeNumber') == index), None)

            if contentID is None:
                print_message("ERROR", "EPISODE",
                              "REQUESTED EPISODE NOT FOUND Try Again...")

        stream_details = ZEE5API(
            hevc=self.parsed_args.hevc_value).extract_streams(contentID)

        mpd, lic_url, lic_headers, name, ott = stream_details.get("mpd"), stream_details.get(
            "license"), stream_details.get("license_headers"), stream_details.get("name"), stream_details.get("ott")

        if not lic_url == "":
            key = find_keys(mpd, lic_url, lic_headers)
        else:
            key = None

        print_message("EXTRACTING KEYS", "KEYS", " ".join(key))
        print("\n")

        if self.parsed_args.info == "True" or self.parsed_args.info == True:
            print(mpd_table(mpd, name, ott, key, lic_url))
            return

        try:

            Processor(mpd, key, video_resolution=self.parsed_args.resolution, video_quality=self.parsed_args.vquality,
                      alang=self.parsed_args.alang, audio_quality=self.parsed_args.aquality, audio_codec=self.parsed_args.acodec, init_file_name=name, ott=ott, und_lang=None).start_process()

        except Exception as e:
            print_message("ERROR", f"INDEX - {index}", e)
            pass

    def tv_shows_dl(self):
        print_message("Extracting Data", "URL", self.parsed_args.url)

        if self.episode_end == 0:
            self.single_index_processor(self.episode_start)
        else:
            for ep_index in range(self.episode_start, (self.episode_end + 1)):
                self.single_index_processor(ep_index)

    def movie_dl(self):
        self.single_index_processor(index=None)

    def start_process(self):
        if "web-series" in self.parsed_args.url:
            self.tv_shows_dl()
        elif "tv-shows" in self.parsed_args.url:
            self.tv_shows_dl()
        elif "movies" in self.parsed_args.url:
            self.movie_dl()
        else:
            print_message("ERROR", "URL",
                          "Not matching either with Series or Movie URL. Try Again. Example - https://www.zee5.com/movies/details/gadar-2/0-0-1z5437988")


class Processor():
    def __init__(self, link, key, video_resolution=None, video_quality=None, audio_codec=None, audio_quality=None, alang=None, und_lang=None, init_file_name=None, ott=None):

        self.link = link
        self.key = key
        self.video_resolution = video_resolution
        self.video_quality = video_quality
        self.audio_codec = audio_codec
        self.audio_quality = audio_quality
        self.alang = alang
        self.und_lang = und_lang
        self.init_file_name = init_file_name
        self.ott = ott
        self.custom_group_tag = GROUP_TAG

        self.process_start = time.time()
        self.end_code = str(time.time()).replace(".", "")

        self.video_data, self.audio_data, self.subtitles_data, self.baseurl, self.pssh, self.final_file_name = MPD(
            link, init_file_name, ott, self.custom_group_tag).refine(video_resolution=self.video_resolution, video_quality=self.video_quality, audio_codec=self.audio_codec, audio_quality=self.audio_quality, audio_languages=self.alang, und_lang=self.und_lang)

    def download_audio_stream(self, stream_format, filename):
        dest = os.path.join(dl_folder, f"{filename}.m4a")
        try:
            cmd = [
                f"{ytdlp}",
            ]

            if proxy_url and proxy_url.strip():  # Check if proxy_url is not empty or None
                cmd.extend(["--proxy", proxy_url])

            cmd.extend(["--allow-unplayable-formats",
                        "-f",
                        str(stream_format),
                        f"{self.link}",
                        "-o",
                        dest,
                        "--external-downloader",
                        f"{aria2c}",
                        ])
            dl_process = dl_process = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL)
            dl_process.wait()
        except Exception as e:
            raise Exception(f"Error Running YT-DLP Command {e}")

    def mpd_download(self):
        threads = []

        for i, audio_info in enumerate(self.audio_data):
            stream_format = audio_info["id"]
            filename = f"enc_{stream_format}_{self.end_code}"
            thread = threading.Thread(
                target=self.download_audio_stream, args=(
                    stream_format, filename)
            )
            threads.append(thread)
            thread.start()
            print_message("DOWNLOADING", "⬇️",
                          f"AUDIO STREAM {i + 1} of {len(self.audio_data)}")

        try:
            video_format = self.video_data["id"]
            dest = os.path.join(
                dl_folder, f"enc_{video_format}_{self.end_code}.mp4")

            video_cmd = [
                f"{ytdlp}",
            ]
            if proxy_url and proxy_url.strip():  # Check if proxy_url is not empty or None
                video_cmd.extend(["--proxy", proxy_url])

            video_cmd.extend([
                "--allow-unplayable-formats",
                "-f",
                str(video_format),
                f"{self.link}",
                "-o",
                dest,
                "--external-downloader",
                f"{aria2c}",
            ])
            print_message("DOWNLOADING", "⬇️", "VIDEO STREAM")
            subprocess.call(video_cmd, stdout=subprocess.DEVNULL)
        except Exception as e:
            raise Exception(f"Error Downloading Video File {e}")

        for thread in threads:
            thread.join()

        return self.end_code

    def decrypt(self):
        print_message("DECRYPTING", "⬇️", "VIDEO + AUDIO")

        try:
            for audio_info in self.audio_data:
                stream_format = audio_info["id"]
                enc_dl_audio_file_name = os.path.join(
                    dl_folder, f"enc_{stream_format}_{self.end_code}.m4a")
                dec_out_audio_file_name = os.path.join(
                    dl_folder, f"dec_{stream_format}_{self.end_code}.m4a")

                if isinstance(self.key, list):
                    cmd_audio_decrypt = [
                        f"{mp4decrypt}"]

                    for k in self.key:
                        cmd_audio_decrypt.append(str("--key"))
                        cmd_audio_decrypt.append(str(k))

                    cmd_audio_decrypt.append(str(enc_dl_audio_file_name)),
                    cmd_audio_decrypt.append(str(dec_out_audio_file_name))

                else:

                    cmd_audio_decrypt = [
                        f"{mp4decrypt}",
                        "--key",
                        str(self.key),
                        str(enc_dl_audio_file_name),
                        str(dec_out_audio_file_name)

                    ]
                subprocess.run(cmd_audio_decrypt, stdout=subprocess.DEVNULL)
                try:
                    os.remove(enc_dl_audio_file_name)
                except:
                    pass

            video_format = self.video_data["id"]
            enc_dl_video_file_name = os.path.join(
                dl_folder, f"enc_{video_format}_{self.end_code}.mp4")
            dec_out_video_file_name = os.path.join(
                dl_folder, f"dec_{video_format}_{self.end_code}.mp4")

            cmd_video_decrypt = [f"{mp4decrypt}"]
            if isinstance(self.key, list):
                cmd_video_decrypt = [
                    f"{mp4decrypt}"]

                for k in self.key:
                    cmd_video_decrypt.append(str("--key"))
                    cmd_video_decrypt.append(str(k))

                cmd_video_decrypt.append(str(enc_dl_video_file_name)),
                cmd_video_decrypt.append(str(dec_out_video_file_name))

            else:
                cmd_video_decrypt = [
                    f"{mp4decrypt}",
                    "--key",
                    str(self.key),
                    str(enc_dl_video_file_name),
                    str(dec_out_video_file_name)

                ]
            try:
                subprocess.run(cmd_video_decrypt, stdout=subprocess.DEVNULL)
            except Exception as e:
                raise Exception(str(e))

            try:
                os.remove(enc_dl_video_file_name)
            except:
                pass

        except Exception as e:
            raise Exception("Error During Decryption")

        return self.end_code

    def dl_subs(self):

        if self.subtitles_data is not None:
            for sub in self.subtitles_data:
                subs_lang = sub["lang"]
                dest = os.path.join(
                    dl_folder, f"subtitle_{subs_lang}_{self.end_code}.vtt")
                subs_url = sub['baseURL'] + sub["url"]
                subs_dl_cmd = [
                    f"{ytdlp}",
                ]

                if proxy_url and proxy_url.strip():  # Check if proxy_url is not empty or None
                    subs_dl_cmd.extend(["--proxy", proxy_url])

                subs_dl_cmd.extend([
                    f"{subs_url}",
                    "-o",
                    dest,
                    "--external-downloader",
                    f"{aria2c}"
                ])
                print_message("DOWNLOADING", "⬇️",
                              f"SUBTITLE")
                print_message("", "URL 🔗",
                              subs_url)

                subprocess.call(subs_dl_cmd, stdout=subprocess.DEVNULL)

    def mux_video(self, startTime=None, endTime=None):

        file_prefix = "enc" if self.key is None else "dec"

        dec_out_video_file_name = os.path.join(
            dl_folder, f"{file_prefix}_{self.video_data['id']}_{self.end_code}.mp4")
        audio_files = [
            os.path.join(
                dl_folder, f"{file_prefix}_{audio_info['id']}_{self.end_code}.m4a")
            for audio_info in self.audio_data
        ]

        ffmpeg_opts = ["ffmpeg", "-y", "-i", dec_out_video_file_name]

        for audio_file, audio_info in zip(audio_files, self.audio_data):
            lang = audio_info["lang"]
            ffmpeg_opts.extend(["-i", audio_file])

        if self.subtitles_data is not None:

            subs_file = [
                os.path.join(
                    dl_folder, f"subtitle_{sub['lang']}_{self.end_code}.vtt")
                for sub in self.subtitles_data
            ]

            for individual_subs_file in subs_file:
                ffmpeg_opts.extend(["-i", individual_subs_file])

        if startTime is not None and endTime is not None:
            ffmpeg_opts.extend(["-ss", f"{startTime}"])
            ffmpeg_opts.extend(["-to", f"{endTime}"])

        ffmpeg_opts.extend(["-map", "0:v:0"])

        for i in range(len(self.audio_data)):
            ffmpeg_opts.extend(["-map", f"{i+1}:a:0"])

        if self.subtitles_data is not None:
            for i in range(len(self.subtitles_data)):
                ffmpeg_opts.extend(["-map", f"{len(self.audio_data)+1}:s:0"])

        ffmpeg_opts.extend(
            ["-metadata", f"encoded_by={self.custom_group_tag}"])
        ffmpeg_opts.extend(["-metadata:s:a", f"title={self.custom_group_tag}"])
        ffmpeg_opts.extend(["-metadata:s:v", f"title={self.custom_group_tag}"])

        if self.subtitles_data is not None:
            ffmpeg_opts.extend(
                ["-metadata:s:s", f"title={self.custom_group_tag}"])

        for i, audio_info in enumerate(self.audio_data):
            lang = audio_info["lang"]
            ffmpeg_opts.extend(
                ["-metadata:s:a:{0}".format(i), f"language={lang}"])

        if self.subtitles_data is not None:
            for i in range(len(self.subtitles_data)):
                ffmpeg_opts.extend(
                    ["-metadata:s:s:{0}".format(i), f"language={self.subtitles_data[i]['lang']}"])

        out_name = f"{self.end_code}.mkv"
        out_file_name = self.final_file_name
        ffmpeg_opts.extend(["-c", "copy", out_name])

        try:
            subprocess.check_call(ffmpeg_opts, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFMPEG Error: {e}")

        try:
            os.rename(out_name, out_file_name)
        except OSError as e:
            raise Exception(f"OSError: {e}",)

        for audio_file in audio_files:
            try:
                os.remove(audio_file)
            except OSError as e:
                print(f"OSError: {e}")
                pass
        try:
            os.remove(dec_out_video_file_name)
        except OSError as e:
            print(f"OSError: {e}")
            pass

        return out_file_name

    def start_process(self, startTime=None, endTime=None):

        task_start_time = time.time()
        print(
            '[+] Downloading {}'.format(colored_text(self.final_file_name, "blue")))
        self.mpd_download()

        self.dl_subs()

        if self.key is not None:
            self.decrypt()

        print(
            '[+] Muxing {}'.format(colored_text(self.final_file_name, "blue")))

        out_file_name = self.mux_video(startTime, endTime)

        print(colored_text("[+] TASK COMPLTED IN", "cyan"),
              get_readable_time(time.time() - task_start_time))

        return out_file_name


parser_data = {
    "zee5": [
        {
            "short_parsername": "url",
            "long_parsername": "url",
            "help": "Provide ZEE5 URL (Can be a Complete Season URL or a Movie URL)",
            "example": "https://www.zee5.com/movies/details/gadar-2/0-0-1z5437988",
            "required": True,
            "default": None,
        },
        {
            "short_parsername": "s",
            "long_parsername": "season",
            "example": "1",
            "help": "DL Complete Season",
            "required": None,
            "default": None,
        },
        {
            "short_parsername": "e",
            "long_parsername": "episode",
            "example": "[2] or [1-10]",
            "help": "DL Episodes. Use for Individial Episodes or Episodes in range (1-10) or don't use this parser command to DL all Available Episodes",
            "required": None,
            "default": None,
        },
        {
            "short_parsername": "r",
            "long_parsername": "resolution",
            "example": "1080p, 720p, 480p",
            "help": "If Requested Resolution not in MPD, then takes the highest resolution",
            "default": None,
            "required": None,
        },
        {
            "short_parsername": "info",
            "long_parsername": "info",
            "example": "True",
            "help": "Get Detailed Stream Info (Skips Download)",
            "default": False,
            "required": None,
        },
        {
            "short_parsername": "alang",
            "long_parsername": "alang",
            "example": "hi-ta-te",
            "help": "DL Particular Audios only if available in MPD, use 639-1 code of that language",
            "default": None,
            "required": None,
        },
        {
            "short_parsername": "vquality",
            "long_parsername": "vquality",
            "example": "HQ, LQ",
            "help": "DL HQ or LQ Versions of that Resolution",
            "default": "HQ",
            "required": None,
        },
        {
            "short_parsername": "aquality",
            "long_parsername": "aquality",
            "example": "HQ, MQ, LQ",
            "help": "DL High, Medium, Low Versions of that Audio Bitrate",
            "default": None,
            "required": None,
        },
        {
            "short_parsername": "acodec",
            "long_parsername": "acodec",
            "example": "ddplus, dd+, dd, dolbydigial, aac",
            "help": "Audio Codec to be downloaded. Defaults to best available",
            "default": None,
            "required": None,
        },
        {
            "short_parsername": "hevc",
            "long_parsername": "hevc_value",
            "example": "Add True or true / False or false to select/not select HEVC MPD",
            "help": "Try Extracting HEVC if set to True",
            "default": False,
            "required": None,
        },

    ]

}


def ott_argument_parser():
    parser = argparse.ArgumentParser()
    ott = "zee5"  # Replace with your desired OTT value

    for data in parser_data[ott]:
        # Convert long and short parser names to command-line argument format
        long_arg = f"--{data['long_parsername']}"
        short_arg = f"-{data['short_parsername']}"

        # Add the argument to the argparse parser
        parser.add_argument(
            long_arg,
            short_arg,
            help=data["help"],
            default=data["default"],
            required=data["required"],
            # Handle optional arguments
            nargs='?' if data['required'] is None else None,
        )

    parsed_args = parser.parse_args()
    ZEE5(parsed_args).start_process()


def print_help_message(parser_data_key):
    if parser_data_key in parser_data:
        print(colored_text(
            f"PARSER DATA HELP FOR '{parser_data_key.upper()}' - ", "green"))
        for item in parser_data[parser_data_key]:
            short_name = item["short_parsername"]
            example = item["example"]
            help_text = item["help"]
            required = item["required"]
            default = item["default"]

            required_str = " (Required)" if required else ""
            default_str = f" (Default: {default})" if default is not None else ""

            print(
                f"{colored_text(f'  -{short_name},', 'cyan')}{required_str}{default_str}"
            )
            print(f"    {help_text}")
            print(f"    Example: {colored_text(example , 'green')}")
            print()


def colored_text(text, color):
    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m",
    }
    if colored_text_config is True:
        return f"{colors[color]}{text}{colors['reset']}"
    else:
        return text


def custom_sort(audio):
    # Assign a high index if the language is not in language_order
    lang_index = language_order.index(
        audio["lang"]) if audio["lang"] in language_order else len(language_order)
    return (lang_index, audio["lang"])


def language_mapping(language_code, return_key=None):
    with open(languages_info_file_path, "r") as json_file:
        language_info = json.load(json_file)
    for code, info in language_info.items():
        if (
            code == language_code
            or info.get("639-1") == language_code
            or info.get("639-2") == language_code
            or "en" in info and info["en"][0].lower() == language_code.lower()
        ):
            return_value = info.get(return_key)
            if return_key == "en" and return_value:
                return return_value[0]
            return return_value or info.get("639-1")

    # If the language_code is not found, return an error message
    raise Exception(f"Language code '{language_code}' not found.")


def print_message(first, second, third):
    print(MESSAGE.format(colored_text(first, "green"), colored_text(
        second, "blue"), colored_text(third, "cyan")))


class MPD():
    def __init__(self, url, init_file_name, ott, custom_group_tag):
        self.url = url
        if filename_format == "p2p":
            self.init_file_name = init_file_name.replace(" ", ".")
        else:
            self.init_file_name = self.format_movie_title(init_file_name)
        self.ott = ott
        self.custom_group_tag = custom_group_tag

        self.AUDIO_CODEC_MAP = {
            "mp4a.40.2": "AAC", "ac-3": "DD", "ec-3": "DD+"}
        self.CHANNEL_MAP = {"F801": "5.1", "6.0": "5.1", "6": "5.1",
                            "2.0": "2.0", "2": "2.0", "1.0": "2.0", "1": "2.0"}
        self.AUDIO_CODEC_v2_MAP = {"aac": "mp4a.40.2", "dd": "ac-3", "dd+": "ec-3", "dolby": "ac-3",
                                   "dolbydigital+": "ec-3", "ddplus": "ec-3", "mp4a.40.2": "mp4a.40.2", "ac-3": "ac-3", "ec-3": "ec-3"}

    def format_movie_title(self, title):
        match = re.search(r'\b\d{4}\b$', title)

        if match:
            release_year = match.group()
            formatted_title = re.sub(
                fr'\b{release_year}\b', f'({release_year})', title)
            return formatted_title
        else:
            return title

    def find_atmos(self, json_data):
        json_text = json.dumps(json_data)
        pattern = r'\bJOC\b'
        matches = re.findall(pattern, json_text, re.IGNORECASE)
        return matches

    def extract_pssh(self, text):
        pattern = r"<cenc:pssh>(.*?)</cenc:pssh>"
        matches = re.findall(pattern, text)
        if matches:
            smaller_pssh = min(matches, key=len)
            return smaller_pssh.strip()
        else:
            return None

    def round_bitrate(self, bitrate):
        bits = [640, 448, 384, 192, 128, 96, 64, 32]
        nearest_bitrate = min(bits, key=lambda x: abs(x - bitrate))
        return nearest_bitrate

    def video_codec_mapping(self, video_codec):
        codec_mapping = {
            "hvc": "HEVC",
            "hev1.2": "HEVC.10bit",
            "hev1.1": "HEVC",
            "hevc": "HEVC",
            "avc": "H264"
            # Add more mappings as needed
        }
        for substring, title in codec_mapping.items():
            if substring in video_codec.lower():
                return title

        return "H264"

    def parse(self, und_lang=None):
        audioslist, videoslist, subtitlelist = list(), list(), list()
        text = requests.get(self.url, proxies=proxies, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            'x-playback-session-id': "9c7631d21edd4a65a92b2b641c8a13a2-1634808345996"
        }).text
        # text = open(self.file_path, 'r').read()

        mpd = json.loads(json.dumps(xmltodict.parse(text)))
        self.baseurl = re.sub(r'[^\/]*$', '', self.url)
        periods = mpd['MPD']['Period']
        if not isinstance(periods, list):
            periods = [periods]

        global periodsNumber
        periodsNumber = len(periods)

        adaptationSet = periods[0]['AdaptationSet']

        for ad in adaptationSet:
            if not isinstance(ad['Representation'], list):
                ad['Representation'] = [ad['Representation']]
            for item in ad['Representation']:
                if (item.get('@mimeType', False) or ad.get('@mimeType')) == 'audio/mp4':

                    is_atmos = True if len(self.find_atmos(ad)) >= 1 else False
                    lang = und_lang if und_lang else ad.get(
                        "@lang", False) or und_lang
                    codec = item.get('@codecs', '') if item.get('@codecs',
                                                                '') != "" else ad.get("@codecs", "mp4a.40.2")
                    channel = ad.get('AudioChannelConfiguration', {}).get(
                        '@value', "2.0")
                    bandwidth = int(item.get("@bandwidth", "126000"))

                    auddict = {
                        # 'lang': ad.get('@lang', False) or 'und',
                        'lang': language_mapping(lang),
                        'id': item["@id"].replace("/", "_"),
                        "audio_codec_release_name": "{}{}{}".format(self.AUDIO_CODEC_MAP.get(
                            codec), self.CHANNEL_MAP.get(channel), ((".ATMOS" if filename_format == "p2p" else " ATMOS") if is_atmos == True else "")),
                        "bandwidth_release_name": str(self.round_bitrate(int(bandwidth / 1000)))
                        + (p2p_audio_bitrate if filename_format ==
                           "p2p" else non_p2p_audio_bitrate),
                        "channels": self.CHANNEL_MAP.get(channel),
                        'codec': codec,
                        'bandwidth': item.get('@bandwidth', '125'),
                        'label': language_mapping(lang, return_key="en")
                    }
                    audioslist.append(auddict)

        for ad in adaptationSet:
            if not isinstance(ad['Representation'], list):
                ad['Representation'] = [ad['Representation']]
            for item in ad['Representation']:
                if (item.get('@mimeType', False) or ad.get('@mimeType')) == 'video/mp4':
                    pssh = self.extract_pssh(text)
                    try:
                        viddict = {
                            'width': item['@width'],
                            'height': item['@height'],
                            'id': item['@id'],
                            'codec': item.get('@codecs', 'h264'),
                            'bandwidth': item.get('@bandwidth', '125'),
                            "video_codec_release_name": self.video_codec_mapping(
                                item.get("@codecs", "avc")
                            ),
                        }
                        videoslist.append(viddict)
                    except Exception:
                        continue

        for ad in adaptationSet:
            if not isinstance(ad['Representation'], list):
                ad['Representation'] = [ad['Representation']]
            for item in ad['Representation']:
                if (item.get('@mimeType', False) or ad.get('@mimeType')) == 'text/vtt':
                    subdict = {
                        'lang': ad.get('@lang', 'eng'),
                        'url': item.get('BaseURL'),
                        'baseURL': self.baseurl
                    }
                    subtitlelist.append(subdict)

        if len(subtitlelist) == 0:
            subtitlelist = None

        self.videoslist = videoslist
        self.audioslist = audioslist
        self.subtitlelist = subtitlelist
        self.pssh = pssh

        return videoslist, audioslist, subtitlelist, self.baseurl, pssh

    def get_highest_audio_codec(self, audioslist):
        codec_order = ["ec-3", "ac-3", "mp4a.40.2"]
        filtered_audios = []

        for codec in codec_order:
            for audio in audioslist:
                if codec in audio["codec"]:
                    # Append matching audio to the filtered list
                    filtered_audios.append(audio)

        if filtered_audios:
            return filtered_audios  # Return the filtered list if any matches were found
        else:
            return audioslist

    def filter_audio_quality(self, audioslist, audio_quality):
        lang_groups = {}  # Dictionary to group audio items by lang

        for audio in audioslist:
            lang = audio["lang"]
            if lang not in lang_groups:
                lang_groups[lang] = []
            lang_groups[lang].append(audio)

        filtered_audios = []

        for lang, audio_group in lang_groups.items():
            if audio_quality == "HQ":
                selected_audio = max(
                    audio_group, key=lambda x: int(x["bandwidth"]))
            elif audio_quality == "MQ":
                selected_audio = self.find_mid_value(audioslist, 'bandwidth')
            elif audio_quality == "LQ":
                selected_audio = min(
                    audio_group, key=lambda x: int(x["bandwidth"]))
            else:
                # Default to "HQ" if no audio_quality is specified
                selected_audio = max(
                    audio_group, key=lambda x: int(x["bandwidth"]))

            filtered_audios.append(selected_audio)

        return filtered_audios

    def mid(self, iterable, key=None):
        if key is None:
            def key(x): return x
        sorted_iterable = sorted(iterable, key=key)
        length = len(sorted_iterable)
        if length == 0:
            raise ValueError("mid() arg is an empty sequence")
        middle_index = length // 2
        return sorted_iterable[middle_index]

    def find_mid_value(self, data_list, key):
        sorted_data = sorted(data_list, key=lambda x: int(x[key]))
        middle_index = len(sorted_data) // 2
        return sorted_data[middle_index]

    def refine(self, video_resolution=None, video_quality=None, audio_languages=None, audio_codec=None, audio_quality="HQ", und_lang=None):

        self.parse(und_lang=und_lang)

        # VIDEO RESOLUTION
        if video_resolution:

            filtered_video_data = [
                video
                for video in self.videoslist
                if int(video["height"]) == int(video_resolution.replace("p", ""))
            ]

            if filtered_video_data:
                videoslist = filtered_video_data
            else:
                # No videos matched the specified resolution; use the highest resolution
                videoslist = [
                    max(self.videoslist, key=lambda x: int(x["height"]))]
        else:
            # Use the video with the highest resolution by default
            videoslist = [max(self.videoslist, key=lambda x: int(x["height"]))]

        # VIDEO QUALITY
        if video_quality:
            if video_quality == "HQ":
                selected_video = max(
                    videoslist, key=lambda x: int(x["bandwidth"]))
                selected_video["quality"] = "HQ" if len(videoslist) > 1 else ""
            elif video_quality == "LQ":
                selected_video = min(
                    videoslist, key=lambda x: int(x["bandwidth"]))
                selected_video["quality"] = "LQ" if len(videoslist) > 1 else ""
            else:
                selected_video = max(
                    videoslist, key=lambda x: int(x["bandwidth"]))
                selected_video["quality"] = "HQ" if len(videoslist) > 1 else ""
        else:
            selected_video = max(videoslist, key=lambda x: int(x["bandwidth"]))
            selected_video["quality"] = "HQ" if len(videoslist) > 1 else ""
        videoslist = selected_video

        # DEFAULT AUDIO SORT

        self.audioslist.sort(key=custom_sort)
        audioslist = self.audioslist

        # AUDIO LANGUAGE

        if audio_languages:
            requested_languages = audio_languages.split("-")
            filtered_audio_data = [
                audio for audio in audioslist if audio["lang"] in requested_languages
            ]

            if filtered_audio_data:
                audioslist = filtered_audio_data

        # AUDIO CODEC
        if audio_codec:
            filtered_audio_data = [audio for audio in audioslist if self.AUDIO_CODEC_v2_MAP.get(
                audio_codec) in audio["codec"]] or self.get_highest_audio_codec(audioslist)

            audioslist = filtered_audio_data

        else:

            # Group by language and find the one with the highest bandwidth for each language
            unique_lang_audios = {}
            for audio in audioslist:
                lang = audio["lang"]
                if lang not in unique_lang_audios or int(audio["bandwidth"]) > int(
                    unique_lang_audios[lang]["bandwidth"]
                ):
                    unique_lang_audios[lang] = audio

            audioslist = list(unique_lang_audios.values())

        # AUDIO QUALITY
        if audio_quality:
            audioslist = self.filter_audio_quality(audioslist, audio_quality)

        # Filename

        filename_generator = FilenameGenerator(audioslist, videoslist, self.subtitlelist, self.init_file_name,
                                               self.ott, self.custom_group_tag, videoslist["height"], language_order)
        filename = filename_generator.generate_filename()

        return videoslist, audioslist, self.subtitlelist, self.pssh, self.baseurl, filename


if __name__ == "__main__":
    ott_argument_parser()
