# import re
# import os
# import json
# import requests
# import subprocess
# import threading
# import time
# import argparse
# import sys
# import json
# import xmltodict
# import requests
# import base64
# import time
# from pywv.device import Device
# from pywv.pssh import PSSH
# from pywv.cdm import Cdm

# proxy_url = ""


# proxies = {
#     "https": proxy_url,
#     "http": proxy_url
# } if proxy_url and proxy_url.strip() else None

# colored_text_config = False

# MESSAGE = "\n[+] {}\n[+] {} : {}"

# GROUP_TAG = "chung-C"

# filename_format = "p2p"  # p2p or non-p2p

# p2p_audio_bitrate = "K"

# non_p2p_audio_bitrate = "Kbps"

# underscore_before_after_group_tag = "__"

# language_order = ['hi', 'ta', 'te', 'kn', 'bn', 'gu', 'pa', 'as', 'or',
#                   'ml', 'mr', 'en', 'th', 'ja', 'th', 'id', 'ms', 'ko', 'bho']


# script_directory = os.path.dirname(os.path.abspath("__file__"))

# if os.name == "nt":
#     iswin = "1"
# else:
#     iswin = "0"

# # script_directory = os.path.join(script_directory, "Zee5_2024")

# ytdlp = os.path.join(script_directory, "binaries",
#                      "yt-dlp") + (".exe" if iswin != "0" else "")
# mp4decrypt = os.path.join(script_directory, "binaries",
#                           "mp4decrypt") + (".exe" if iswin != "0" else "")
# aria2c = os.path.join(script_directory, "binaries",
#                       "aria2c") + (".exe" if iswin != "0" else "")
# wvd_file_path = os.path.join(script_directory, "static",
#                              "google_sdk_google_atv_x86_15.0.0_27cfa318_8162_l3.wvd")

# dl_folder = os.path.join(script_directory, "downloads")
# if not os.path.exists(dl_folder):
#     os.mkdir(folder_path)

# thumb_folder = os.path.join(script_directory, "Thumbnail")
# if not os.path.exists(thumb_folder):
#     os.mkdir(thumb_folder)

# languages_info_file_path = os.path.join(script_directory, "static",
#                                         "languages_info.json")


# if iswin == "0":
#     os.system(f"chmod 777 {ytdlp} {mp4decrypt} {aria2c}")


# ######################################## code starts helper functions 1 ####################################################


# def print_help_message(parser_data_key):
#     if parser_data_key in parser_data:
#         print(colored_text(
#             f"PARSER DATA HELP FOR '{parser_data_key.upper()}' - ", "green"))
#         for item in parser_data[parser_data_key]:
#             short_name = item["short_parsername"]
#             example = item["example"]
#             help_text = item["help"]
#             required = item["required"]
#             default = item["default"]

#             required_str = " (Required)" if required else ""
#             default_str = f" (Default: {default})" if default is not None else ""

#             print(
#                 f"{colored_text(f'  -{short_name},', 'cyan')}{required_str}{default_str}"
#             )
#             print(f"    {help_text}")
#             print(f"    Example: {colored_text(example , 'green')}")
#             print()


# def colored_text(text, color):
#     colors = {
#         "black": "\033[30m",
#         "red": "\033[31m",
#         "green": "\033[32m",
#         "yellow": "\033[33m",
#         "blue": "\033[34m",
#         "magenta": "\033[35m",
#         "cyan": "\033[36m",
#         "white": "\033[37m",
#         "reset": "\033[0m",
#     }
#     if colored_text_config is True:
#         return f"{colors[color]}{text}{colors['reset']}"
#     else:
#         return text


# def custom_sort(audio):
#     # Assign a high index if the language is not in language_order
#     lang_index = language_order.index(
#         audio["lang"]) if audio["lang"] in language_order else len(language_order)
#     return (lang_index, audio["lang"])


# def language_mapping(language_code, return_key=None):
#     with open(languages_info_file_path, "r") as json_file:
#         language_info = json.load(json_file)
#     for code, info in language_info.items():
#         if (
#             code == language_code
#             or info.get("639-1") == language_code
#             or info.get("639-2") == language_code
#             or "en" in info and info["en"][0].lower() == language_code.lower()
#         ):
#             return_value = info.get(return_key)
#             if return_key == "en" and return_value:
#                 return return_value[0]
#             return return_value or info.get("639-1")

#     # If the language_code is not found, return an error message
#     raise Exception(f"Language code '{language_code}' not found.")


# def print_message(first, second, third):
#     print(MESSAGE.format(colored_text(first, "green"), colored_text(
#         second, "blue"), colored_text(third, "cyan")))

# ##################################### helper function 2 ################################################

# def extract_pssh(text):
#     try:
#         pattern = rb"<cenc:pssh>(.*?)</cenc:pssh>"
#         matches = re.findall(pattern, text)
#         if matches:
#             smaller_pssh = min(matches, key=len)
#             return smaller_pssh.strip().decode()
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         print("Error occurred while making the request:", e)
#         return None


# def extract_pssh_ytdlp(url):
#     command = [
#         ytdlp,
#         "--allow-unplayable-formats",
#         "--skip-download",
#         "--dump-pages",
#         url
#     ]

#     try:
#         result = subprocess.run(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,  # Capture the output as text
#             check=True  # Raise an exception if the command fails
#         )

#         return extract_pssh(base64.b64decode(result.stdout.split("\n")[3]))

#     except subprocess.CalledProcessError as e:
#         return None

# def get_pssh(url):
#     try:
#         response = requests.get(
#             url,
#             headers={
#                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
#             }, proxies=proxies
#         )
#         text = response.text
#         # print(text)
#         pattern = r"<cenc:pssh>(.*?)</cenc:pssh>"
#         matches = re.findall(pattern, text)
#         if matches:
#             smaller_pssh = min(matches, key=len)
#             return smaller_pssh.strip()
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         print("Error occurred while making the request:", e)
#         return None


# def find_keys_wvclone_api(mpd, lic_url, custom_headers=None):

#     # pssh = extract_pssh_ytdlp(mpd)
#     pssh = get_pssh(mpd)

#     headers = {
#         'authority': 'wvclone.fly.dev',
#         'accept': 'application/json, text/plain, */*',
#         'accept-language': 'en,en-US;q=0.9,en-IN;q=0.8',
#         'content-type': 'application/json',
#         'origin': 'https://wvclone.fly.dev',
#         'referer': 'https://wvclone.fly.dev/',
#         'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
#     }

#     if custom_headers:

#         formatted_lic_headers = ''
#         for key, value in custom_headers.items():
#             formatted_lic_headers += f'{key} : {value}\n'

#         json_data = {
#             'password': '',
#             'license': lic_url,
#             'headers': formatted_lic_headers.rstrip('\n'),
#             'pssh': pssh,
#             'buildInfo': '',
#             'cache': False,
#         }

#     else:
#         json_data = {
#             'password': '',
#             'license': lic_url,
#             'headers': '',
#             'pssh': pssh,
#             'buildInfo': '',
#             'cache': False,
#         }

