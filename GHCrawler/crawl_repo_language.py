import os
import json
import sys
import time
import random
import shutil
import signal
import subprocess

from config import Crawler, auth_tokens
from path import LOG_DIR, CRAWLED_DIR, SELECTED_REPO_PATH
from concurrent.futures import ThreadPoolExecutor, as_completed


class RepoLanguageCrawler(Crawler):
    def __init__(
        self, 
        log_file=LOG_DIR+"language_err.log"):
        super().__init__(log_file)

    def crawl(self, usr, repo, auth_token=None):
        url = "https://api.github.com/repos/{}/{}/languages".format(usr, repo)
        response = self.requestWithTokens(url, auth_token)
        if not response:
            self.err_handling(url)
            return None
        return response.json()


# ======================================================
"""
Repo Language Crawler
"""
# origin code
# def crawl_repo_languages():
#     cralwer = RepoLanguageCrawler()
#     outf = open(CRAWLED_DIR+"repo_languages.txt", "a+", encoding="utf-8")
#     with open(SELECTED_REPO_PATH, "r", encoding="utf-8") as inf:
#         repo_names = json.load(inf)
#     for repo_name in repo_names:
#         print("Now processing repository: {}".format(repo_name))
#         owner, repo = repo_name.strip().split("/")
#         languages = cralwer.crawl(usr=owner, repo=repo, auth_token=random.choice(auth_tokens))
#         if not languages:
#             continue
#         outf.write("{}\t{}\n".format(repo_name, json.dumps(languages, ensure_ascii=False)))
#     outf.close()
    
def crawl_repo_languages():
    crawler = RepoLanguageCrawler()
    with open(CRAWLED_DIR+"repo_languages.txt", "a+", encoding="utf-8") as outf, open(SELECTED_REPO_PATH, "r", encoding="utf-8") as inf:
        repo_names = json.load(inf)
        # 使用ThreadPoolExecutor并发执行请求
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_repo = {executor.submit(crawler.crawl, repo_name.strip().split("/")[0],repo_name.strip().split("/")[1]): repo_name for repo_name in repo_names}
            
            for future in as_completed(future_to_repo):
                repo_name = future_to_repo[future]
                try:
                    languages = future.result()
                    if languages is not None:
                        outf.write("{}\t{}\n".format(repo_name, json.dumps(languages, ensure_ascii=False)))
                except Exception as exc:
                    print(f'{repo_name} generated an exception: {exc}')
                    # 可以在这里调用错误处理函数

if __name__ == "__main__":
    crawl_repo_languages()