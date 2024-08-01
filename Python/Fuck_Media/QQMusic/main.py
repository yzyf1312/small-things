import subprocess
import requests
import random
import json
import time
import re
import os

def cleartext(original_string):
    special_chars_with_spaces = r'\s*[\\\/\:\*\?"<>|\-]\s*'

    replaced_string = re.sub(special_chars_with_spaces, '_', original_string)
    return replaced_string

# 定义常量
## 循环间时间间隔的范围(防止可能存在的风控)
min_wait = 0.3
max_wait = 0.8

# 获取当前工作目录
current_directory = os.getcwd()

disstid_data = input("请输入歌单的 disstid:")
cookie_string = input("Press your cookie here:")

base_url = "https://i.y.qq.com/qzone-music/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg"

# 配置载荷
get_payload = "?type=1&json=1&utf8=1&onlysong=0&nosign=1&disstid=" + disstid_data + "&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=GB2312&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
target_url = base_url + get_payload

# 构造请求头
## Rederer 非常重要!
header_data = {
    'Referer': 'https://y.qq.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

fcg = requests.get(target_url,headers=header_data)
fcg_data = json.loads(fcg.text)

for cdlist_item in fcg_data["cdlist"]:
    songlist_data = cdlist_item.get("songlist", [])
    dissname_data = cleartext(cdlist_item["dissname"])
    
    for song_data in songlist_data:
        # 安全地获取每个歌曲的"songname"和"songmid"，如果不存在则使用默认值
        song_songname = song_data.get("songname", "Default Song Name")
        song_albumname = song_data.get("albumname", "Default Song Albumname")
        song_songmid = song_data.get("songmid", "Default Song MID")

        # 获取歌手
        ## 下面一行用于初始化，变量 is_first_singer 用于判断是否为第一个歌手
        is_first_singer = True
        for singer_data in song_data["singer"]:
            if is_first_singer:
                is_first_singer = False
                singer_name_string = singer_data["name"]
                singer_name_data = singer_data["name"]
            else:
                singer_name_string = singer_name_string + "、" + singer_data["name"]
                singer_name_data = singer_name_data + "/" + singer_data["name"]
        
        local_filename = cleartext(song_songname) + " - " + singer_name_string + ".mp3"

        # 使用os.path.join来构建正确的文件路径
        local_file = os.path.join(current_directory, dissname_data, local_filename)

        # 伪断点续传
        if os.path.exists(local_file):
            continue

        wait_time = random.uniform(min_wait, max_wait)
        time.sleep(wait_time)  # 等待随机生成的时间

        print(f"{song_songname}:{song_songmid}")

        # 获取 musicu.fcg

        # 构造请求使用到的文件名
        filename = "M500" + song_songmid + song_songmid + ".mp3"

        # 构建请求的载荷
        payload = {
"req_1": {
    "module": "vkey.GetVkeyServer",
    "method": "CgiGetVkey",
    "param": {
        "filename": [
            filename
        ],
        "guid": "10000",
        "songmid": [
            song_songmid
        ],
        "songtype": [
            0
        ],
        "uin": "0",
        "loginflag": 1,
        "platform": "20"
    }
},
"loginUin": "0",
"comm": {
    "uin": "0",
    "format": "json",
    "ct": 24,
    "cv": 0
}
}

        header_data = {
            'Content-Type': 'application/json',
            'Cookie': cookie_string,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'  # 根据需要设置User-Agent
        }

        # 发送POST请求
        # 要将payload转换为JSON格式的字符串，因为requests默认发送application/x-www-form-urlencoded格式
        response = requests.post(
            'https://u.y.qq.com/cgi-bin/musicu.fcg',
            data=json.dumps(payload),  # 将payload字典转换为JSON字符串
            headers=header_data
        )

        response_data = json.loads(response.text)
        req_1_data = response_data["req_1"]

        data_data = req_1_data["data"]
        midurlinfo_data = data_data["midurlinfo"][0]
        purl_data = midurlinfo_data["purl"]

        if purl_data == "":
            print("链接获取失败")
        else:
            url_data = "http://ws.stream.qqmusic.qq.com/" + purl_data

            # 确保目录存在
            os.makedirs(os.path.dirname(local_file), exist_ok=True)

            # 使用aria2进行下载
            command = [
                './aria2c.exe',
                '-o', local_filename,  # 输出文件名
                '-d', os.path.dirname(local_file),  # 输出目录
                '-s', '16',  # 同时尝试的源数
                url_data
            ]

            # 运行aria2命令
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print(f"Download completed for {local_filename}")
            else:
                print(f"Error downloading {local_filename}: {stderr.decode()}")

