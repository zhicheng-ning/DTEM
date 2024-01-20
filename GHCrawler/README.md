# 介绍
## 数据介绍
1. ghs.csv文件来自于论文《Sampling Projects in GitHub for MSR Studies》开源的[GitHub数据集](https://seart-ghs.si.usi.ch)上使用在**2022年之后出现更新**并且**star数目大于等于15**（统计时间截止2022年5月20日）的仓库名称。采样的数据集存放于GHCrawler/ghs.csv

2. 


## 文件介绍
- 1.config.py
爬虫的基类以及一些配置参数

- 2.clean.py
DataCleaner 类封装了一个从原始爬取数据到清洗后数据的处理流程，通过过滤、转换和选择特定数据，为后续的数据分析和推荐系统提供更清洁、更一致的数据基础。

- 3.crawl_repo_info.py
爬取仓库的信息：https://api.github.com/repos/X-lab2017/open-igger

- 4.crawl_repo_languages.py
爬取仓库的language：https://api.github.com/repos/X-lab2017/open-digger/languages

- 5.crawl_repo_readme.py
爬取仓库的readme：https://api.github.com/repos/X-lab2017/open-digger/readme

- 6.crawl_repo_contributors.py
爬取仓库的贡献者（至少有 10 个 contributions）：https://api.github.com/repos/X-Engineer/x-tiktok/contributors?per_page=50&page=1
  
- 7.