# Introduction
This repository is the code submitted for paper **Automatic Representation of Developers' Technical Expertise Based on GitHub Social Network**

# How to Run
Below shows the repository structure. The correspondence between the table results in the paper and the code can be roughly found through the  comments in the directory trees.
```
.
├── GHCrawler # run this to get the dataset in the research scope
│   └── export
├── GNN # run code here to get the detailed GNN performance in table 3 & table 4
│   ├── DataPreprocess
│   ├── HGT
│   │   └── pretrained
│   ├── HetGAT
│   │   ├── bin
│   │   └── pretrained
│   ├── HetGCN
│   │   └── pretrained
│   ├── HetSAGE
│   │   ├── bin
│   │   └── pretrained
│   ├── RGCN
│   │   ├── bin
│   │   └── pretrained
│   └── Visualize
├── NodeFeatureInitializer # run code here to get initial technical expertise embedding of Issue, PR, Repository nodes.
│   ├── IssueEmbedding
│   ├── PREmbedding
│   ├── RepositoryCodeEmbedding
│   ├── RepositoryEmbedding
│   ├── export
│   └── parser
│       ├── tree-sitter-c-sharp
│       ├── tree-sitter-go
│       ├── tree-sitter-java
│       ├── tree-sitter-javascript
│       ├── tree-sitter-php
│       ├── tree-sitter-python
│       └── tree-sitter-ruby
├── RecommendationTasks # run code here to get performance in 4 downstream recommendation tasks which is shown in table 6 & table 7
│   ├── ContributionRepo
│   │   └── metric
│   ├── PRReviewer
│   │   └── metric
│   ├── RepoMaintainer
│   │   └── metric
│   ├── SimDeveloper
│   │   └── metric
│   └── TopicEmbedding # the baseline method in table 6 & table 7
├── T-Test # run code here to get the t-test result in table 5
│   ├── user_contribute_repository
│   └── user_join_repository
└── imgs
```

## 