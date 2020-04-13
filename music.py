import re
import json
import time
import random
import requests

requests.packages.urllib3.disable_warnings()

def resolve(url, verify=False):
    """
    resolve audio url
    :param url: like 'https://y.qq.com/n/yqq/song/000YU69H3N55rZ.html'
    :return:
    """
    songmid = re.search('/(\w+).html$', url).groups()[0]
    filename = 'C400' + songmid + '.m4a'
    guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000

    d = {
        'format': 'json',
        'cid': 205361747,
        'uin': 0,
        'songmid': songmid,
        'filename': filename,
        'guid': guid,
    }
    r = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg', params=d, verify=False)
    vkey = json.loads(r.content)['data']['items'][0]['vkey']
    audio_url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=66' % (filename, vkey, guid)
    print(audio_url)
    return audio_url

url = resolve('https://y.qq.com/n/yqq/song/0020YPPj0wcofU.html')