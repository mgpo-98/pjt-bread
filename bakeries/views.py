from bs4 import BeautifulSoup
import requests
import re
from django.shortcuts import render
from reviews.models import Review

# keyword = request.GET.get('keyword')

# 지역별 빵집
def shops_by_region(request, region_name):
  base_url = 'https://www.siksinhot.com/search?keywords=' # 식신페이지
  keyword = f'{region_name} 빵집' # 검색어
  search_url = base_url + keyword # 식신페이지 + 검색어
  r = requests.get(search_url) # 페이지에 요청하기
  soup = BeautifulSoup(r.text, "html.parser") # 요청한 데이터 텍스트로 불러오기

  store_DB = [] # 한 페이지 내 모든 가게의 데이터
  '''
  [
    {
      'store_name': 식당이름,
      'store_score': 평점,
      'store_img': 썸네일,
      'store_region': 위치정보,
      'store_category': 가게 업종,   
      'store_id': 가게 url,
      'review_cnt': 식당에 달린 리뷰 개수,
    }
  ]
  '''
  
  store_name = soup.select(".textBox > h2") # 식당 이름
  store_score = soup.select(".textBox > span") # 식당 평점
  store_img = soup.select("figure > a > img") # 식당 이미지 주소
  store_region = soup.select('.cate > a') # 식당 간단정보(지역+업종)
  store_id = soup.select('figure > a') # 식당 url

  # 식당 이미지 주소 정제
  store_img_rst = []
  for store in store_img:
      if store['alt'] != 'best':
          store_img_rst.append(store)

  # 가게의 id 알아내기 위한 정규 표현식
  # 예) https://www.siksinhot.com/P/329263 에서 '329263'만 뽑아냄
  p = re.compile('[0-9]+')

  for i in range(0, len(store_name)):
      store_data = {}
      if store_region[2 * i + 1].text in ['베이커리/제과점', '카페/커피숍', '샌드위치', '브런치']:
        store_data['store_name'] = store_name[i].text
        store_data['store_score'] = store_score[i].text
        store_data['store_img'] = store_img_rst[i]['src']
        store_data['store_region'] = store_region[i * 2].text
        store_data['store_category'] = store_region[2 * i + 1].text

        store_id_rst = p.search(store_id[i]['href']).group()
        store_data['store_id'] = store_id_rst
        store_data['review_cnt'] = Review.objects.filter(shop_id=int(store_id_rst)).count
        
        store_DB.append(store_data)

  context = {
      'store_DB': store_DB,
      'region_name': region_name,
  }

  return render(request, 'bakeries/shop_list.html', context)

# 빵 종류별 빵집
def shops_by_bread(request, bread_name):
  base_url = 'https://www.siksinhot.com/search?keywords=' # 식신페이지
  keyword = f'{bread_name}' # 검색어
  search_url = base_url + keyword # 식신페이지 + 검색어
  r = requests.get(search_url) # 페이지에 요청하기
  soup = BeautifulSoup(r.text, "html.parser") # 요청한 데이터 텍스트로 불러오기

  store_DB = [] # 한 페이지 내 모든 가게의 데이터
  '''
  [
    {
      'store_name': 식당이름,
      'store_score': 평점,
      'store_img': 썸네일,
      'store_region': 위치정보,
      'store_category': 가게 업종,   
      'store_id': 가게 url,
      'review_cnt': 식당에 달린 리뷰 개수,
    }
  ]
  '''

  store_name = soup.select(".textBox > h2") # 식당 이름
  store_score = soup.select(".textBox > span") # 식당 평점
  store_img = soup.select("figure > a > img") # 식당 이미지 주소
  store_region = soup.select('.cate > a') # 식당 간단정보
  store_id = soup.select('figure > a') # 식당 url

  # 식당 이미지 주소 정제
  store_img_rst = []
  for store in store_img:
      if store['alt'] != 'best':
          store_img_rst.append(store)

  # 가게의 id 알아내기 위한 정규 표현식
  # 예) https://www.siksinhot.com/P/329263 에서 '329263'만 뽑아냄
  p = re.compile('[0-9]+')

  for i in range(0, len(store_name)):
      store_data = {}
      if store_region[2 * i + 1].text in ['베이커리/제과점', '카페/커피숍', '샌드위치', '브런치']:
        store_data['store_name'] = store_name[i].text
        store_data['store_score'] = store_score[i].text
        store_data['store_img'] = store_img_rst[i]['src']
        store_data['store_region'] = store_region[i * 2].text
        store_data['store_category'] = store_region[2 * i + 1].text
        
        store_id_rst = p.search(store_id[i]['href']).group()
        store_data['store_id'] = store_id_rst
        store_data['review_cnt'] = Review.objects.filter(shop_id=int(store_id_rst)).count

        store_DB.append(store_data)

  context = {
      'store_DB': store_DB,
      'bread_name': bread_name,
  }

  return render(request, 'bakeries/shop_list.html', context)

