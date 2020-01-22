# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from AnalizeWords import AnalizeWords
from konlpy.tag import Kkma
from konlpy.utils import pprint


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
< naver 뉴스 전문 가져오기 >_select 사용
- 네이버 뉴스만 가져와서 결과값 조금 작음 
- 결과 메모장 저장 -> 엑셀로 저장 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
result={}


#내용 정제화 함수
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                      str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                       first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    #print(contents_text)


def crawler(query):
    currnet_searching_page = 1
    have_more_page_to_search = True
    # today_yy_mm_dd = datetime.today().strftime("%Y.%m.%d")
    today_yy_mm_dd = '2020.01.22'

    analizeWords = AnalizeWords()

    while have_more_page_to_search:
        url = "https://search.naver.com/search.naver?&where=news&query=" + query + "&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds=" + today_yy_mm_dd + "&de=" + today_yy_mm_dd + "&mynews=0&start=" + str(currnet_searching_page) + "&refresh_start=0"

        req = requests.get(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')

        # <a>태그에서 제목과 링크주소 추출
        atags = soup.select('._sp_each_title')
        for atag in atags:
            title_text.append(atag.text)  # 제목
            link_text.append(atag['href'])  # 링크주소
            print('title: ', atag.text)
            print('link: ', atag['href'])
            # analizeWords.test(atag.text)

            kkma = Kkma()
            pprint(kkma.sentences(atag.text))

        # 본문요약본
        contents_lists = soup.select('ul.type01 dl')
        for contents_list in contents_lists:
            # print('==='*40)
            print(contents_list.text)
            contents_cleansing(contents_list)  # 본문요약 정제화

        for page in soup.select(".paging"):
            print('page: ', page.text)
            if "다음페이지" in page.text:
                print('currnet page: ', page)
                currnet_searching_page = currnet_searching_page + 10
            else:
                have_more_page_to_search = False

        noresult = soup.select('.noresult_tab')

        if noresult:
            print('no result')
            break



def main():
    query = input("검색어 입력: ")
    crawler(query)  # 검색된 네이버뉴스의 기사내용을 크롤링합니다.


main()
