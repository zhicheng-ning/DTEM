import os
import json
import re
import sys
import random
from urllib import response
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import Crawler
from path import CRAWLED_DIR, LOG_DIR, SELECTED_REPO_PATH

class RepositoryCrawler(Crawler):
    def __init__(
        self, 
        log_file=LOG_DIR+"respository_err.log"):
        super(RepositoryCrawler, self).__init__(log_file)

    def crawl_with_github_url(self, gh_url, auth_token=None):
        owner, repo = self.get_owner_and_repo_from_gh_url(gh_url)
        return self.crawl(owner, repo, auth_token)
    
    # origin code
    # def crawl_with_target_url(self, url, auth_token=None):
    #     print("Now crawling URL: {}".format(url))

    #     response = self.request(url, auth_token)
    #     if not response:
    #         self.err_handling(url)
    #         return {}
    #     return response.json()
    
    def crawl_with_target_url(self, url, auth_token=None):
        print("Now crawling URL: {}".format(url))

        #response = self.request(url, auth_token)
        response = self.requestWithTokens(url, auth_token)
        if not response:
            self.err_handling(url)
            return None  # 返回 None 而不是 {}
        try:
            return response.json()  # 尝试解析JSON
        except ValueError:
            # 如果响应不是JSON格式，记录错误并返回None
            self.err_handling(f"Invalid JSON response for URL: {url}")
            return None
    
    def crawl(self, owner, repo, auth_token=None):
        url = "https://api.github.com/repos/{}/{}".format(owner, repo)
        return self.crawl_with_target_url(url, auth_token)

    def crawl_repos(self, repos, auth_token=None, max_workers=10):
        # 使用ThreadPoolExecutor并发执行请求
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_repo = [executor.submit(self.crawl, owner, repo, auth_token) for owner, repo in repos]
            
            for future in as_completed(future_to_repo):
                try:
                    data = future.result()
                    print("data:",data)
                    if data is not None :
                        results.append(data)
                except Exception as exc:
                    print(f' an exception: {exc}')

        print("result:",results)
        return results

# ======================================================
"""
Repo Info Crawler
"""
def crawl_repo_info():
    repo_crawler = RepositoryCrawler()
    skipped_repos = set()
    with open(CRAWLED_DIR+"repo_statistics.txt", "r", encoding="utf-8") as inf:
        for line in inf:
            try:
                obj = json.loads(line)
            except:
                print(line)
                sys.exit(0)
            skipped_repos.add(obj.get("full_name", "").lower())
    
    repo_info_outf = open(CRAWLED_DIR+"repo_statistics.txt", "a+", encoding="utf-8")
    
    with open(SELECTED_REPO_PATH, "r", encoding="utf-8") as inf:
        repo_names = json.load(inf)
        repos = [(name.split("/")[0], name.split("/")[1]) for name in repo_names if name.lower() not in skipped_repos]
        # 并发爬取
        repo_infos = repo_crawler.crawl_repos(repos)
        for info in repo_infos:
            if info:
                repo_info_outf.write(json.dumps(info) + "\n")
                
        # origin code    
        # for repo_name in repo_names:
        #     if repo_name.lower() in skipped_repos:
        #         continue

        #     owner, repo = repo_name.split("/")
        #     repo_info = repo_crawler.crawl(owner=owner, repo=repo)

        #     if repo_info:
        #         repo_info_outf.write(json.dumps(repo_info)+"\n")

if __name__ == "__main__":
    crawl_repo_info()
    
'''
上述代码定义了一个爬虫类 `RepositoryCrawler` 用于从GitHub API获取仓库（repository）的信息，并实现了一个脚本来使用这个爬虫类爬取特定仓库的信息。

具体来说：

1. **定义 `RepositoryCrawler` 类**:
   - 这个类继承自一个名为 `Crawler` 的基类（虽然基类的代码没有在这段中给出，但可以推断出它提供了一些基本的爬虫功能，如请求处理和错误记录）。
   - `RepositoryCrawler` 类提供了额外的方法来爬取GitHub仓库的信息。
   - `crawl_with_github_url` 方法接受一个GitHub仓库的URL，提取所有者（owner）和仓库名（repo），然后调用 `crawl` 方法。
   - `crawl_with_target_url` 方法接受一个URL，使用 `request` 方法（从基类继承）来执行实际的HTTP请求，并处理错误。
   - `crawl` 方法构建GitHub API的URL来获取特定仓库的信息，并调用 `crawl_with_target_url` 方法。

2. **定义 `crawl_repo_info` 函数**:
   - 这个函数使用 `RepositoryCrawler` 类来爬取在 `SELECTED_REPO_PATH` 文件中定义的仓库列表。
   - 函数首先读取已经爬取的仓库信息（`repo_statistics.txt`），并将这些仓库添加到 `skipped_repos` 集合中，以避免重复爬取。
   - 然后，函数读取 `SELECTED_REPO_PATH` 文件中定义的仓库列表，并对于每一个仓库，检查它是否已被爬取（即是否在 `skipped_repos` 中）。如果没有，函数会爬取该仓库的信息并将结果写入 `repo_statistics.txt` 文件。

3. **主执行逻辑 (`if __name__ == "__main__":`)**:
   - 当脚本作为主程序运行时，它会调用 `crawl_repo_info` 函数来执行爬取任务。

总的来说，这段代码实现了一个针对GitHub仓库信息的爬虫。它能从GitHub API获取特定仓库的信息，并记录爬取结果。代码还处理了错误情况，并确保不会重复爬取已经爬过的仓库。
'''