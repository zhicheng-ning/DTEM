
import os
import json
from path import CRAWLED_DIR
def generate_contributor_json():
    if os.path.exists(CRAWLED_DIR+"repo_contributions.txt"):     
        with open(CRAWLED_DIR+"repo_contributions.txt", "r", encoding="utf-8") as inf,\
        open("contributor_nodes.json","w",encoding="utf-8") as outf:    
            contributors = set()
            for line in inf:
                print(line)
                contributors_list = line.strip().split("\t")[-1]
                contributors_list = json.loads(contributors_list)
                for contributor_pair in contributors_list:
                    # print(contributor_pair)
                    contributors.add(contributor_pair[0])
            json.dump(list(contributors), outf, ensure_ascii=False, indent=4)

    
if __name__ == "__main__":
    generate_contributor_json()