#     response = requests.post('https://wvclone.fly.dev/wv',
#                              headers=headers, json=json_data)
#     return extract_keys_from_text(response.text)


# def find_keys(mpd, lic_url, custom_headers=None):
#     pssh = PSSH(get_pssh(mpd))
#     device_path = wvd_file_path
#     license_manager = WidevineLicenseManager(pssh, device_path)
#     keys_data = license_manager.extract_keys(lic_url, custom_headers)

#     return keys_data


# def extract_keys_from_text(data):
#     pattern = r"[a-fA-F0-9]{32}:[a-fA-F0-9]{32}"
#     keys = re.findall(pattern, data)
#     return keys


# def mpd_table(url, init_file_name, ott, keys, lic_url):
#     videoslist, audioslist, subtitlelist, baseurl, pssh = MPD(
#         url, init_file_name, ott, custom_group_tag=GROUP_TAG).parse()

#     table_audio_data = ['- {language} ({languageCode}) [{formatID}] [{audio_info}]'.format(
#         language=language_mapping(audio['lang'], return_key="en"),
#         languageCode=audio['lang'],
#         formatID=audio['id'],
#         audio_info=audio['audio_codec_release_name'] +
#         f" - {audio['bandwidth_release_name']}bps"

#     ) for audio in audioslist]

#     table_videos_list = ['- {resolution} {vcodec} [{formatID}] - {bandwidth}Kbps'.format(
#         resolution="{}x{}".format(video['width'], video['height']),
#         vcodec=video['video_codec_release_name'],
#         formatID=video['id'],
#         bandwidth=int(video['bandwidth']) / 1000
#     ) for video in videoslist]

#     if subtitlelist is not None:
#         table_subs_list = ['- {lang} {url}'.format(
#             lang=subtitle['lang'],
#             url=subtitle['url']
#         ) for subtitle in subtitlelist]

#     else:
#         table_subs_list = None

#     table = ''

#     if table_audio_data:
#         table += 'Audio:\n'
#         table += '\n'.join(table_audio_data) + '\n\n'

#     if table_videos_list:
#         table += 'Video:\n'
#         table += '\n'.join(table_videos_list) + '\n\n'

#     if table_subs_list:
#         table += 'Subtitle:\n'
#         table += '\n'.join(table_subs_list) + '\n\n'

#     if baseurl:
#         table += 'BASE URL:\n'
#         table += baseurl + '\n\n'

#     if pssh:
#         table += 'PSSH:\n'
#         table += pssh + '\n\n'

#     if keys:
#         table += 'KEYS:\n'
#         table += "\n".join(keys) + "\n\n" if isinstance(keys,
#                                                         list) else keys + '\n\n'

#     if lic_url:
#         table += 'LICENSE URL:\n'
#         table += lic_url + '\n\n'

#     return table

# ################################ class WidevineLicenseManager ##############################################

# class WidevineLicenseManager:
#     def __init__(self, pssh, device_path):
#         self.pssh = pssh
#         self.device_path = device_path
#         self.device = None
#         self.cdm = None
#         self.session_id = None

#     def initialize(self):
#         self.device = Device.load(self.device_path)
#         self.cdm = Cdm.from_device(self.device)

#     def open_session(self):
#         self.session_id = self.cdm.open()

#     def get_license_challenge(self):
#         challenge = self.cdm.get_license_challenge(self.session_id, self.pssh)
#         return challenge

#     def parse_license(self, license_data):
#         self.cdm.parse_license(self.session_id, license_data)

#     def get_keys_data(self):
#         keys_data = ""
#         for key in self.cdm.get_keys(self.session_id):
#             if key.type != "SIGNING":
#                 keys_data += f"{key.kid.hex}:{key.key.hex()}\n"
#         return keys_data.strip().split()

#     def close_session(self):
#         self.cdm.close(self.session_id)

#     def extract_keys(self, license_url, custom_headers=None):
#         self.initialize()
#         self.open_session()

#         challenge = self.get_license_challenge()

#         license_response = requests.post(
#             license_url, data=challenge, headers=custom_headers)
#         license_response.raise_for_status()

#         self.parse_license(license_response.content)

#         keys_data = self.get_keys_data()

#         self.close_session()

#         return keys_data

# ################################ class FilenameGenerator ##############################################

# class FilenameGenerator:
#     def __init__(self, audioslist, videoslist, subtitleslist, init_file_name, ott, custom_group_tag, resolution, language_order):
#         self.audioslist = audioslist
#         self.videoslist = videoslist
#         self.subtitleslist = subtitleslist
#         self.init_file_name = init_file_name
#         self.ott = ott
#         self.custom_group_tag = custom_group_tag
#         self.resolution = resolution
#         self.language_order = language_order

#     def get_subtitle_write_data(self):

#         if self.subtitleslist is not None:
#             if len(self.subtitleslist) == 1:
#                 if filename_format == "p2p":
#                     subs_write = ".ESub"
#                 else:
#                     subs_write = "ESub"
#             else:
#                 if filename_format == "p2p":
#                     subs_write = ".MSubs"
#                 else:
#                     subs_write = "MSubs"
#         else:
#             subs_write = ""

#         return subs_write

#     def generate_filename(self):
#         subtitle_write_data = self.get_subtitle_write_data()
#         unique_audio_configs = self._group_unique_audio_configs()
#         audio_groups = self._group_languages_by_audio_config(
#             unique_audio_configs)

#         filename_parts = self._generate_filename_parts(audio_groups)
#         video_codec = self.videoslist['video_codec_release_name']
#         video_resolution = f"{self.videoslist['height']}p"

#         video_quality = (
#             "." + self.videoslist["quality"] if "quality" in self.videoslist and self.videoslist["quality"] != "" else "")
#         video_codec_v2 = "x264" if video_codec == "H264" else (
#             "x265" + (" 10bit" if "10bit" in video_codec else "") if "H265" or "HEVC" in video_codec else "")

#         if filename_format == "p2p":
#             filename = f"{self.init_file_name}.{video_resolution}{video_quality}.{self.ott}.WEB-DL.{'-'.join(filename_parts)}.{video_codec}{subtitle_write_data}-{self.custom_group_tag}.mkv"
#             filename.replace(" ", ".").replace(
#                 "/", "").replace(":", "").replace(",", "")
#         else:
#             filename = f"{self.init_file_name} {video_resolution}{video_quality.replace('.' , ' ')} {self.ott} WEB-DL {video_codec_v2} [{' - '.join(filename_parts)}] {subtitle_write_data}{underscore_before_after_group_tag}{self.custom_group_tag}{underscore_before_after_group_tag}.mkv"
#             filename.replace("/", "").replace(":", "").replace(",", "")

#         return filename

