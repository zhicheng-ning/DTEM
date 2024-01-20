import os
import sys
import json
import random
import time
import signal

import requests

# API Tokens
auth_tokens = [
    "example_tokens"
]

# 定义感兴趣的文件类型后缀
suffixs = [
    ".py", ".ipynb",    # python 
    ".java",            # Java
    ".js",              # JavaScript
    ".php",             # PHP
    ".rb",              # Ruby
    ".go",              # Go
    ]
# 定义需要忽略的文件或目录前缀
ignore_prefixs = [
    ".github",
    "build",
    ".vscode",
    ".docs",
    ".doc",
    ".licenses",
    ".license",
    "dist"
]
# 一个装饰器，用于为函数设置超时时间，防止某些函数执行时间过长。
def set_timeout(num):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError
 
        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟
                r = func(*args, **kwargs)
                signal.alarm(0)  # 关闭闹钟
                return r
            # 超时返回
            except RuntimeError as e:
                return None
 
        return to_do
 
    return wrap

class Crawler(object):
    def __init__(self, log_file):
        self.errlog = open(os.path.join(os.path.dirname(__file__), log_file), "a+", encoding="utf-8")

    def __del__(self):
        self.errlog.close()

    # @set_timeout(180)
    def request(self, url, auth_token=None, retry=2):
        if not auth_token:
            auth_token = auth_tokens
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token {}".format(auth_token)
        }
        while retry:
            try:
                response = requests.get(url, headers=headers)
                print(response.headers)
                print(response)
            except requests.exceptions.ProxyError as e:
                print("爬取速度过快了，休息一分钟")
                time.sleep(60)
            except requests.exceptions.SSLError as e:
                print("爬取速度过快了，休息一分钟")
                time.sleep(60)
            except requests.exceptions.ConnectionError as e:
                print("爬取速度过快了，休息一分钟")
                time.sleep(60)
            else:
                if response.status_code == 200:
                    return response
                else:
                    return None
            time.sleep(random.randint(1, 3))
            retry -= 1
        return None
    
    def requestWithTokens(self, url, auth_token_list, retry=1):

        os.environ['http_proxy'] = 'http://127.0.0.1:7890'
        os.environ['https_proxy'] = 'http://127.0.0.1:7890'
        headers = {
            "Accept": "application/vnd.github.v3+json",
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }
        if not auth_token_list or auth_token_list is None:
            auth_token_list = auth_tokens
        for token in auth_tokens:
            
            headers["Authorization"] = f'token {token}'
            # print("current_token:",token)
            retry = 1
            while retry > 0:
                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        # print("response:",response)
                        print("url:",url)
                        return response
                    elif response.status_code == 403:
                        # 处理速率限制或其他需要切换token的情况
                        print(f"Token {token} is rate limited or not valid, switching to next token.")
                        break  # 跳出重试循环，切换到下一个token
                    else:
                        # 对于其他错误，你可能希望记录或重试
                        print(f"Request failed with status code {response.status_code}. Retrying...")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed with exception {e}. Retrying...")
                #time.sleep(random.randint(1, 3))  # 简单的退避策略，避免立即重试
                retry -= 1
            
        return None  # 所有token都用完或请求失败
    def get_owner_and_repo_from_gh_url(self, gh_url:str):
        last_idx = gh_url.rfind("/")
        repo = gh_url[last_idx+1:]
        last_second_idx = gh_url[:last_idx].rfind("/")
        owner = gh_url[last_second_idx+1:last_idx]
        return owner, repo

    def get_gh_url_from_owner_and_repo(self, owner, repo):
        return "https://github.com/{}/{}".format(owner, repo)
    
    def err_handling(self, url):
        self.errlog.write(url+"\n")
        pass