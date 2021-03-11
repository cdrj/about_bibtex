import os
import random
import re

import bibtexparser
import json
from bs4 import BeautifulSoup
import requests
import time


def list_authors(bibFile) -> list:
    all_authors = set()
    with open(bibFile, encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    cites = bib_database.entries
    for paper in cites:
        # paper["Author"] = paper["Author"].replace("and", ",")
        temp = paper["author"].split("and")
        authors = []
        for item in temp[:]:
            author_without_space = item.strip().replace('\n', '').replace('\r', '')
            authors.append(author_without_space)
            all_authors.add(author_without_space)

        title = paper["title"].replace("{textendash}", "-")

        if "journal" in paper:
            journal = paper["journal"]
            # print("journal:" + journal)
        elif "Journal" in paper:
            journal = paper["Journal"]
        elif (("booktitle" or "Booktitle") in paper):
            booktitle = paper["booktitle"]
            continue
            # print("booktitle:" + booktitle)
        for author in authors:
            print(author)

        print("title:" + title + "\n" + "=====================")

    list_of_authors = list(all_authors)

    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())

    authors_path=".\\authors\\"
    if os.path.exists(authors_path) == False:
        os.mkdir(authors_path)

    # 写入 JSON 数据
    with open(authors_path+ bibFile[:-4] + now_time + '.json', 'w') as f:
        json.dump(list_of_authors, f)

    # print(all_authors)
    return list_of_authors


def check_fellow_by_names(names, output):
    proxies = {
        'https': 'http://10.0.0.66:12333',
        'http': 'http://10.0.0.66:12333'
    }
    results = {}
    num_of_authors = len(names)
    index = 1
    fellows = []
    sum = 0
    for name in names:

        s = requests.session()
        s.keep_alive = False
        requests.DEFAULT_RETRIES = 5

        print("共有 {} 位作者,正在查找第 {} 位作者 {} ".format(num_of_authors, index, name))
        index += 1

        kv = {'keyword': name}

        # headers = {
        #     'User-Agent':
        #         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

        head = {
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&pvid=d4a3fce8a4e8424ba3a11de05bbdd443',
            'scheme': 'https',
            'referer': 'https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&wq=%E7%94%B5%E8%84%91&pvid=097a8dead9704f0d85ba224fce56c8c1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'Cookie': 'areaId=22; ipLoc-djd=22-1930-50947-0; PCSYCityID=CN_510000_510100_510107; shshshfpa=3c696b4b-4db5-8688-b7bf-53d8ef2639d1-1577169256; shshshfpb=3c696b4b-4db5-8688-b7bf-53d8ef2639d1-1577169256; xtest=7978.cf6b6759; unpl=V2_ZzNtbUVVRUVxDREGL0taBWJWGlkSVEcRIghGXSkdW1ViAEdbclRCFX0URldnGlgUZwAZWEBcQxdFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsaWgZvBRRVQFZzJXI4dmR9GFgHYAsiXHJWc1chVERUfR1dByoDEVtBX0UTfQpHZHopXw%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_637a54fcec714d95a255f118c56a42d7|1577248990400; qrsc=3; __jdu=1272977930; user-key=66522f02-f902-4764-8693-0eefdd7745bd; cn=0; __jda=122270672.1272977930.1577169251.1577257496.1577326776.5; __jdb=122270672.4.1272977930|5.1577326776; __jdc=122270672; shshshfp=7324c276d86c51251dbc81623c455052; shshshsID=febb1869dc62c6b7318e4bec8bb1e058_4_1577326815219; rkv=V0700; 3AB9D23F7A4B3C9B=WNBES7CO6JKYVHCHPD7S6VLV7PWVDFBTPTRJ4M6VCTBXXQAQWP2OXRZ6O4TNGNQCNETV57IOKIGZSUWHGMX32TMH2Y'

        }
        url = "http://services27.ieee.org/fellowsdirectory/keywordsearch.html"

        r = requests.get(url, params=kv, proxies=proxies, headers=head)
        page_text = r.text

        soup = BeautifulSoup(page_text, 'lxml')
        # print(soup.find(id="mobile-result-list"))
        result = soup.find(class_="returned_line col-xs-12 visible-xs")

        if (result):
            result_num = int(result.p.i.b.contents[0])
            name_on_page = soup.find(class_="loc_n_name col-xs-12").p.a.span.contents[0]
            temp = ""
            first_name_on_page = temp.join(name_on_page)  # Cao, Jinde

            print("找到结果数量：", result_num)
            print("网页上的名字是：", first_name_on_page)
            print("名单上的名字是：", name)
            if (result_num == 1):
                results[name] = [first_name_on_page, result_num]
                # 判断是否和name相同，需要对name去除特殊字符
                if re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "",
                          first_name_on_page).lower() == re.sub(
                    u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "",
                    name).lower():
                    sum += 1
                    # print("{} 位作者名字相同!".format(sum))
                    # results.append(first_name_on_page)
                    fellows.append(name)

            time.sleep(5)
        else:
            print("找不到结果")

        print("{} 位作者名字相同!".format(sum))
        print("==============")

    num = len(fellows)
    print("共有{} 位作者应该是fellow!他们的名字是：".format(num))
    for fellow in fellows:
        print(fellow)
    print("=======================")

    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())

    fellow_path = ".\\fellows\\"
    if os.path.exists(fellow_path) == False:
        os.mkdir(fellow_path)

    output=output[:-4]
    with open(fellow_path + output + now_time + '_fellows.json', 'w') as f:
        json.dump(fellows, f)

    with open(fellow_path + output + now_time + '_cands.json', 'w') as f:
        json.dump(results, f)

    return fellows


# fileName = "39cites.bib"
# names = list_authors(fileName)
#
# print(names)

if __name__ == '__main__':
    print('程序自身在运行')
    fileNames = ["paper_15.bib", "paper_30.bib"]
    for file in fileNames:
        check_fellow_by_names(list_authors(file), file)
else:
    print('我来自另一模块')
