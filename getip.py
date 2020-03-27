# 获取github和其子域名的IP地址
import re
import platform
import requests
from bs4 import BeautifulSoup
import threading


def get_host():
    for i in open("url.txt"):
        url = i.strip()
        t = MyThread(url)
        t.start()


class MyThread(threading.Thread):

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        host = self.url
        self.url = "http://ip.chinaz.com/" + self.url
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.text, features="html.parser")
        x = soup.find(class_="IcpMain02")
        x = x.find_all("span", class_="Whwtdhalf")
        print(x[5].string.strip(), host)


host_window = r"C:\Windows\System32\drivers\etc\hosts"
host_mac = r"/etc/hosts"
UAT_HOST = ["#B2B uat deepblue2",
            '10.128.xx.xx uat.xx.com',
            '10.128.xx.xx xx.com',
            '10.128.xx.xx xx.com']

HOST_LIVE = ["#LIVE",
             "104.20.xx.xx       xxx.com",
             "104.20.xx.xx       www.xxx.com",
             "104.20.xx.xx       www.xxx.br"]


def search_host(hostvalue, host_path):
    hostfile = open(host_path, 'r')
    each_line = hostfile.readlines()
    hostfile.close()
    findresult = re.findall(hostvalue, ''.join(each_line))
    return findresult


def write_host(host_value):
    if platform.system() is "Windows":
        output = open(host_window, 'a')
    else:
        output = open(host_mac, 'a')

    output.write("# GitHub Start")
    for inside in host_value:
        output.write(inside)
        output.newlines()
    output.write("# GitHub End")
    output.close()


if __name__ == "__main__":
    get_host()

    # if search_host(HOST_LIVE[0], host_window):
    #     print("it exist, no need to update")
    # else:
    #     write_host(HOST_LIVE)