#     def _group_unique_audio_configs(self):
#         unique_audio_configs = {}
#         for audio in self.audioslist:
#             config = (audio['audio_codec_release_name'].rsplit(
#                 '.', 1)[0], audio['bandwidth_release_name'])
#             if config not in unique_audio_configs:
#                 unique_audio_configs[config] = []
#             unique_audio_configs[config].append(audio)
#         return unique_audio_configs

#     def _group_languages_by_audio_config(self, unique_audio_configs):
#         audio_groups = {}
#         for config, audio_data in unique_audio_configs.items():
#             langs = sorted(
#                 set([audio['lang'] for audio in audio_data]), key=self._custom_sort_key)
#             # lang_concatenated = "-".join(langs)
#             lang_concatenated = "-".join(langs)
#             audio_groups[lang_concatenated] = audio_data
#         return audio_groups

#     def _custom_sort_key(self, lang):
#         return self.language_order.index(lang)

#     def _generate_filename_parts(self, audio_groups):
#         filename_parts = []
#         for lang_group, audio_data in audio_groups.items():
#             audio_codec = audio_data[0]['audio_codec_release_name']
#             audio_bandwidths = audio_data[0]['bandwidth_release_name']

#             lang_group = [language_mapping(
#                 lang.strip(), "639-2").upper() for lang in lang_group.split("-")]
#             if filename_format == "p2p":
#                 lang_group = "-".join(lang_group)
#             else:
#                 lang_group = " + ".join(lang_group)
#             if filename_format == "p2p":
#                 filename_parts.append(
#                     f"{lang_group}.{audio_codec}.{audio_bandwidths}")
#             else:
#                 filename_parts.append(
#                     f"{lang_group} ({audio_codec} - {audio_bandwidths})")
#         return filename_parts


# def get_readable_time(seconds: int) -> str:
#     result = ''
#     (days, remainder) = divmod(seconds, 86400)
#     days = int(days)
#     if days != 0:
#         result += f'{days}d'
#     (hours, remainder) = divmod(remainder, 3600)
#     hours = int(hours)
#     if hours != 0:
#         result += f'{hours}h'
#     (minutes, seconds) = divmod(remainder, 60)
#     minutes = int(minutes)
#     if minutes != 0:
#         result += f'{minutes}m'
#     seconds = int(seconds)
#     result += f'{seconds}s'
#     return result


# def get_zee5_id(url):
#     id_pattern = r'/details/[^/]+/([^/]+)/?$'
#     match = re.search(id_pattern, url)
#     if match:
#         return match.group(1).split("?")[0]
#     else:
#         return None


# def save_file(data, file_name):
#     json_object = json.dumps(data, indent=4)

#     dest = f"{file_name}"

#     # Writing to extracted_keys.json
#     with open(dest, "w+") as outfile:
#         outfile.write(json_object)


# ############################################### class MPD #########################################

# class MPD():
#     def __init__(self, url, init_file_name, ott, custom_group_tag):
#         self.url = url
#         if filename_format == "p2p":
#             self.init_file_name = init_file_name.replace(" ", ".")
#         else:
#             self.init_file_name = self.format_movie_title(init_file_name)
#         self.ott = ott
#         self.custom_group_tag = custom_group_tag

#         self.AUDIO_CODEC_MAP = {
#             "mp4a.40.2": "AAC", "ac-3": "DD", "ec-3": "DD+"}
#         self.CHANNEL_MAP = {"F801": "5.1", "6.0": "5.1", "6": "5.1",
#                             "2.0": "2.0", "2": "2.0", "1.0": "2.0", "1": "2.0"}
#         self.AUDIO_CODEC_v2_MAP = {"aac": "mp4a.40.2", "dd": "ac-3", "dd+": "ec-3", "dolby": "ac-3",
#                                    "dolbydigital+": "ec-3", "ddplus": "ec-3", "mp4a.40.2": "mp4a.40.2", "ac-3": "ac-3", "ec-3": "ec-3"}

#     def format_movie_title(self, title):
#         match = re.search(r'\b\d{4}\b$', title)

#         if match:
#             release_year = match.group()
#             formatted_title = re.sub(
#                 fr'\b{release_year}\b', f'({release_year})', title)
#             return formatted_title
#         else:
#             return title

#     def find_atmos(self, json_data):
#         json_text = json.dumps(json_data)
#         pattern = r'\bJOC\b'
#         matches = re.findall(pattern, json_text, re.IGNORECASE)
#         return matches

#     def extract_pssh(self, text):
#         pattern = r"<cenc:pssh>(.*?)</cenc:pssh>"
#         matches = re.findall(pattern, text)
#         if matches:
#             smaller_pssh = min(matches, key=len)
#             return smaller_pssh.strip()
#         else:
#             return None

#     def round_bitrate(self, bitrate):
#         bits = [640, 448, 384, 192, 128, 96, 64, 32]
#         nearest_bitrate = min(bits, key=lambda x: abs(x - bitrate))
#         return nearest_bitrate

#     def video_codec_mapping(self, video_codec):
#         codec_mapping = {
#             "hvc": "HEVC",
#             "hev1.2": "HEVC.10bit",
#             "hev1.1": "HEVC",
#             "hevc": "HEVC",
#             "avc": "H264"
#             # Add more mappings as needed
#         }
#         for substring, title in codec_mapping.items():
#             if substring in video_codec.lower():
#                 return title

#         return "H264"

#     def parse(self, und_lang=None):
#         audioslist, videoslist, subtitlelist = list(), list(), list()
#         text = requests.get(self.url, proxies=proxies, headers={
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#             'x-playback-session-id': "9c7631d21edd4a65a92b2b641c8a13a2-1634808345996"
#         }).text
#         # text = open(self.file_path, 'r').read()
#         # print("persed text is ",text)
#         mpd = json.loads(json.dumps(xmltodict.parse(text)))
#         self.baseurl = re.sub(r'[^\/]*$', '', self.url)
#         periods = mpd['MPD']['Period']
        
#         if not isinstance(periods, list): # cameTrue
#             periods = [periods]
#             # print(periods)

#         global periodsNumber
#         periodsNumber = len(periods)

#         adaptationSet = periods[0]['AdaptationSet']

#         for ad in adaptationSet:
#             if not isinstance(ad['Representation'], list):
#                 ad['Representation'] = [ad['Representation']]
#             for item in ad['Representation']:
#                 if (item.get('@mimeType', False) or ad.get('@mimeType')) == 'audio/mp4':

#                     is_atmos = True if len(self.find_atmos(ad)) >= 1 else False
#                     lang = und_lang if und_lang else ad.get(
#                         "@lang", False) or und_lang
#                     codec = item.get('@codecs', '') if item.get('@codecs',
#                                                                 '') != "" else ad.get("@codecs", "mp4a.40.2")
#                     channel = ad.get('AudioChannelConfiguration', {}).get(
#                         '@value', "2.0")
#                     bandwidth = int(item.get("@bandwidth", "126000"))

