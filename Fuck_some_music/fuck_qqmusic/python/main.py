from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
from mutagen.mp3 import MP3
from browser_cookie3 import load
import subprocess
import requests
import random
import json
import time
import re
import os


def cookie_filter_for_qqmusic_from_browser():
    cookies = load(domain_name="qq.com")

    tocheck_list = ["wxopenid", "wxuin", "qm_keyst"]

    temp_dict = {}

    for c in cookies:
        if c.name in tocheck_list:
            temp_dict[c.name] = c.value

    is_first_run = True
    for item in tocheck_list:
        if is_first_run:
            cookie_str = item + "=" + temp_dict[item]
            is_first_run = False
        else:
            cookie_str = cookie_str + "; " + item + "=" + temp_dict[item]

    return cookie_str


def get_cdinfo_fcg(disstid_data):
    # 配置载荷
    target_url = (
        "https://i.y.qq.com/qzone-music/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg"
        + "?type=1&json=1&utf8=1&onlysong=0&nosign=1&disstid="
        + disstid_data
        + "&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=GB2312&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    )

    # 构造请求头
    ## Rederer 非常重要!
    header_data = {
        "Referer": "https://y.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }

    return requests.get(target_url, headers=header_data)


def post_musicu_fcg(filename, songmid, cookie_string):
    # 构建请求的载荷
    payload = {
        "req_1": {
            "module": "vkey.GetVkeyServer",
            "method": "CgiGetVkey",
            "param": {
                "filename": [filename],
                "guid": "10000",
                "songmid": [songmid],
                "songtype": [0],
                "uin": "0",
                "loginflag": 1,
                "platform": "20",
            },
        },
        "loginUin": "0",
        "comm": {"uin": "0", "format": "json", "ct": 24, "cv": 0},
    }

    header_data = {
        "Content-Type": "application/json",
        "Cookie": cookie_string,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",  # 根据需要设置User-Agent
    }

    retry_times = 0
    while retry_times < 4:
        try:
            response = requests.post(
                "https://u.y.qq.com/cgi-bin/musicu.fcg",
                data=json.dumps(payload),  # 将payload字典转换为JSON字符串
                headers=header_data,
                timeout=2,
            )
            return response.text
        except requests.exceptions.RequestException:
            retry_times += 1
            if retry_times >= 4:
                print(f"请求超时{retry_times}次，跳过此歌曲")
            else:
                print(f"请求超时，进行第{retry_times}次重试")


def update_song_tags(song_file_path, album_pic, song_name, singer_name, album_name):

    # 打开音频文件
    song = MP3(song_file_path, ID3=ID3)

    # 处理元数据
    song.tags.add(TIT2(encoding=3, text=song_name))  # 歌曲标题
    song.tags.add(TPE1(encoding=3, text=singer_name))  # 艺术家
    song.tags.add(TALB(encoding=3, text=album_name))  # 专辑

    if not os.path.exists(album_pic):
        print("使用默认歌曲封面")
        album_pic = "QQMusic_redesign.jpg"

    # 打开封面图片文件
    with open(album_pic, "rb") as image_file:
        # 创建 APIC 对象
        # encoding=3 表示使用 UTF-8 编码
        # mime='image/jpeg' 表示图片格式为 JPEG
        # type=3 表示这是封面图片
        picture = APIC(encoding=3, mime="image/jpeg", type=3, data=image_file.read())

        # 添加封面图片到 ID3 标签
        song.tags.add(picture)

    # 保存更改
    song.save()

    print(f"Update tags completed for song:{song_name}")


def cleartext(original_string):
    special_chars_with_spaces = r'\s*[\\\/\:\*\?"<>|\-]\s*'

    replaced_string = re.sub(special_chars_with_spaces, "_", original_string)
    return replaced_string


def path_check(path):
    # 检查路径是否指向有扩展名的文件

    # 获取路径末端的对象
    base_name = os.path.basename(path)

    # 找到最后一个英文句号的位置
    last_period_index = base_name.rfind(".")

    # 检查句号之后是否还有字符
    if last_period_index != -1 and last_period_index < len(base_name) - 1:
        return True
    else:
        return False


def aria2_download(url, file_path, file_name):
    if path_check(file_path):
        command = [
            "./aria2c.exe",
            "-o",
            file_name,  # 输出文件名
            "-d",
            os.path.dirname(file_path),  # 输出目录
            "-s",
            "16",  # 同时尝试的源数
            url,
        ]
    else:
        command = [
            "aria2c.exe",
            "-o",
            file_name,  # 输出文件名
            "-d",
            file_path,  # 输出目录
            "-s",
            "16",  # 同时尝试的源数
            url,
        ]

    retry_times = 0
    while retry_times < 4:

        # 运行aria2命令
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        try:
            stdout, stderr = process.communicate(timeout=16)

            if process.returncode == 0:
                print(f"Download completed for {file_name}")
                return "succeed"
            else:
                retry_times += 1
                print(f"Error downloading {file_name}: {stderr.decode()}")
            if retry_times >= 4:
                print(f"Error downloading {retry_times} times, skip {file_name}")
                return "skip"
        except subprocess.TimeoutExpired:
            process.kill()  # 终止进程
            retry_times += 1
            if retry_times >= 4:
                return "skip"
            else:
                print(f"Aria2下载超时，进行第{retry_times}次重试")


def lyric_downlaod(song_songmid, lyric_file):
    base_url = "https://i.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"

    # 配置载荷
    get_payload = (
        "?songmid="
        + song_songmid
        + "&g_tk=5381&format=json&inCharset=utf8&outCharset=utf-8&nobase64=1"
    )
    target_url = base_url + get_payload

    # 构造请求头
    ## Rederer 非常重要!
    header_data = {
        "Referer": "https://y.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }

    retry_times = 0
    while retry_times < 8:
        try:
            fcg = requests.get(target_url, headers=header_data, timeout=2)

            fcg_data = json.loads(fcg.text)

            with open(lyric_file, "w", encoding="utf-8") as lyric:
                if "lyric" in fcg_data:
                    lyric.write(fcg_data["lyric"])

                    print("歌词写入完成")
                    return "succeed"
                else:
                    lyric.write("[00:00:00]此歌曲暂无歌词")

                    print("无法找到歌词数据，写入空数据")
                    return "fail"
        except requests.exceptions.RequestException:
            retry_times += 1
            if retry_times >= 8:
                print(f"请求超时{retry_times}次，跳过此歌词")
                return "skip"
            else:
                print(f"请求超时，进行第{retry_times}次重试")


def get_purl_from_musicu_fcg(filename_prefix, song_songmid, cookie_string):
    # 获取 musicu.fcg

    # 构造请求使用到的文件名
    filename = filename_prefix + song_songmid + song_songmid + ".mp3"

    # 发送POST请求
    # 要将payload转换为JSON格式的字符串，因为requests默认发送application/x-www-form-urlencoded格式

    response_text = post_musicu_fcg(filename, song_songmid, cookie_string)

    if response_text == None:
        return "None"

    response_data = json.loads(response_text)
    req_1_data = response_data["req_1"]

    data_data = req_1_data["data"]
    midurlinfo_data = data_data["midurlinfo"][0]
    purl_data = midurlinfo_data["purl"]

    return purl_data


def main(disstid_data, cookie_string):

    if cookie_string == "":
        cookie_string = cookie_filter_for_qqmusic_from_browser()

    # 定义常量
    ## 循环间时间间隔的范围(防止可能存在的风控)
    min_wait = 0.3
    max_wait = 0.8

    # 获取当前工作目录
    current_directory = os.getcwd()

    fcg_data = json.loads(get_cdinfo_fcg(disstid_data).text)

    skip_times = 0

    for cdlist_item in fcg_data["cdlist"]:
        songlist_data = cdlist_item.get("songlist", [])
        dissname_data = cleartext(cdlist_item["dissname"])

        for song_data in songlist_data:
            # 安全地获取每个歌曲的信息，如果不存在则使用默认值
            song_songname = song_data.get("songname", "Default Song Name")
            song_albumname = song_data.get("albumname", "Default Song Albumname")
            song_albummid = song_data["albummid"]
            song_songmid = song_data.get("songmid", "Default Song MID")

            # 获取歌手
            ## 下面一行用于初始化，变量 is_first_singer 用于判断是否为第一个歌手
            is_first_singer = True
            for singer_data in song_data["singer"]:
                singer_name_temp = cleartext(singer_data["name"])
                if is_first_singer:
                    is_first_singer = False
                    singer_name_string = singer_name_temp
                    singer_name_data = singer_name_temp
                else:
                    singer_name_string = singer_name_string + "、" + singer_name_temp
                    singer_name_data = singer_name_data + "/" + singer_name_temp

            local_filename = (
                cleartext(song_songname) + " - " + singer_name_string + ".mp3"
            )

            # 使用os.path.join来构建正确的文件路径
            local_file = os.path.join(current_directory, dissname_data, local_filename)

            # 伪断点续传
            if os.path.exists(local_file):
                continue

            wait_time = random.uniform(min_wait, max_wait)
            time.sleep(wait_time)  # 等待随机生成的时间

            print(f"{song_songname}:{song_songmid}")

            song_size_320 = song_data["size320"]
            song_size_128 = song_data["size128"]

            if song_size_320 != 0:
                filename_prefix = "M800"
            elif song_size_128 != 0:
                filename_prefix = "M500"
            else:
                print(song_songname + ":找不到可用的音质")
                continue

            # # 获取 musicu.fcg

            # # 构造请求使用到的文件名
            # filename = filename_prefix + song_songmid + song_songmid + ".mp3"

            # # 发送POST请求
            # # 要将payload转换为JSON格式的字符串，因为requests默认发送application/x-www-form-urlencoded格式

            # response_text = post_musicu_fcg(filename,song_songmid,cookie_string)

            # if response_text == None:
            #     skip_times += 1
            #     continue

            # response_data = json.loads(response_text)
            # req_1_data = response_data["req_1"]

            # data_data = req_1_data["data"]
            # midurlinfo_data = data_data["midurlinfo"][0]
            # purl_data = midurlinfo_data["purl"]

            purl_data = get_purl_from_musicu_fcg(
                filename_prefix, song_songmid, cookie_string
            )

            if purl_data == "None":
                skip_times += 1
                continue

            if purl_data == "" and song_size_320 != 0 and song_size_128 != 0:
                print("链接获取失败")
                print("降低音质重试")
                filename_prefix = "M500"
                purl_data = get_purl_from_musicu_fcg(
                    filename_prefix, song_songmid, cookie_string
                )

            if purl_data == "":
                print("链接获取失败")
            else:
                song_url_data = "http://ws.stream.qqmusic.qq.com/" + purl_data
                album_pic_filename = (
                    cleartext(song_songname) + " - " + singer_name_string + ".jpg"
                )
                lyric_filename = (
                    cleartext(song_songname) + " - " + singer_name_string + ".lrc"
                )
                album_pic_url_data = (
                    "https://y.gtimg.cn/music/photo_new/T002R800x800M000"
                    + song_albummid
                    + ".jpg"
                )
                album_pic_file = os.path.join(
                    current_directory, dissname_data, album_pic_filename
                )
                lyric_file = os.path.join(
                    current_directory, dissname_data, lyric_filename
                )

                # 确保目录存在
                os.makedirs(os.path.dirname(local_file), exist_ok=True)

                # 使用 aria2 下载歌曲
                result = aria2_download(song_url_data, local_file, local_filename)
                if result == "skip":
                    print(f"Aria2下载多次超时，跳过{local_filename}的下载")
                    skip_times += 1
                    continue
                # 使用 aria2 下载歌曲封面
                aria2_download(album_pic_url_data, album_pic_file, album_pic_filename)

                # 写入元数据
                update_song_tags(
                    local_file,
                    album_pic_file,
                    song_songname,
                    singer_name_data,
                    song_albumname,
                )

                # 下载歌词
                lyric_downlaod(song_songmid, lyric_file)

    if skip_times != 0:
        print(f"本次跳过了{skip_times}首歌曲")


if __name__ == "__main__":
    cookie_string = input("输入你的 Cookie (留空从浏览器获取):")
    disstid_data = input("输入目标歌单的 disstid:")

    main(disstid_data, cookie_string)
