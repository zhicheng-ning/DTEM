import os
import sys
import json

from path import LOG_DIR, CRAWLED_DIR, SELECTED_REPO_PATH, CLEANED_DIR

class DataCleaner(object):
    def __init__(self, src_dir=CRAWLED_DIR, dst_dir=CLEANED_DIR, selected_repos=SELECTED_REPO_PATH) -> None:
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        with open(selected_repos, "r", encoding="utf-8") as inf:
            self.selected_repos = json.load(inf)
        self.selected_contributors = set()
        pass

    def clean_repo_statistics(self, filename="repo_statistics.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                # print(line)
                obj = json.loads(line)
                if obj["full_name"] not in self.selected_repos:
                    continue
                outf.write(line)
        pass

    def clean_repo_contributions(self, filename="repo_contributions.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                repo, contris = line.strip().split("\t")
                contris = json.loads(contris)
                if repo not in self.selected_repos:
                    continue
                new_contris = []
                for c in contris:
                    if "[bot]" in c[0] or "-bot" in c[0] or "_bot" in c[0]:
                        continue
                    new_contris.append(c)
                    self.selected_contributors.add(c[0])
                outf.write("{}\t{}\n".format(repo, json.dumps(new_contris, ensure_ascii=False)))
        pass

    def clean_repo_stars(self, filename="repo_stargazers.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                repo, stargazers = line.strip().split("\t")
                if repo not in self.selected_repos:
                    continue
                stargazers = json.loads(stargazers)
                stargazers = [s for s in stargazers if s in self.selected_contributors]
                outf.write("{}\t{}\n".format(repo, json.dumps(stargazers, ensure_ascii=False)))
        pass

    def clean_repo_watchers(self, filename="repo_watchers.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                repo, watchers = line.strip().split("\t")
                if repo not in self.selected_repos:
                    continue
                watchers = json.loads(watchers)
                watchers = [s for s in watchers if s in self.selected_contributors]
                outf.write("{}\t{}\n".format(repo, json.dumps(watchers, ensure_ascii=False)))
        pass

    def clean_repo_issues(self, filename="repo_issues.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                repo, issues = line.strip().split("\t")
                if repo not in self.selected_repos:
                    continue
                issues = json.loads(issues)
                # body不可为空，或者巨短
                # 提出者不能是bot
                new_issues = [i for i in issues if i["body"] and len(i["body"]) > 10 and "[bot]" not in i["committer"] and "-bot" not in i["committer"] and "_bot" not in i["committer"]]
                contributors = [i["committer"] for i in new_issues]
                self.selected_contributors.update(contributors)
                outf.write("{}\t{}\n".format(repo, json.dumps(new_issues, ensure_ascii=False)))
        pass
    
    def clean_repo_prs(self, filename="repo_prs.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                repo, prs = line.strip().split("\t")
                if repo not in self.selected_repos:
                    continue
                prs = json.loads(prs)
                new_prs = [i for i in prs if i["body"] and len(i["body"]) > 10 and "[bot]" not in i["committer"] and "-bot" not in i["committer"] and "_bot" not in i["committer"]]
                contributors = [i["committer"] for i in new_prs]
                self.selected_contributors.update(contributors)
                outf.write("{}\t{}\n".format(repo, json.dumps(new_prs, ensure_ascii=False)))
        pass
    
    def clean_user_followers(self, user_followings_filename="user_followings.txt", user_followers_filename="user_followers.txt"):
        with open(os.path.join(self.src_dir, user_followings_filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, user_followings_filename), "w", encoding="utf-8") as outf:
            for line in inf:
                user, followings = line.strip().split("\t")
                if user not in self.selected_contributors:
                    continue
                followings = json.loads(followings)
                new_followings = [i for i in followings if i in self.selected_contributors]
                outf.write("{}\t{}\n".format(user, json.dumps(new_followings, ensure_ascii=False)))
        with open(os.path.join(self.src_dir, user_followers_filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, user_followers_filename), "w", encoding="utf-8") as outf:
            for line in inf:
                user, followers = line.strip().split("\t")
                if user not in self.selected_contributors:
                    continue
                followers = json.loads(followers)
                new_followers = [i for i in followers if i in self.selected_contributors]
                outf.write("{}\t{}\n".format(user, json.dumps(new_followers, ensure_ascii=False)))
        pass

    def clean_user_organizations(self, filename="user_organizations.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                usr, ogs = line.strip().split("\t")
                if usr not in self.selected_contributors:
                    continue
                outf.write(line)
    
    def clean_repo_pr_commits(self, filename="repo_pr_commits.txt"):
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                repo = line.strip().split("\t")[0]
                if repo not in self.selected_repos:
                    continue
                outf.write(line)
    
    def clean_repo_languages(self, filename="repo_languages.txt"):
        has_languaged_repos = set()
        with open(os.path.join(self.src_dir, filename), "r", encoding="utf-8") as inf, open(os.path.join(self.dst_dir, filename), "w", encoding="utf-8") as outf:
            for line in inf:
                repo, langs = line.strip().split("\t")
                repo_lower = repo
                if repo_lower not in self.selected_repos:
                    continue
                has_languaged_repos.add(repo_lower)
                outf.write("{}\t{}\n".format(repo_lower, langs))
        with open("stupid.txt", "w", encoding="utf-8") as outf:
            for x in set(self.selected_repos) - has_languaged_repos:
                outf.write(x+"\n")
    
    def clean(self):
        self.clean_repo_statistics()
        self.clean_repo_pr_commits()
        self.clean_repo_languages()
        self.clean_repo_contributions()
        self.clean_repo_prs()
        self.clean_repo_issues()
        self.clean_repo_stars()
        self.clean_repo_watchers()
        self.clean_user_followers()
        self.clean_user_organizations()

if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.clean()
    

'''
上述代码定义了一个名为 `DataCleaner` 的Python类，主要用于清洗和过滤从GitHub爬取的数据。这个类通过一系列的方法处理原始数据，以生成清洗过的、格式统一的数据文件。具体来说：

1. **初始化 (`__init__`)**:
   - 初始化时，设置源数据目录 (`src_dir`)、目标数据目录 (`dst_dir`) 和已选择仓库列表的路径 (`selected_repos`)。
   - 从给定路径加载已选择仓库列表到 `self.selected_repos`。
   - 初始化一个空集合 `self.selected_contributors` 用于存放选定的贡献者。

2. **数据清洗方法**:
   - 这些方法针对不同类型的数据文件执行清洗任务，如 `clean_repo_statistics`, `clean_repo_contributions`, `clean_repo_stars`, `clean_repo_watchers`, `clean_repo_issues`, `clean_repo_prs`, `clean_user_followers`, `clean_user_organizations`, `clean_repo_pr_commits`, `clean_repo_languages`。
   - 这些方法通常通过以下步骤清洗数据：
     - 打开源文件和目标文件。
     - 逐行读取源文件，对每一行：
       - 解析数据（通常是JSON格式）。
       - 检查数据是否符合特定条件（例如，是否属于选定的仓库或贡献者）。
       - 过滤或转换数据（例如，排除机器人用户，或仅保留特定字段）。
       - 将清洗过的数据写入目标文件。

3. **清洗流程 (`clean`)**:
   - `clean` 方法依次调用上述定义的清洗方法，对所有相关数据执行清洗流程。

4. **执行清洗 (`__name__ == "__main__"`)**:
   - 当脚本作为主程序运行时，会创建 `DataCleaner` 实例，并调用其 `clean` 方法来执行清洗流程。

总体来说，这个 `DataCleaner` 类封装了一个从原始爬取数据到清洗后数据的处理流程，通过过滤、转换和选择特定数据，为后续的数据分析和推荐系统提供更清洁、更一致的数据基础。
'''
    