#                     auddict = {
#                         # 'lang': ad.get('@lang', False) or 'und',
#                         'lang': language_mapping(lang),
#                         'id': item["@id"].replace("/", "_"),
#                         "audio_codec_release_name": "{}{}{}".format(self.AUDIO_CODEC_MAP.get(
#                             codec), self.CHANNEL_MAP.get(channel), ((".ATMOS" if filename_format == "p2p" else " ATMOS") if is_atmos == True else "")),
#                         "bandwidth_release_name": str(self.round_bitrate(int(bandwidth / 1000)))
#                         + (p2p_audio_bitrate if filename_format ==
#                            "p2p" else non_p2p_audio_bitrate),
#                         "channels": self.CHANNEL_MAP.get(channel),
#                         'codec': codec,
#                         'bandwidth': item.get('@bandwidth', '125'),
#                         'label': language_mapping(lang, return_key="en")
#                     }
#                     audioslist.append(auddict)

#         for ad in adaptationSet:
#             if not isinstance(ad['Representation'], list):
#                 ad['Representation'] = [ad['Representation']]
#             for item in ad['Representation']:
#                 if (item.get('@mimeType', False) or ad.get('@mimeType')) == 'video/mp4':
#                     pssh = self.extract_pssh(text)
#                     try:
#                         viddict = {
#                             'width': item['@width'],
#                             'height': item['@height'],
#                             'id': item['@id'],
#                             'codec': item.get('@codecs', 'h264'),
#                             'bandwidth': item.get('@bandwidth', '125'),
#                             "video_codec_release_name": self.video_codec_mapping(
#                                 item.get("@codecs", "avc")
#                             ),
#                         }
#                         videoslist.append(viddict)
#                     except Exception:
#                         continue

#         for ad in adaptationSet:
#             if not isinstance(ad['Representation'], list):
#                 ad['Representation'] = [ad['Representation']]
#             for item in ad['Representation']:
#                 if (item.get('@mimeType', False) or ad.get('@mimeType')) == 'text/vtt':
#                     subdict = {
#                         'lang': ad.get('@lang', 'eng'),
#                         'url': item.get('BaseURL'),
#                         'baseURL': self.baseurl
#                     }
#                     subtitlelist.append(subdict)

#         if len(subtitlelist) == 0:
#             subtitlelist = None

#         self.videoslist = videoslist
#         self.audioslist = audioslist
#         self.subtitlelist = subtitlelist
#         self.pssh = pssh
        
#         # print("video_data is  under mpd 1 💚" ,self.videoslist) # IMP we can produce button under this
#         # print("audio_data is 💚" ,self.audioslist)
#         # print("subtitles_data is 💚" ,self.subtitlelist)

#         return videoslist, audioslist, subtitlelist, self.baseurl, pssh

#     def get_highest_audio_codec(self, audioslist):
#         codec_order = ["ec-3", "ac-3", "mp4a.40.2"]
#         filtered_audios = []

#         for codec in codec_order:
#             for audio in audioslist:
#                 if codec in audio["codec"]:
#                     # Append matching audio to the filtered list
#                     filtered_audios.append(audio)

#         if filtered_audios:
#             return filtered_audios  # Return the filtered list if any matches were found
#         else:
#             return audioslist

#     def filter_audio_quality(self, audioslist, audio_quality):
#         lang_groups = {}  # Dictionary to group audio items by lang

#         for audio in audioslist:
#             lang = audio["lang"]
#             if lang not in lang_groups:
#                 lang_groups[lang] = []
#             lang_groups[lang].append(audio)

#         filtered_audios = []

#         for lang, audio_group in lang_groups.items():
#             if audio_quality == "HQ":
#                 selected_audio = max(
#                     audio_group, key=lambda x: int(x["bandwidth"]))
#             elif audio_quality == "MQ":
#                 selected_audio = self.find_mid_value(audioslist, 'bandwidth')
#             elif audio_quality == "LQ":
#                 selected_audio = min(
#                     audio_group, key=lambda x: int(x["bandwidth"]))
#             else:
#                 # Default to "HQ" if no audio_quality is specified
#                 selected_audio = max(
#                     audio_group, key=lambda x: int(x["bandwidth"]))

#             filtered_audios.append(selected_audio)

#         return filtered_audios

#     def mid(self, iterable, key=None):
#         if key is None:
#             def key(x): return x
#         sorted_iterable = sorted(iterable, key=key)
#         length = len(sorted_iterable)
#         if length == 0:
#             raise ValueError("mid() arg is an empty sequence")
#         middle_index = length // 2
#         return sorted_iterable[middle_index]

#     def find_mid_value(self, data_list, key):
#         sorted_data = sorted(data_list, key=lambda x: int(x[key]))
#         middle_index = len(sorted_data) // 2
#         return sorted_data[middle_index]

#     def refine(self, video_resolution=None, video_quality=None, audio_languages=None, audio_codec=None, audio_quality="HQ", und_lang=None):

#         self.parse(und_lang=und_lang)

#         # VIDEO RESOLUTION
#         if video_resolution:

#             filtered_video_data = [
#                 video
#                 for video in self.videoslist
#                 if int(video["height"]) == int(video_resolution.replace("p", ""))
#             ]

#             if filtered_video_data:
#                 videoslist = filtered_video_data
#             else:
#                 # No videos matched the specified resolution; use the highest resolution
#                 videoslist = [
#                     max(self.videoslist, key=lambda x: int(x["height"]))]
#         else:
#             # Use the video with the highest resolution by default
#             videoslist = [max(self.videoslist, key=lambda x: int(x["height"]))]

#         # VIDEO QUALITY
#         if video_quality:
#             if video_quality == "HQ":
#                 selected_video = max(
#                     videoslist, key=lambda x: int(x["bandwidth"]))
#                 selected_video["quality"] = "HQ" if len(videoslist) > 1 else ""
#             elif video_quality == "LQ":
#                 selected_video = min(
#                     videoslist, key=lambda x: int(x["bandwidth"]))
#                 selected_video["quality"] = "LQ" if len(videoslist) > 1 else ""
#             else:
#                 selected_video = max(
#                     videoslist, key=lambda x: int(x["bandwidth"]))
#                 selected_video["quality"] = "HQ" if len(videoslist) > 1 else ""
#         else:
#             selected_video = max(videoslist, key=lambda x: int(x["bandwidth"]))
#             selected_video["quality"] = "HQ" if len(videoslist) > 1 else ""
#         videoslist = selected_video

#         # DEFAULT AUDIO SORT

#         self.audioslist.sort(key=custom_sort)
#         audioslist = self.audioslist

#         # AUDIO LANGUAGE

#         if audio_languages:
#             requested_languages = audio_languages.split("-")
#             filtered_audio_data = [
#                 audio for audio in audioslist if audio["lang"] in requested_languages
#             ]

#             if filtered_audio_data:
#                 audioslist = filtered_audio_data
#                 # print(audioslist)
#         # print(self.AUDIO_CODEC_v2_MAP.get(audio_codec))

