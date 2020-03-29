# 获取github和其子域名的IP地址
import os
import re
import platform
from shutil import copyfile, copy

import requests
from bs4 import BeautifulSoup
import threading

from requests.adapters import HTTPAdapter

hosts = []
thread_pool = []
start_line = "# GitHub host start"
end_line = "# GitHub host end"


def get_host():
    for i in open("url.txt"):
        url = i.strip()
        t = MyThread(url)
        t.setName(url)
        thread_pool.append(t)
        t.start()


class MyThread(threading.Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        host = self.url
        self.url = "http://ip.chinaz.com/" + host
        try:
            http_session = requests.Session()
            http_session.mount('http://', HTTPAdapter(max_retries=3))
            request = http_session.get(self.url, timeout=60)
            soup = BeautifulSoup(request.text, features="html.parser")
            ips = soup.find(class_="IcpMain02")
            ips = ips.find_all("span", class_="Whwtdhalf")
            group_num = (len(ips) - 4) / 4
            for i in range(int(group_num)):
                hosts.append(ips[(i + 1) * 4 + 1].string.strip() + " " + host)
                print(ips[(i + 1) * 4 + 1].string.strip() + " " + host)
        except Exception as e:
            print(e)


host_window = r"C:\Windows\System32\drivers\etc\hosts"
host_mac = r"/etc/hosts"


def wait_thread_result():
    stop_flag = True
    while stop_flag:
        for thread in thread_pool:
            if thread.isAlive():
                stop_flag = True
                break
            stop_flag = False


def clean_host():
    with open(host_window, 'r', encoding='UTF-8') as host_file:
        contents = host_file.readlines()
        start_line_num = 0
        end_line_num = 0
        for i, content in enumerate(contents):
            if content.find(start_line) != -1:
                start_line_num = i
            if content.find(end_line) != -1:
                end_line_num = i
        if start_line_num != 0 and end_line_num != 0:
            current_line_num = start_line_num
            while current_line_num <= end_line_num:
                del contents[start_line_num]
                current_line_num += 1
    with open(host_window, 'w+', encoding='UTF-8') as host_file:
        for content in contents:
            host_file.write(content)


def delete_line(old_file, new_file, del_line):
    current_line = 0
    while current_line < (del_line - 1):
        old_file.readline()
        current_line += 1
    # 当前光标在被删除行的行首，记录该位置
    seek_point = old_file.tell()
    # 设置光标位置
    new_file.seek(seek_point, 0)
    # 读需要删除的行，光标移到下一行行首
    old_file.readline()
    # 被删除行的下一行读给 next_line
    next_line = old_file.readline()
    # 连续覆盖剩余行，后面所有行上移一行
    while next_line:
        new_file.write(next_line)
        next_line = old_file.readline()
    # 写完最后一行后截断文件，因为删除操作，文件整体少了一行，原文件最后一行需要去掉
    new_file.truncate()


def write_host(hosts_value):
    if platform.system() is "Windows":
        output = open(host_window, 'a')
    else:
        output = open(host_mac, 'a')

    output.write("\n")
    output.write(start_line + "\n")
    for inside in hosts_value:
        output.write(inside + "\n")
    output.write(end_line)
    output.close()


if __name__ == "__main__":
    get_host()
    wait_thread_result()
    clean_host()
    write_host(hosts)
