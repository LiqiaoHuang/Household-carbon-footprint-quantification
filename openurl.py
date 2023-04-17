import urllib.request as urllib

import requests as rq
from bs4 import BeautifulSoup as bs
import re

url = "https://www.e-stat.go.jp/"
folder_path = "./dataset/"


def gethtml(rooturl, encoding="utf-8"):
    response = rq.get(rooturl)
    response.encoding = encoding
    html = response.text
    return html


def getherf(html):
    soup = bs(html, features="lxml")
    allnode_of_a = soup.find_all("a", class_="stat-item_child")
    result = [url + _.get("href") for _ in allnode_of_a]
    return result


html = gethtml(
    "https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200561&tstat=000000330001&cycle=1&tclass1=000000330001&tclass2=000000330004&tclass3=000000330005&tclass4val=0")
results = getherf(html)
excel_url_list = []
number = 0
for result in results:
    page = urllib.urlopen(result)
    contents = page.read()
    uls_new = []
    soup = bs(contents, "html.parser")
    uls = soup.find_all('ul', class_='stat-dataset_list-detail')
    index_list = []
    final_index = 0
    for ul in uls:
        lis = ul.find('li', class_='stat-dataset_list-detail-item stat-dataset_list-border-top')
        if lis is None:
            continue
        index_list.append(uls.index(ul))
        span = lis.find('span', class_='')
        if span.text == '4-1':
            final_index = uls.index(ul)
    next_index = index_list[index_list.index(final_index) + 1]

    uls_new = uls[final_index:next_index]
    # for ul in uls:
    #     lis = ul.find('li', class_='stat-dataset_list-detail-item stat-dataset_list-border-top')
    #     if lis is None:
    #         continue
    #     span = lis.find('span', class_='')
    #     if span.text == '4-1':
    #         start = uls.index(ul)
    #         print(start)
    #     if bool(re.search(r'\d', span.text)):
    #         end = uls.index(ul)
    #         print(end)
    #

    for ul in uls_new:
        download_url = ''
        lis = ul.find('li', class_='stat-dataset_list-detail-item stat-dataset_list-border-top')
        excel_url = ul.find('a', class_='stat-dl_icon stat-icon_0 stat-icon_format js-dl stat-download_icon_left')
        excel_url_list.append('https://www.e-stat.go.jp' + excel_url.get("href"))
        download_url = 'https://www.e-stat.go.jp' + excel_url.get("href")
        filepath = folder_path + str(number) + ".xlsx"
        f = rq.get(download_url)
        with open(filepath, 'wb') as code:
            code.write(f.content)
        number = number + 1


    print(excel_url_list)

# file = open('download_list.txt', 'w')
#
# file.write(str(excel_url_list))
#
# file.close()