#         # AUDIO CODEC
#         if audio_codec:
#             codec_map = self.AUDIO_CODEC_v2_MAP.get(audio_codec)
#             # print(audio_codec)
#             if codec_map:
#                 filtered_audio_data = [audio for audio in audioslist if codec_map in audio["codec"]]
                
#             else:
#                 filtered_audio_data = self.get_highest_audio_codec(audioslist)
#             # print(filtered_audio_data)


#         # if audio_codec:
#         #     filtered_audio_data = [audio for audio in audioslist if self.AUDIO_CODEC_v2_MAP.get(
#         #         audio_codec) in audio["codec"]] or self.get_highest_audio_codec(audioslist)

#         #     audioslist = filtered_audio_data

#         else:

#             # Group by language and find the one with the highest bandwidth for each language
#             unique_lang_audios = {}
#             for audio in audioslist:
#                 lang = audio["lang"]
#                 if lang not in unique_lang_audios or int(audio["bandwidth"]) > int(
#                     unique_lang_audios[lang]["bandwidth"]
#                 ):
#                     unique_lang_audios[lang] = audio

#             audioslist = list(unique_lang_audios.values())

#         # AUDIO QUALITY
#         if audio_quality:
#             audioslist = self.filter_audio_quality(audioslist, audio_quality)

#         # Filename

#         filename_generator = FilenameGenerator(audioslist, videoslist, self.subtitlelist, self.init_file_name,
#                                                self.ott, self.custom_group_tag, videoslist["height"], language_order)
#         filename = filename_generator.generate_filename()
        
#         # print("videoslist is under mpd 2 ❤️" ,videoslist)
#         # print("audioslist is ❤️" ,audioslist)
#         # print("subtitlelist is ❤️" ,self.subtitlelist)
#         # print("pssh is ❤️" ,self.pssh)
#         # print("baseurl is ❤️" ,self.baseurl)
#         # print("filename is ❤️" ,filename)
#         return videoslist, audioslist, self.subtitlelist, self.pssh, self.baseurl, filename

#     # def refine(self, selected_Videoqulity, und_lang=None):

#     #     self.parse(und_lang=und_lang)

#     #     if selected_Videoqulity: ### getting video resolution (height)
#     #         selected_Videoqulity = selected_Videoqulity
            
            
#     #     else:
#     #         # Use the video with the highest resolution by default
#     #         videoslist = [max(self.videoslist, key=lambda x: int(x["height"]))]

# ####################################### class Processor #######################################

# class Processor():
#     def __init__(self, link, key, init_file_name=None, ott=None,  baseurl=None, pssh=None, filename=None, subtitle_data=None, videos_id=None, audios_id=None):

#         self.link = link
#         self.key = key
#         self.init_file_name = init_file_name
#         self.ott = ott
#         self.baseurl = baseurl
#         self.pssh = pssh
#         self.final_file_name = filename
#         self.subtitles_data = subtitle_data
#         self.video_data = videos_id
#         self.audio_data = [json.loads(audios) for audios in audios_id]


#         self.custom_group_tag = GROUP_TAG
#         self.process_start = time.time()
#         self.end_code = str(time.time()).replace(".", "")        

#         # print("video_data is 💙" ,self.video_data)
#         print(" recevied video_data is 💙" ,self.video_data)
#         print("recevied audios_id is 💙" ,self.audio_data)

#     def download_audio_stream(self, stream_format, filename):
#         dest = os.path.join(dl_folder, f"{filename}.m4a")
#         # print(f"dl..ing audio by 0️⃣{stream_format}")
#         try:
#             cmd = [
#                 f"{ytdlp}",
#             ]

#             if proxy_url and proxy_url.strip():  # Check if proxy_url is not empty or None
#                 cmd.extend(["--proxy", proxy_url])

#             cmd.extend(["--allow-unplayable-formats",
#                         "-f",
#                         str(stream_format),
#                         f"{self.link}",
#                         "-o",
#                         dest,
#                         "--external-downloader",
#                         f"{aria2c}",
#                         ])
#             dl_process = dl_process = subprocess.Popen(
#                 cmd, stdout=subprocess.DEVNULL)
#             dl_process.wait()
#         except Exception as e:
#             raise Exception(f"Error Running YT-DLP Command {e}")

#     def mpd_download(self):
#         threads = []
#         # if len(audio_data) == 1:
#         for i, audio_info in enumerate(self.audio_data): ### here downloading all avalable audio stream by using for loop  ==["id"]
#             print("in for loop",audio_info)
#             stream_format = audio_info["id"]
#             filename = f"enc_{stream_format}_{self.end_code}"
#             thread = threading.Thread(target=self.download_audio_stream, args=(stream_format, filename))
#             threads.append(thread)
#             thread.start()
#             print_message("DOWNLOADING", "⬇️", f"AUDIO STREAM {i + 1} of {len(self.audio_data)}")
#         # else:
#             # print("stream qulity is pass from bot here")

#         try:
#             video_format = self.video_data
#             dest = os.path.join(
#                 dl_folder, f"enc_{video_format}_{self.end_code}.mp4")

#             video_cmd = [
#                 f"{ytdlp}",
#             ]
#             if proxy_url and proxy_url.strip():  # Check if proxy_url is not empty or None
#                 video_cmd.extend(["--proxy", proxy_url])
#             print(f"dl..ing video by 0️⃣{video_format}")
#             video_cmd.extend([
#                 "--allow-unplayable-formats",
#                 "-f",
#                 str(video_format),
#                 f"{self.link}",
#                 "-o",
#                 dest,
#                 "--external-downloader",
#                 f"{aria2c}",
#             ])
#             print_message("DOWNLOADING", "⬇️", "VIDEO STREAM")
#             subprocess.call(video_cmd, stdout=subprocess.DEVNULL)
#         except Exception as e:
#             raise Exception(f"Error Downloading Video File {e}")

#         for thread in threads:
#             thread.join()

#         return self.end_code

#     def decrypt(self):
#         print_message("DECRYPTING", "⬇️", "VIDEO + AUDIO")

#         try:
#             for audio_info in self.audio_data:
#                 stream_format = audio_info["id"]
#                 enc_dl_audio_file_name = os.path.join(
#                     dl_folder, f"enc_{stream_format}_{self.end_code}.m4a")
#                 dec_out_audio_file_name = os.path.join(
#                     dl_folder, f"dec_{stream_format}_{self.end_code}.m4a")

#                 if isinstance(self.key, list):
#                     cmd_audio_decrypt = [
#                         f"{mp4decrypt}"]

#                     for k in self.key:
#                         cmd_audio_decrypt.append(str("--key"))
#                         cmd_audio_decrypt.append(str(k))

#                     cmd_audio_decrypt.append(str(enc_dl_audio_file_name)),
#                     cmd_audio_decrypt.append(str(dec_out_audio_file_name))

#                 else:

#                     cmd_audio_decrypt = [
#                         f"{mp4decrypt}",
#                         "--key",
#                         str(self.key),
#                         str(enc_dl_audio_file_name),
#                         str(dec_out_audio_file_name)

