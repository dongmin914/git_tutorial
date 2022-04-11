
from selenium import webdriver  # 셀레니움
from bs4 import BeautifulSoup  # HTML 태그 가져오기
import time
import sys
import os
import requests
import json
from collections import OrderedDict


host = "https://www.lge.co.kr"
json_data = OrderedDict()

json_data['recommend_list'] = [];

def GetImg(model, img):
    dir = "./img"

    if not os.path.exists(dir):
        os.makedirs(dir)

    urllib.request.urlretrieve(img, dir + "/" + model + ".png")

    f = open("./img.txt", 'a')
    f.write(model+" : "+img+"\n")
    f.close()

    return  "img/" + model + ".png"

def GetURL(_URL):
    URL = _URL.split(",")[1]
    URL = URL.split("')")[0]
    URL = URL.split("'")[1]
    return host+URL

# 웹드라이버 실행 경로 chromedriver는 폴더가 아니라 파일명입니다.
driver = webdriver.Chrome("./chromedriver")

# LG 전자 이동
driver.get('https://www.lge.co.kr/lgekor/main.do')

page_source = driver.page_source
html = BeautifulSoup(page_source, 'html.parser')

count = 0;
menu = html.select('.gnb-main > .gnb-list > li')

for i in menu:

    menu_name = i.select_one('a').get_text()

    if menu_name == "TV/AV" or menu_name == "PC/모니터" or menu_name == "주방가전" or menu_name == "생활가전" or menu_name == "에어컨/에어케어" or menu_name == "모바일" or menu_name == "뷰티/의료기기":
    # if menu_name == "뷰티/의료기기":

        sub_menu = i.select(".gnb-depth2 .unit .no-sibling")

        for j in sub_menu:
            sub_menu_name = j.get_text()
            url = j.attrs['href']

            item_main = []
            model = []

            p_num = 1
            if sub_menu_name == "케어용품":
                p_num = 2

            # if sub_menu_name != "의료기기":
            #     continue
            if sub_menu_name == "청소기" or sub_menu_name == "LG 페이" or sub_menu_name == "빌트인가전" or sub_menu_name == "시그니처 키친 스위트":
                continue
            elif "코드제로" in sub_menu_name or "컨텐츠" in sub_menu_name:
                continue

            driver.get(url)
            html = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(1)

            # 베스트 상품 INPUT
            # best = html.select(".best-box ul li")
            #
            # if len(best) > 0:
            #     for a in best:
            #         item_name = a.select(".item-exp p")[p_num-1].get_text().strip()
            #         item_model = a.select(".item-exp p")[p_num].get_text().replace("/", "_")
            #         item_url = host + a.select_one("a").attrs['href']
            #         item_img = a.select(".item-info .imgbox img")[0].attrs['src']
            #
            #         if item_model not in model:
            #             model.append(item_model)
            #
            #             img_url = GetImg(item_model, item_img)
            #
            #             item_main.append({"name" : item_name, "model" : item_model, "url" : item_url, "img" : img_url})

            # 모든 상품 INPUT
            cate = html.select(".category-info .tg-cont li")

            if len(cate) > 1:
                for k in cate:
                    if sub_menu_name == "의료기기":

                        item_name = k.select("strong")[0].get_text().strip()
                        item_model = k.select("strong .small")[0].get_text().replace("/", "_")
                        item_name = item_name.replace(item_model, "").strip()
                        item_url = k.select_one("a").attrs['href']
                        item_img = host + k.select(".thumb img")[0].attrs['src']

                        if item_model not in model:
                            model.append(item_model)

                            img_url = GetImg(item_model, item_img)

                            item_main.append({"name" : item_name, "model" : item_model, "url" : item_url, "img" : img_url})

                    else:
                        while True:

                            try:
                                __URL = k.select_one('a').attrs['href']
                                if "www" in __URL:
                                    __URL = __URL
                                else:
                                    __URL = host+__URL
                                driver.get(__URL)
                                time.sleep(1)

                                html = BeautifulSoup(driver.page_source, 'html.parser')

                                if sub_menu_name == "스마트폰":

                                    list = html.select(".prdlist-opt .onW li input")
                                    _n = 0

                                    if len(list) > 1 :
                                        for _l in list:
                                            _n += 1

                                            if _n == 1 :
                                                continue

                                            while True:

                                                try:
                                                    time.sleep(3)

                                                    if _n > 5:
                                                        driver.execute_script("document.getElementsByClassName('jspContainer')[0].scrollTo(0, document.body.scrollHeight);")

                                                    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/section[2]/section[1]/ul/li[1]/ul/div/div[1]/li['+str(_n)+']/label').click()

                                                    time.sleep(3)

                                                    html = BeautifulSoup(driver.page_source, 'html.parser')

                                                    item = html.select(".item")

                                                    for l in item:
                                                        item_name = l.select(".item-exp p")[p_num-1].get_text().strip()
                                                        item_model = l.select(".item-exp p")[p_num].get_text().replace("/", "_")
                                                        item_url = GetURL(l.select_one("a").attrs['onclick'])
                                                        item_img = l.select(".item-info .imgbox img")[0].attrs['src']

                                                        if item_model not in model:
                                                            model.append(item_model)

                                                            img_url = GetImg(item_model, item_img)

                                                            item_main.append({"name" : item_name, "model" : item_model, "url" : item_url, "img" : img_url})
                                                    break
                                                except Exception as e:
                                                    driver.refresh()
                                                    print("ERROR RETRY {0}".format(sub_menu_name))

                                elif sub_menu_name == "전기레인지" or sub_menu_name == "뷰티 디바이스":

                                    list = html.select(".prdlist-opt .onW li input")
                                    _n = 0

                                    if len(list) > 1 :
                                        for _l in list:
                                            _n += 1

                                            while True:

                                                try:
                                                    time.sleep(3)

                                                    if _n > 5:
                                                        driver.execute_script("document.getElementsByClassName('jspContainer')[0].scrollTo(0, document.body.scrollHeight);")

                                                    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/section[2]/section[1]/ul/li[1]/ul/div/div[1]/li['+str(_n)+']/label').click()

                                                    time.sleep(3)

                                                    html = BeautifulSoup(driver.page_source, 'html.parser')

                                                    item = html.select(".item")

                                                    for l in item:
                                                        item_name = l.select(".item-exp p")[p_num-1].get_text().strip()
                                                        item_model = l.select(".item-exp p")[p_num].get_text().replace("/", "_")
                                                        item_url = GetURL(l.select_one("a").attrs['onclick'])
                                                        item_img = l.select(".item-info .imgbox img")[0].attrs['src']

                                                        if item_model not in model:
                                                            model.append(item_model)

                                                            img_url = GetImg(item_model, item_img)

                                                            item_main.append({"name" : item_name, "model" : item_model, "url" : item_url, "img" : img_url})
                                                    break
                                                except Exception as e:
                                                    driver.refresh()
                                                    print("ERROR RETRY {0}".format(sub_menu_name))

                                else:
                                    item = html.select(".item")
                                    for l in item:
                                        item_name = l.select(".item-exp p")[p_num-1].get_text().strip()
                                        item_model = l.select(".item-exp p")[p_num].get_text().replace("/", "_")
                                        item_url = GetURL(l.select_one("a").attrs['onclick'])
                                        item_img = l.select(".item-info .imgbox img")[0].attrs['src']

                                        if item_model not in model:
                                            model.append(item_model)

                                            img_url = GetImg(item_model, item_img)

                                            item_main.append({"name" : item_name, "model" : item_model, "url" : item_url, "img" : img_url})
                                break
                            except Exception as e:
                                driver.refresh()
                                print("ERROR RETRY {0}".format(sub_menu_name))

                        if sub_menu_name == "스마트폰" or sub_menu_name == "전기레인지" or sub_menu_name == "뷰티 디바이스":
                            break
            else:
                list = html.select(".prdlist-opt .onW li input")
                _n = 0

                if len(list) > 1 :
                    for _l in list:
                        _n += 1

                        while True:

                            try:
                                time.sleep(3)

                                if _n > 5:
                                    driver.execute_script("document.getElementsByClassName('jspContainer')[0].scrollTo(0, document.body.scrollHeight);")

                                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/section[2]/section[1]/ul/li[1]/ul/div/div[1]/li['+str(_n)+']/label').click()

                                time.sleep(3)

                                html = BeautifulSoup(driver.page_source, 'html.parser')

                                item = html.select(".item")

                                for l in item:
                                    item_name = l.select(".item-exp p")[p_num-1].get_text().strip()
                                    item_model = l.select(".item-exp p")[p_num].get_text().replace("/", "_")
                                    item_url = GetURL(l.select_one("a").attrs['onclick'])
                                    item_img = l.select(".item-info .imgbox img")[0].attrs['src']

                                    if item_model not in model:
                                        model.append(item_model)

                                        img_url = GetImg(item_model, item_img)

                                        item_main.append({"name" : item_name, "model" : item_model, "url" : item_url, "img" : img_url})
                                break
                            except Exception as e:
                                driver.refresh()
                                print("ERROR RETRY {0}".format(sub_menu_name))
                else:
                    item = html.select(".item")
                    for l in item:
                        item_name = l.select(".item-exp p")[p_num-1].get_text().strip()
                        item_model = l.select(".item-exp p")[p_num].get_text().replace("/", "_")
                        item_url = GetURL(l.select_one("a").attrs['onclick'])
                        item_img = l.select(".item-info .imgbox img")[0].attrs['src']

                        if item_model not in model:
                            model.append(item_model)

                            img_url = GetImg(item_model, item_img)

                            item_main.append({"name" : item_name, "model" : item_model, "url" : item_url, "img" : img_url})


            if item_main != []:
                json_data['recommend_list'].append(item_main)

            count += len(item_main)
            print(sub_menu_name + str(len(item_main)))

    print("\n")

f = open("./data/data.json", 'w', encoding='UTF-8-sig')
f.write(json.dumps(json_data, ensure_ascii=False, indent="\t"))
f.close()

f = open("./data/data-back.json", 'w', encoding='UTF-8-sig')
f.write(str(json_data))
f.close()

# print(json.dumps(json_data, ensure_ascii = False, indent="\t"))
print("Total : {0}".format(count))
print("success")
driver.quit()
sys.exit()
