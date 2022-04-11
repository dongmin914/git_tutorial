from selenium import webdriver  # 셀레니움
from bs4 import BeautifulSoup  # HTML 태그 가져오기
import time
import sys
import os
import urllib.request
import json
from collections import OrderedDict

# 접속할 HOST 설정
host = "https://www.lge.co.kr"

# 결과 JSON 객체
json_data = OrderedDict()
json_data['recommend_list'] = [];


# 이미지 저장 함수
def GetImg(model, img):
    dir = "./img"

    if not os.path.exists(dir):
        os.makedirs(dir)

    urllib.request.urlretrieve(img, dir + "/" + model + ".png")

    # f = open("./img.txt", 'a')
    # f.write(model + " : " + img + "\n")
    # f.close()

    return "img/" + model + ".png"


if __name__ == '__main__':

    # 웹드라이버 실행 경로 chromedriver는 폴더가 아니라 파일명입니다.
    driver = webdriver.Chrome("./chromedriver")

    # LG 전자 이동
    driver.get(host)

    # LG 전자 HTML 가져오기
    page_source = driver.page_source
    html = BeautifulSoup(page_source, 'html.parser')

    menu = html.select('.nav-inner > .nav > .nav-category > .nav-category-container > ul > li')
    for i in menu:
        # 메뉴명
        L_category = i.select_one('.super-category-item').get_text()

        if L_category not in ('TV/AV', 'IT', '주방가전', '생활가전', '에어컨/에어케어', '뷰티/의료기기'):
        # if L_category not in ('주방가전', '에어컨/에어케어', '뷰티/의료기기'):
            continue
        print(L_category)

        sub_menu = i.select(".category .category-item")
        for sub in sub_menu:
            item_Array = []

            # 서브 메뉴명
            M_category = sub.get_text()

            if M_category in ("케어용품/소모품", "빌트인가전", "시그니처 키친 스위트"):
                continue

            href = sub.attrs['href']
            M_category_en = href.replace("https://www.lge.co.kr/", "")

            print("     " + M_category + "(" + M_category_en + ")")
            print("     " + href)

            driver.get(href)
            driver.implicitly_wait(10)

            # 맥주 제조기인 경우 19세 동의 클릭
            if M_category in ("맥주제조기"):
                driver.find_element_by_class_name('bd-black').click()
                time.sleep(2)

            # 제품 더보기가 있는 경우 클릭
            while True:
                if driver.find_element_by_class_name('read-more').get_attribute("style") != "display: none;":
                    driver.find_element_by_class_name('read-more').click()
                else:
                    break
                time.sleep(0.5)

            _html = BeautifulSoup(driver.page_source, 'html.parser')
            item_list = _html.select('.plp-item')

            for item in item_list:
                modelObject = json.loads(item.attrs['data-ec-product'])

                model_name = modelObject.get("model_name")
                model_number = modelObject.get("model_sku")

                main_category = M_category
                sub_category = ""
                category = modelObject.get("category").split('/')[-1]
                if M_category.find("/") != -1:
                    if M_category in "일체형/데스크톱":
                        if category in "데스크톱":
                            main_category = "데스크톱"
                            sub_category = "일체형 PC"
                        else:
                            main_category = "일체형 PC"
                            sub_category = "데스크톱"
                    else:
                        sub_category = main_category.replace("/", "")
                        sub_category = sub_category.replace(category, "")
                        main_category = category
                if M_category in "청소기":
                    if category in "싸이킹":
                        main_category = "유선청소기"
                        sub_category = "무선청소기"
                    else:
                        main_category = "무선청소기"
                        sub_category = "유선청소기"


                url = host + item.select_one('.slide-conts > a').attrs['href']

                if "src" not in item.select_one('.slide-conts > a > img').attrs:
                    continue

                img_url = host + item.select_one('.slide-conts > a > img').attrs['src']
                img_path = GetImg(model_number, img_url)

                item_Array.append({"name": model_name, "model": model_number, "url": url, "img": img_path, "main_category": main_category, "sub_category": sub_category})

            if item_Array != []:
                json_data['recommend_list'].append(item_Array)

    f = open("./data/data.json", 'w', encoding='UTF-8-sig')
    f.write(json.dumps(json_data, ensure_ascii=False, indent="\t"))
    f.close()

    f = open("./data/data-back.json", 'w', encoding='UTF-8-sig')
    f.write(str(json_data))
    f.close()

    # print(json.dumps(json_data, ensure_ascii = False, indent="\t"))
    print("success")
    driver.quit()
    sys.exit()
