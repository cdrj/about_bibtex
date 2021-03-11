import os
import re
import time

import bibtexparser
import json

JOURNALS = ["IEEE Transactions on Automatic Control",
            "IEEE Transactions on Circuits and Systems I:Regular Papers",
            "IEEE Transactions on Circuits and Systems II:Express Briefs",
            "IEEE Transactions on Control of Network Systems",
            "IEEE Transactions on Cybernetics",
            "IEEE Transactions on Fuzzy Systems",
            "IEEE Transactions on Industrial Electronics",
            "IEEE Transactions on Industrial Informatics",
            "IEEE Transactions on Intelligent Transportation Systems",
            "IEEE Transactions on Neural Networks and Learning Systems",
            "IEEE Transactions on Robotics",
            "IEEE Transactions on Signal Processing",
            "IEEE Transactions on Sustainable Energy",
            "IEEE Transactions on Systems, Man, and Cybernetics:Systems",
            "IEEE TRANSACTIONS ON SYSTEMS MAN CYBERNETICS-SYSTEMS",
            "Automatica",
            "Nature",
            "Nature Communications",
            "Nature Physics",
            ]


def parse_bibtex(fileName):
    title_journal = {}
    journal_number = {}
    with open(fileName, encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    cites = bib_database.entries

    for paper in cites:
        if "title" in paper:
            title = paper["title"].replace("{textendash}", "-")
        elif "Title" in paper:
            title = paper["Title"].replace("{textendash}", "-")

        if "journal" in paper:
            journal = paper["journal"]
            # print("journal:" + journal)
        elif "Journal" in paper:
            journal = paper["Journal"]
        elif (("booktitle" or "Booktitle") in paper):
            booktitle = paper["booktitle"]
            continue
            # print("booktitle:" + booktitle)
        title_journal[title] = journal
        # print("title:" + title + "\n" + "=====================")
        # 不是会议的话
        # sub_str为引用中的论文所属期刊
        sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", journal).lower()
        for pub_name in JOURNALS:
            if sub_str == re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", pub_name).lower():
                print(title, "\n", journal, "\n", sub_str)
                print("===============")
                journal_number[pub_name] = journal_number.setdefault(pub_name, 0) + 1

    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())

    pub_path = '.\\pubs\\'

    if os.path.exists(pub_path) == False:
        os.mkdir(pub_path)

    with open(pub_path + fileName[:-4] + "_" + now_time + '_pub.json', 'w') as f:
        json.dump(journal_number, f)

    # with open('title_journal.json', 'w') as f:
    #     json.dump(title_journal, f)



if __name__ == '__main__':
    print('程序自身在运行')
    fileNames = ["paper_15.bib", "paper_30.bib"]
    for file in fileNames:
        parse_bibtex(file)

else:
    print('我来自另一模块')
