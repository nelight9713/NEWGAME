import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium.webdriver.common.by import By

# Chrome 드라이버 옵션 설정
options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ['enable-logging'])

# 파일명에서 사용할 수 없는 문자 목록
invalid_chars = r'\/:*?"<>|'

# 파일명에서 특수문자를 제거하는 함수
def clean_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

# 이미지 저장 함수
def save_image(driver, img_xpath, img_suffix, category, title):
    try:
        img_url = driver.find_element(By.XPATH, img_xpath).get_attribute('src')
        img_path = rf"C:\Users\Koo\kdty\img\{category}!{title}{img_suffix}.jpg"
        r = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with open(img_path, 'wb') as outfile:
            outfile.write(r.content)
            print(f'{title} {img_suffix} 이미지 저장 완료')
    except Exception as e:
        print(f'{img_suffix} 이미지 저장에 실패하였습니다. 에러: {e}')

# 수집할 URL 리스트
urls = [
    'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1640962800000&mkt=all&ct=kr&rc=free',
    'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1649948400000&mkt=all&ct=kr&rc=free',
    'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1656601200000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1669820400000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1672498800000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1680274800000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1688137200000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1696431600000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1706799600000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1716303600000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1708959600000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1577804400000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1585666800000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1593529200000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1601478000000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1609426800000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1619103600000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1627657200000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1627657200000&mkt=all&ct=kr&rc=free',
'https://game.mobileindex.com/chart/day?tag=tc1061&pm=date&sd=1638003200000&mkt=all&ct=kr&rc=free'
]

# 데이터 저장용 리스트 초기화
title_lst = []
appUrl_lst = []
company_lst = []
gcategory_lst = []
dcategory_lst = []
description_lst = []
comment_rank_lst = []
comment_rank_num_lst = []

for url in urls:
    # Chrome 드라이버 초기화
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # URL 열기
    driver.get(url)
    time.sleep(3)

    # 더 많은 콘텐츠 로드를 위한 클릭 이벤트
    driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/section/section/div/div/div[2]').click()
    time.sleep(2)

    # 모든 콘텐츠 요소 찾기
    all_contents = driver.find_elements(By.XPATH, '//*[@id="content"]/div[2]/div[3]/section/section/div/div/div[1]/div[2]/div/span')
    print(f'발견된 콘텐츠 수: {len(all_contents)}')

    # 제목 추출 및 데이터 수집
    for content in all_contents:
        try:
            # 앱 이름 
            title = content.find_element(By.XPATH, './/span/span[2]/span[1]/span').text
            title = clean_filename(title)
            print(f'글 제목: {title}')

            # 앱 상세로 이동
            content.find_element(By.XPATH, './/span[1]/span').click()
            time.sleep(3)

            # 앱 URL 복사
            appUrl = driver.current_url
            print(f'URL: {appUrl}')

            # 게임 회사
            company = content.find_element(By.XPATH, './/span/span[2]/span[2]/span').text
            print(f'회사 이름: {company}')

            # 구글플레이 카테고리
            try:
                gcategory = content.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/span').text
                print(f'GoogleCategory: {gcategory}')
            except Exception as e:
                print(f'데이터 추출 중 오류 발생: {e}')
                gcategory = None

            # 상세 카테고리 (없으면 넘어감)
            try:
                dcategory = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[2]/div[2]/div[1]/div/div[2]/div[2]').text
                dcategory = dcategory.replace('/', '-')
                print(f'DetailedCategory: {dcategory}')
            except Exception as e:
                print(f'데이터 추출 중 오류 발생: {e}, 상세카데고리 오류')
                dcategory = None

            # 설명 가져오기
            try:
                description = content.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div').text
                print(f'설명: {description}')
            except Exception as e:
                print(f'데이터 추출 중 오류 발생: {e}')
                description = None

            # 별점 추출
            try:
                comment_rank = content.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/div/label/span').text
                print(f'별점 : {comment_rank}')
                comment_rank_num = content.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/p/span').text
                print(f'평가인 수 : {comment_rank_num}')
            except Exception as e:
                print(f'데이터 추출 중 오류 발생: {e}')
                comment_rank = None
                comment_rank_num = None

            # 앱 내부 첫 이미지 저장
            if dcategory:
                save_image(driver, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/img[1]', '(1)', dcategory, title)
            else:
                save_image(driver, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/img[1]', '(1)', gcategory, title)

            # 앱 내부 두번째 이미지 저장
            if dcategory:
                save_image(driver, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/img[2]', '(2)', dcategory, title)
            else:
                save_image(driver, '//*[@id="content"]/div[4]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/img[2]', '(2)', gcategory, title)

            # 뒤로가기
            driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/div[1]/span').click()
            time.sleep(1)

            # 리스트에 데이터 추가
            title_lst.append(title)
            appUrl_lst.append(appUrl)
            company_lst.append(company)
            gcategory_lst.append(gcategory)
            dcategory_lst.append(dcategory)
            description_lst.append(description)
            comment_rank_lst.append(comment_rank)
            comment_rank_num_lst.append(comment_rank_num)

        except Exception as e:
            print(f'데이터 추출 중 오류 발생: {e}')

    # 드라이버 종료
    driver.quit()

# 각 리스트의 길이를 가장 긴 리스트의 길이로 맞춤
max_length = max(len(lst) for lst in [title_lst, appUrl_lst, company_lst, gcategory_lst, dcategory_lst, description_lst, comment_rank_lst, comment_rank_num_lst])

for lst in [title_lst, appUrl_lst, company_lst, gcategory_lst, dcategory_lst, description_lst, comment_rank_lst, comment_rank_num_lst]:
    while len(lst) < max_length:
        lst.append(None)

# 데이터프레임 생성 및 CSV로 저장
app_dict = {
    'title': title_lst, 
    'appUrl': appUrl_lst, 
    'company': company_lst, 
    'gcategory': gcategory_lst, 
    'dcategory': dcategory_lst, 
    'description': description_lst, 
    'comment_rank': comment_rank_lst, 
    'comment_rank_num': comment_rank_num_lst
}
app_df = pd.DataFrame(app_dict)
print(f'총 수집한 어플 수: {app_df.shape[0]}')

file_name = 'app_df.csv'
app_df.to_csv(file_name, index=False, encoding='utf-8-sig')