#                     ]
#                 subprocess.run(cmd_audio_decrypt, stdout=subprocess.DEVNULL)
#                 try:
#                     os.remove(enc_dl_audio_file_name)
#                 except:
#                     pass

#             video_format = self.video_data
#             enc_dl_video_file_name = os.path.join(
#                 dl_folder, f"enc_{video_format}_{self.end_code}.mp4")
#             dec_out_video_file_name = os.path.join(
#                 dl_folder, f"dec_{video_format}_{self.end_code}.mp4")

#             cmd_video_decrypt = [f"{mp4decrypt}"]
#             if isinstance(self.key, list):
#                 cmd_video_decrypt = [
#                     f"{mp4decrypt}"]

#                 for k in self.key:
#                     cmd_video_decrypt.append(str("--key"))
#                     cmd_video_decrypt.append(str(k))

#                 cmd_video_decrypt.append(str(enc_dl_video_file_name)),
#                 cmd_video_decrypt.append(str(dec_out_video_file_name))

#             else:
#                 cmd_video_decrypt = [
#                     f"{mp4decrypt}",
#                     "--key",
#                     str(self.key),
#                     str(enc_dl_video_file_name),
#                     str(dec_out_video_file_name)

#                 ]
#             try:
#                 subprocess.run(cmd_video_decrypt, stdout=subprocess.DEVNULL)
#             except Exception as e:
#                 raise Exception(str(e))

#             try:
#                 os.remove(enc_dl_video_file_name)
#             except:
#                 pass

#         except Exception as e:
#             raise Exception("Error During Decryption")

#         return self.end_code

#     def dl_subs(self):

#         if self.subtitles_data is not None:
#             for sub in self.subtitles_data:
#                 subs_lang = sub["lang"]
#                 dest = os.path.join(
#                     dl_folder, f"subtitle_{subs_lang}_{self.end_code}.vtt")
#                 subs_url = sub['baseURL'] + sub["url"]
#                 subs_dl_cmd = [
#                     f"{ytdlp}",
#                 ]

#                 if proxy_url and proxy_url.strip():  # Check if proxy_url is not empty or None
#                     subs_dl_cmd.extend(["--proxy", proxy_url])

#                 subs_dl_cmd.extend([
#                     f"{subs_url}",
#                     "-o",
#                     dest,
#                     "--external-downloader",
#                     f"{aria2c}"
#                 ])
#                 print_message("DOWNLOADING", "⬇️",
#                               f"SUBTITLE")
#                 print_message("", "URL 🔗",
#                               subs_url)

#                 subprocess.call(subs_dl_cmd, stdout=subprocess.DEVNULL)

#     def mux_video(self, startTime=None, endTime=None):

#         file_prefix = "enc" if self.key is None else "dec"

#         dec_out_video_file_name = os.path.join(
#             dl_folder, f"{file_prefix}_{self.video_data}_{self.end_code}.mp4")
#         audio_files = [
#             os.path.join(
#                 dl_folder, f"{file_prefix}_{audio_info['id']}_{self.end_code}.m4a")
#             for audio_info in self.audio_data
#         ]

#         ffmpeg_opts = ["ffmpeg", "-y", "-i", dec_out_video_file_name]

#         for audio_file, audio_info in zip(audio_files, self.audio_data):
#             lang = audio_info["lang"]
#             ffmpeg_opts.extend(["-i", audio_file])

#         if self.subtitles_data is not None:

#             subs_file = [
#                 os.path.join(
#                     dl_folder, f"subtitle_{sub['lang']}_{self.end_code}.vtt")
#                 for sub in self.subtitles_data
#             ]

#             for individual_subs_file in subs_file:
#                 ffmpeg_opts.extend(["-i", individual_subs_file])

#         if startTime is not None and endTime is not None:
#             ffmpeg_opts.extend(["-ss", f"{startTime}"])
#             ffmpeg_opts.extend(["-to", f"{endTime}"])

#         ffmpeg_opts.extend(["-map", "0:v:0"])

#         for i in range(len(self.audio_data)):
#             ffmpeg_opts.extend(["-map", f"{i+1}:a:0"])

#         if self.subtitles_data is not None:
#             for i in range(len(self.subtitles_data)):
#                 ffmpeg_opts.extend(["-map", f"{len(self.audio_data)+1}:s:0"])

#         ffmpeg_opts.extend(
#             ["-metadata", f"encoded_by={self.custom_group_tag}"])
#         ffmpeg_opts.extend(["-metadata:s:a", f"title={self.custom_group_tag}"])
#         ffmpeg_opts.extend(["-metadata:s:v", f"title={self.custom_group_tag}"])

#         if self.subtitles_data is not None:
#             ffmpeg_opts.extend(
#                 ["-metadata:s:s", f"title={self.custom_group_tag}"])

#         for i, audio_info in enumerate(self.audio_data):
#             lang = audio_info["lang"]
#             ffmpeg_opts.extend(
#                 ["-metadata:s:a:{0}".format(i), f"language={lang}"])

#         if self.subtitles_data is not None:
#             for i in range(len(self.subtitles_data)):
#                 ffmpeg_opts.extend(
#                     ["-metadata:s:s:{0}".format(i), f"language={self.subtitles_data[i]['lang']}"])

#         out_name = f"{self.end_code}.mkv"
#         out_file_name = self.final_file_name
#         ffmpeg_opts.extend(["-c", "copy", out_name])

#         try:
#             subprocess.check_call(ffmpeg_opts, stdout=subprocess.DEVNULL)
#         except subprocess.CalledProcessError as e:
#             raise Exception(f"FFMPEG Error: {e}")

#         try:
#             os.rename(out_name, out_file_name)
#         except OSError as e:
#             raise Exception(f"OSError: {e}",)

#         for audio_file in audio_files:
#             try:
#                 os.remove(audio_file)
#             except OSError as e:
#                 print(f"OSError: {e}")
#                 pass
#         try:
#             os.remove(dec_out_video_file_name)
#         except OSError as e:
#             print(f"OSError: {e}")
#             pass

#         return out_file_name

#     def start_process(self, startTime=None, endTime=None):

#         task_start_time = time.time()
#         print(
#             '[+] Downloading {}'.format(colored_text(self.final_file_name, "blue")))
#         self.mpd_download()

#         self.dl_subs()

#         if self.key is not None:
#             self.decrypt()

#         print(
#             '[+] Muxing {}'.format(colored_text(self.final_file_name, "blue")))

#         out_file_name = self.mux_video(startTime, endTime)

#         print(colored_text("[+] TASK COMPLTED IN", "cyan"),
#               get_readable_time(time.time() - task_start_time))
#         return out_file_name


# ############################################## class ZEEAPI #########################################
# class ZEE5API:
#     def __init__(self, hevc=True):

#         # url= "https://www.zee5.com/tv-shows/details/seetharaama/0-6-4z5359283/seetha-confirms-her-doubts-about-sihis-parents/0-1-6z5633476"
#         # id_pattern = r'/details/[^/]+/([^/]+)/$'
#         # match = re.search(id_pattern, url)Processor
#         # if match:
#         #     self.seriesID = match.group(1).split("?")[0]
#         # else:
#         #     self.seriesID = None