# 특정 빵집의 홈 상세 정보 조회
def shop_home(request, shop_id):
  base_url = 'https://www.siksinhot.com/P/' # 식신페이지
  keyword = f'{shop_id}' # 검색어
  search_url = base_url + keyword # 식신페이지 + 검색어
  r = requests.get(search_url) # 페이지에 요청하기
  soup = BeautifulSoup(r.text, "html.parser") # 요청한 데이터 텍스트로 불러오기

  store_data = dict() # 식신 사이트 가게 상세 페이지 내 특정 한 가게의 데이터
  '''
  {    ------------------- 총 15개 데이터 -------------------------
      'store_name': 식당이름,                            => 베이스
      'store_score': 평점,                               => 베이스
      'store_brief_intro': 가게 간단 소개,               => 베이스
      'store_intro': 가게 소개,                          => 상세
      'store_imgs': 가게 사진들,                         => 베이스
      'store_category': 가게 업종,                       => 베이스
      'store_address': 가게 주소,                        => 홈, 상세
      'store_way_to_come': 가게 오시는길,                => 상세
      'store_operating_time': 가게 영업 시간,            => 상세
      'store_today_operating_time': 오늘 매장 영업 시간, => 홈
      'store_phone_number': 가게 전화번호,               => 상세
      'store_facility_detail': 가게 편의 시설 정보,      => 홈
      'store_main_menu': 가게 대표메뉴,                  => 홈, 메뉴
      'store_drinks': 가게 음료/주류,                    => 메뉴
      'store_homepage': 가게 홈페이지,                   => 상세
  }
  '''

  # 1) 식당이름, 2) 식당평점
  store_name_score = soup.select_one(".store_name_score > h3") # 식당 이름 + 평점
  store_name_score_texts = list(store_name_score.stripped_strings)
  store_name = store_name_score_texts[0] # 식당 이름
  store_score = store_name_score_texts[1] # 식당 평점

  store_data['store_name'] = store_name
  store_data['store_score'] = store_score

  # 3) 가게 간단 소개
  store_brief_intro = soup.select_one(".store_name_score > p")
  store_data['store_brief_intro'] = store_brief_intro.get_text()

  # 4) 가게 사진들
  store_imgs = soup.select(".slick-track img")
  store_data['store_imgs'] = [img['src'] for img in store_imgs]

  # 이외 가게 상세 정보(11개)
  store_info_titles = soup.select(".store_info h4")

  for title in store_info_titles:
    title_text = title.get_text()
    if title_text == '업종':
        store_data['store_category'] = title.next_sibling.get_text()
    elif title_text == '매장소개':
        store_data['store_intro'] = title.next_sibling.get_text()
    elif title_text == '전화번호':
        store_data['store_phone_number'] = title.next_sibling.get_text()
    elif title_text == '주소':
      address = list(title.next_sibling.stripped_strings)
      if len(address) >=2:
        store_data['store_address'] = [text for text in address][:-1]
      else:
        store_data['store_address'] = [text for text in address]
    elif title_text == '오시는 길':
        store_data['store_way_to_come'] = title.next_sibling.get_text()
    elif title_text == 'TODAY':
        store_data['store_today_operating_time'] = [text for text in title.next_sibling.stripped_strings]
    elif title_text == '영업시간':
        operating_time = [text for text in title.next_sibling.stripped_strings]
        operating_time_rst = []
        for i in range(0, len(operating_time), 2):
            operating_time_rst.append(operating_time[i:i + 2])
        store_data['store_operating_time'] = operating_time_rst
    elif title_text == '편의/시설 정보':
        p = re.compile('\([a-zA-Z]*\)|\(|\)|,|원')

        store_data['store_facility_detail'] = [text for text in title.next_sibling.stripped_strings if not p.search(text)]
        if title.next_sibling.next_sibling:
          store_data['store_facility_detail'].extend([re.sub(r'\s+', '', text) for text in title.next_sibling.next_sibling.stripped_strings if not p.search(text)])
    elif title_text == '대표메뉴':
        menus = list(title.next_sibling.stripped_strings)
        store_main_menu = []
        for i in range(0, len(menus), 3):
            temp = [menus[i], menus[i + 1]]
            store_main_menu.append(temp)
        store_data['store_main_menu'] = store_main_menu 
    elif title_text == '음료/주류':
        store_data['store_drinks'] = title.next_sibling.get_text().split(', ')
    elif title_text == '매장 홈페이지':
        store_data['store_homepage'] = [text for text in title.next_sibling.stripped_strings if text not in [',']]

  context = {
    'store_data': store_data,
    'shop_id': shop_id,
    'reviews': Review.objects.filter(shop_id=shop_id),
  }

  return render(request, 'bakeries/shop_home.html', context)
