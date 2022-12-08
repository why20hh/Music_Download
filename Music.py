import requests
import re
from bs4 import BeautifulSoup
import os
from tqdm import tqdm


class DownloadMusic:
    def __init__(self):
        self.search_url = 'https://www.fangpi.net/s/'
        self.all_songs = []
        self.all_singers = []
        self.all_urls = []
        self.session = requests.session()
        self.join_url = 'https://www.fangpi.net'
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def search_music(self):
        music_name = input('请输入想要下载的歌曲的名称：')
        request_url = self.search_url + music_name
        res = self.session.get(request_url).text
        soup = BeautifulSoup(res, 'lxml')
        all_songs = soup.select('table.table > tbody > tr > td:nth-child(1) > a')
        all_singers = soup.select('td.text-success')
        all_urls = soup.select('table.table > tbody > tr > td:nth-child(3) > a')
        i = 1
        for song, singer, url in zip(all_songs, all_singers, all_urls):
            print(i, song.get_text().replace('\n', '').replace(' ', ''), singer.get_text())
            i += 1
            self.all_urls.append(url.get("href"))
        music_num = int(input('请您输入需要下载的歌曲的序号：')) - 1
        self.get_download_link(music_num)

    def get_download_link(self, music_num):
        url = self.all_urls[music_num]
        get_url = self.join_url + url
        res = self.session.get(get_url).text
        get_download_url = re.findall("const url = '(.+?)'", res, re.S)[0]
        get_music_name = re.findall("var name =(.+?);", res, re.S)[0].replace("'", "").replace(" ", "").replace("+", "")
        get_download_url = get_download_url.replace('&amp;', '&')
        self.save_music(get_download_url, get_music_name)
        # print(get_music_name)
        # print(get_download_url)

    def save_music(self, get_download_url, get_music_name):
        song_content = self.session.get(get_download_url, headers=self.headers, stream=True)
        total = int(song_content.headers.get('content-length', 0))
        if not os.path.exists(r'.\下载音乐'):  # os模块判断并创建
            os.makedirs(r'.\下载音乐')
        with open(r'.\下载音乐\{}.mp3'.format(get_music_name), 'wb') as file, tqdm(
                desc=get_music_name,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in song_content.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)



if __name__ == '__main__':
    a = DownloadMusic()
    a.search_music()