#         # print(self.seriesID)
#         self.custom_group_tag = GROUP_TAG

#         self.hevc = hevc
#         self.x_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDI0LTEwLTEyVDE1OjQ5OjU1Ljg1NFoiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTcyODc0ODE5NX0.3hDKAwz_YJzuO82AQ_X_8XzesWuL1Z66YbeBbgRXRNU"

#         self.authorization = "eyJraWQiOiJkZjViZjBjOC02YTAxLTQ0MWEtOGY2MS0yMDllMjE2MGU4MTUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJDQzEzQjQ4RC00N0VCLTQxQTktODUzNS1BMTVFRkZCMDg3MDAiLCJkZXZpY2VfaWQiOiJmYTk4ZDJiYi0zZTI0LTRhYTItOTc0Zi0zMjc2Y2E4ZDk4MTYiLCJhbXIiOlsiZGVsZWdhdGlvbiJdLCJpc3MiOiJodHRwczovL3VzZXJhcGkuemVlNS5jb20iLCJ2ZXJzaW9uIjo4LCJjbGllbnRfaWQiOiJyZWZyZXNoX3Rva2VuIiwiYXVkIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIiwiZ2FtZS1wbGF5Il0sInVzZXJfdHlwZSI6IlJlZ2lzdGVyZWQiLCJuYmYiOjE3Mjg3NTc4NzAsInVzZXJfaWQiOiJjYzEzYjQ4ZC00N2ViLTQxYTktODUzNS1hMTVlZmZiMDg3MDAiLCJzY29wZSI6WyJ1c2VyYXBpIiwic3Vic2NyaXB0aW9uYXBpIiwicHJvZmlsZWFwaSJdLCJzZXNzaW9uX3R5cGUiOiJHRU5FUkFMIiwiZXhwIjoxNzI5MzYyNjcwLCJpYXQiOjE3Mjg3NTc4NzAsImp0aSI6IjNlMDYzMmJjLTMyZDItNDk0Yi05MGRlLTlkNzYwMDM0YjViMSJ9.VluwNKnwcUa6d8UypFz9bxKMfLcOpuhVGDmsbVdMUkqrHPRXUKdVY_ZjkfwbnIxQbL5vYGVbEumed_uxJFejgNh_lVntoCW4oz0HXVXxBs-KhULO3RuEw4na_SJLMIq9-IDQLYXPVvSIsyd6-zgO074drbXRCYAgzonxcwlprEUxWYOKGcnUAb91UH01dFQLE-PVZwgUMqyJt8kS1IOduLXu620CQZ0YTbPQ8p-V5RLhYamQ7EQ7OZXVstQ-iYYlUNeFcLKalO5EKpTkAn5bAPdIRnf4zec3GJJnAQFw5o4jB5FOh-Ko5ejxsiom4DfYCzhqip2ziXZ-YNXskL9zkg"

#         self.x_dd_token = "eyJzY2hlbWFfdmVyc2lvbiI6IjEiLCJvc19uYW1lIjoiTi9BIiwib3NfdmVyc2lvbiI6Ik4vQSIsInBsYXRmb3JtX25hbWUiOiJDaHJvbWUiLCJwbGF0Zm9ybV92ZXJzaW9uIjoiMTA0IiwiZGV2aWNlX25hbWUiOiIiLCJhcHBfbmFtZSI6IldlYiIsImFwcF92ZXJzaW9uIjoiMi41Mi4zMSIsInBsYXllcl9jYXBhYmlsaXRpZXMiOnsiYXVkaW9fY2hhbm5lbCI6WyJTVEVSRU8iXSwidmlkZW9fY29kZWMiOlsiSDI2NCJdLCJjb250YWluZXIiOlsiTVA0IiwiVFMiXSwicGFja2FnZSI6WyJEQVNIIiwiSExTIl0sInJlc29sdXRpb24iOlsiMjQwcCIsIlNEIiwiSEQiLCJGSEQiXSwiZHluYW1pY19yYW5nZSI6WyJTRFIiXX0sInNlY3VyaXR5X2NhcGFiaWxpdGllcyI6eyJlbmNyeXB0aW9uIjpbIldJREVWSU5FX0FFU19DVFIiXSwid2lkZXZpbmVfc2VjdXJpdHlfbGV2ZWwiOlsiTDMiXSwiaGRjcF92ZXJzaW9uIjpbIkhEQ1BfVjEiLCJIRENQX1YyIiwiSERDUF9WMl8xIiwiSERDUF9WMl8yIl19fQ==ott"

#         self.json_data = {
#             'x-access-token': self.x_access_token,
#             'Authorization': 'bearer {}'.format(self.authorization),
#             'x-dd-token': self.x_dd_token,
#         }

#         self.headers = {
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
#         }

#         self.headers2 = {
#             'authority': 'gwapi.zee5.com',
#             'accept': '*/*',
#             'accept-language': 'en,en-US;q=0.9,en-IN;q=0.8',
#             'origin': 'https://www.zee5.com',
#             'referer': 'https://www.zee5.com/',
#             'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-site',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
#             'x-access-token': self.x_access_token,
#         }

#     # def fetch_episodes_data(self, seasonIndex=1):

#     #     # seriesID = self.seriesID
#     #     seriesID = "0-1-6z5633475"

#     #     episodes_data = []

#     #     page_url = f"https://gwapi.zee5.com/content/player/{seriesID}?user_type=register&limit=25&translation=en&country=IN&languages=undefined"
#     #     # page_url = "https://gwapi.zee5.com/content/tvshow/?season_id=0-2-5z5359284&type=episode&translation=en&country=IN&asset_subtype=tvshow&limit=10&page=0"
#     #     response = requests.get(page_url, headers=self.headers2)
#     #     # if response.get("error_msg") == "Token Expired":
#     #     #     raise("ZEE5 TOKEN EXPIRED")
#     #     page_data = json.loads(response.text)
#     #     # print(page_data)
#     #     if 'items' in page_data:
#     #         # print(page_data["items"][0]["image_url"])

#     #         episode_info = {
#     #                     'showTitle': page_data["items"][0]["title"],
#     #                     'contentID': page_data["items"][0]["id"],
#     #                     'seasonNumber': page_data["items"][0]["season_details"]["index"],
#     #                     'episodeNumber': page_data["items"][0]["episode_number"],
#     #                     'episodeTitle': page_data["items"][0]["original_title"],
#     #                     'episodeDesc': page_data["items"][0]["description"],
#     #                     'thumb': page_data["items"][0]["image_url"],
#     #                 }
#     #         episodes_data.append(episode_info)
#     #     # Sort episodes_data by 'episodeNumber' in ascending order
#     #     episodes_data.sort(key=lambda x: x['episodeNumber'])
#     #     print(episode_info["contentID"])
#     #     # print(episodes_data)
#     #     ZEE5API(hevc=True).procrss_ready(episodes_data[0]["contentID"])

