import os
import json
import sys
import time
import random
import shutil
import signal
import subprocess
from urllib import response

from config import Crawler
from path import LOG_DIR, CRAWLED_DIR, SELECTED_REPO_PATH

class ContributorCrawler(Crawler):
    def __init__(
        self, 
        per_page,
        log_file=LOG_DIR+"/contributor_err.log"):

        self.per_page = per_page
        super(ContributorCrawler, self).__init__(log_file)

    def crawl_with_github_url(self, gh_url, auth_token=None):
        owner, repo = self.get_owner_and_repo_from_gh_url(gh_url)
        return self.crawl(owner, repo, auth_token)
    
    def crawl_with_target_url(self, url, auth_token=None, contributors_bound_limit=10):
        print("Now crawling URL: {}".format(url))
        results, should_continue = list(), True
        # response = self.request(url, auth_token)
        response = self.requestWithTokens(url,auth_token)
        if not response or not response.json():
            self.err_handling(url)
            return results, False

        for item in response.json():
            if item["contributions"] < contributors_bound_limit:
                should_continue = False
                break
            else:
                results.append([item["login"], item["contributions"]])
        return results, should_continue
    
    def crawl(self, owner, repo, auth_token=None, contributors_bound_limit=10):
        page_no = 0
        should_continue = True
        results = list()
        while should_continue:
            page_no += 1
            url = "https://api.github.com/repos/{}/{}/contributors?per_page={}&page={}".format(owner, repo, self.per_page, page_no)

            page_result, should_continue = self.crawl_with_target_url(url, auth_token, contributors_bound_limit=contributors_bound_limit)
            results.extend(page_result)
        return results

# ======================================================
"""
Repo Contributor Crawler
"""
def crawl_contributor_info():
    contri_crawler = ContributorCrawler(per_page=50)
    crawled_repos = set()
    with open(CRAWLED_DIR+"repo_contributions.txt", "a+", encoding="utf-8") as inf:
        for line in inf:
            repo_name, _ = line.strip().split("\t")
            crawled_repos.add(repo_name.lower())
    
    repo_contri_outf = open(CRAWLED_DIR+"repo_contributions.txt", "a+", encoding="utf-8")
    
    with open(SELECTED_REPO_PATH, "r", encoding="utf-8") as inf:
        repo_names = json.load(inf)
        for repo_name in repo_names:
            if repo_name.lower() in crawled_repos:
                continue

            owner, repo = repo_name.split("/")
            contributors = contri_crawler.crawl(owner=owner, repo=repo)

            repo_contri_outf.write("{}\t{}\n".format(repo_name, json.dumps(contributors, ensure_ascii=False)))

if __name__ == "__main__":
    crawl_contributor_info()

'''
上述代码定义了一个 `ContributorCrawler` 类来爬取GitHub仓库的贡献者信息，并提供了一个脚本来执行这个爬取任务。下面是对代码的详细解释：

### `ContributorCrawler` 类
1. **初始化 (`__init__`)**:
   - 类初始化时接收一个 `per_page` 参数，表示每页请求的贡献者数量，和一个 `log_file` 参数，表示错误日志文件的路径。这些参数被保存为类的属性。
   - 调用父类（`Crawler`）的构造函数。

2. **`crawl_with_github_url` 方法**:
   - 接收一个GitHub仓库的URL和可选的授权令牌（`auth_token`），解析出仓库的所有者（`owner`）和仓库名（`repo`），然后调用 `crawl` 方法来爬取贡献者信息。

3. **`crawl_with_target_url` 方法**:
   - 使用 `self.request` 方法（从父类继承）发送HTTP请求到提供的URL。
   - 检查响应是否有效，无效时记录错误并返回空结果列表和 `False` 表示不再继续。
   - 遍历响应的JSON数据，收集贡献者的登录名和贡献数。如果贡献数低于 `contributors_bound_limit`，停止迭代并返回收集到的结果和 `False` 表示不再继续。

4. **`crawl` 方法**:
   - 分页爬取指定仓库的所有贡献者信息，直到贡献数低于 `contributors_bound_limit` 或没有更多数据。
   - 使用 `crawl_with_target_url` 方法来爬取每一页的数据。
   - 返回收集到的所有贡献者信息。

### `crawl_contributor_info` 函数
- 这个函数定义了爬取逻辑：
   - 创建 `ContributorCrawler` 实例。
   - 读取已爬取的仓库信息，避免重复爬取。
   - 读取待爬取的仓库列表。
   - 遍历仓库列表，跳过已爬取的仓库。
   - 爬取每个仓库的贡献者信息，并将结果写入文件。

### 主逻辑 (`if __name__ == "__main__":`)
- 当脚本作为主程序执行时，调用 `crawl_contributor_info` 函数来开始爬取任务。

整体来看，这段代码是一个相对完整的爬虫程序，专注于从GitHub仓库爬取贡献者信息。它包括请求发送、分页处理、结果收集和错误处理等功能。
'''