#     def get_mpd_url(self, mpd_url):
#         if "/4K/" in mpd_url and "v2-prime" not in mpd_url:
#             mpd = mpd_url.replace("manifest.mpd", "manifest-connected-4k.mpd")
#         else:
#             mpd = mpd_url

#         if self.hevc == True:
#             if "connected" in mpd:
#                 return mpd
#             else:
#                 return mpd
#         else:
#             return mpd.replace("manifest-connected-4k.mpd", "manifest.mpd")


#     def extract_streams(self, contentID):
#         # contentID = ""
#         response = requests.post(
#             f"https://spapi.zee5.com/singlePlayback/getDetails/secure?content_id={contentID}&device_id=iseJrXNCJ3kMOao3drB2000000000000&platform_name=mobile_web&translation=en&user_language=en,hi&country=IN&state=WB&app_version=4.2.2&user_type=premium&check_parental_control=false&uid=111cc006-997e-410f-a12a-0f00fee418fe&ppid=iseJrXNCJ3kMOao3drB2000000000000&version=12", headers=self.headers, json=self.json_data, proxies=proxies).json()

#         # print(response)
#         nl = response.get('keyOsDetails', {}).get('nl')
#         sdrm = response.get('keyOsDetails', {}).get('sdrm')

#         lic_headers = {}
#         lic_url = ""

#         if nl and sdrm:
#             lic_headers = {'nl': nl, 'customdata': sdrm}
#             lic_url = "https://spapi.zee5.com/widevine/getLicense"

#         if response.get("error_msg") == "Token Expired":
#             raise("ZEE5 TOKEN EXPIRED")
#         print("mpd is ❤️ ", self.get_mpd_url(response['assetDetails']['video_url']['mpd'])) ###
#         data = {
#             "seriesTitle": response['assetDetails']['title'],
#             "duration": response['assetDetails']['duration'],
#             "mpd": self.get_mpd_url(response['assetDetails']['video_url']['mpd']),
#             "license_headers": lic_headers,
#             "license": lic_url,
#             "seasonNumber": 0,
#             "episodeNumber": 0,
#             "releaseYear": response['assetDetails']['release_date'][:4],
#             "releaseDate": response['assetDetails']['release_date'][:10],
#             "image_url": f"https://akamaividz2.zee5.com/image/upload/resources/{response['assetDetails']['id']}/list/{response['assetDetails']['image']['list']}.jpg",
#             "synopsis": response['assetDetails']['description'],
#             "name": None,
#             "ott": "ZEE5",
#         }

#         # (self.mpd, key, self.name, self.ott,  baseurl, pssh, filename, subtitle_data, videos_data, audios_data)

#         if response['assetDetails'].get("tvshow_name"):
#             data["seriesTitle"] = response['assetDetails']['tvshow_name']
#             data["episodeName"] = response['assetDetails']['original_title']
#             data["episodeNumber"] = int(response['assetDetails']['orderid'])

#             for season in response['showDetails']['seasons']:
#                 if season["id"] == response['showDetails']['season']:
#                     data["seasonNumber"] = int(season["orderid"])

#             data["name"] = "{} S{:02d}E{:02d} {}".format(
#                 response['assetDetails']['tvshow_name'].strip(),
#                 data['seasonNumber'],
#                 data['episodeNumber'],
#                 data["episodeName"]
#             )

#             data["name"] = data["name"].replace(
#                 "/", "_").replace("~", "").replace(":", "").replace(" - ", "")
#         else:
#             data["name"] = "{} {}".format(
#                 response['assetDetails']['title'], response['assetDetails']['release_date'][:4]).replace("/", "_").replace("~", "").replace(":", "")

#         if not data['license'] == "":
#             key = find_keys(data['mpd'], data['license'], data['license_headers'])
#         else:
#             key = None
#         print_message("EXTRACTING KEYS", "KEYS", " ".join(key))
#         print("\n")

#         und_lang=None

#         videos_data, audios_data, subtitle_data, baseurl, pssh = MPD(data['mpd'], data['name'], data['ott'], self.custom_group_tag).parse(und_lang= und_lang)


#                                             #  this MPD is return the selected qulity to dl file directly
#         videoslist, audioslist, subtitlelist, pssh, baseurl, filename  =  MPD(data['mpd'], data['name'], data['ott'], self.custom_group_tag).refine(video_resolution="480p",
#          video_quality="LQ", audio_codec="acc", audio_quality="LQ", 
#          audio_languages=None, und_lang=None)


#         return data, key, baseurl, pssh, filename, subtitle_data, videos_data, audios_data

#     # def procrss_ready(self, contentID):
#     #     stream_details = ZEE5API(hevc=True).extract_streams(contentID)

#     #     self.mpd, self.lic_url, self.lic_headers, self.name, self.ott = stream_details.get("mpd"), stream_details.get(
#     #         "license"), stream_details.get("license_headers"), stream_details.get("name"), stream_details.get("ott")
        

#     #     print("name is ❤️ ", self.name)

#     #     if not self.lic_url == "":
#     #         key = find_keys(self.mpd, self.lic_url, self.lic_headers)
#     #     else:
#     #         key = None
#     #     print_message("EXTRACTING KEYS", "KEYS", " ".join(key))
#     #     print("\n")
        
#     #     # try:
#     #     und_lang=None
#     #     # GROUP_TAG = "chung-C"


#     #                                         #  this MPD is return the whole qulity which helps to generetae buttons
#     #     videos_data, audios_data, subtitle_data, baseurl, pssh = MPD(self.mpd, self.name, self.ott, self.custom_group_tag).parse(und_lang= und_lang)


#     #                                         #  this MPD is return the selected qulity to dl file directly
#     #     videoslist, audioslist, subtitlelist, pssh, baseurl, filename  =  MPD(self.mpd, self.name, self.ott, self.custom_group_tag).refine(video_resolution="480p",
#     #      video_quality="LQ", audio_codec="acc", audio_quality="LQ", 
#     #      audio_languages=None, und_lang=None)
        
#     #     # print(videoslist, audioslist, subtitlelist, pssh, baseurl, filename,"")
#     #     # print(MPD_detials,"\n\n")
#     #     #         
#     #     return self.mpd, key, self.name, self.ott,  baseurl, pssh, filename, subtitle_data, videos_data, audios_data
        
#     # def Processor(self):#, mpd, key, name, ott):

#     #     return 


# # filename_generator = FilenameGenerator(audioslist, videoslist, self.subtitlelist, self.init_file_name,
# #                                         self.ott, self.custom_group_tag, videoslist["height"], language_order)
# # filename = filename_generator.generate_filename()


    

# # print(ZEE5API(hevc=True).extract_streams("0-1-6z5637337"))
# # ZEE5API(hevc=True).extract_streams("0-0-1z5294923")
# # print(ZEE5API(hevc=True).Processor())
