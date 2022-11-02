from bs4 import BeautifulSoup
import requests
import re
from django.shortcuts import render

# Create your views here.
# 지역별 빵집
def shops_by_region(request, region_name):
  # 식신페이지
  base_url = 'https://www.siksinhot.com/search?keywords='
  # 검색어
  # keyword = request.GET.get('keyword')
  keyword = f'{region_name} 빵집'
  # 식신페이지 + 검색어
  search_url = base_url + keyword
  # 페이지에 요청하기
  r = requests.get(search_url)
  # 요청한 데이터 텍스트로 불러오기
  soup = BeautifulSoup(r.text, "html.parser")

  # --------------------------------------------------------------
  # 한 페이지 내 모든 가게의 데이터
  store_DB = []
  '''
  [
    {
      'store_name': 식당이름,
      'store_score': 평점,
      'store_img': 썸네일,
      'store_region': 위치정보,
      'store_id': 가게 url,
    }
  ]
  '''

  # 식당 이름
  store_name = soup.select(".textBox > h2")
  # 식당 평점
  store_score = soup.select(".textBox > span")
  # 식당 이미지 주소
  store_img = soup.select("figure > a > img")
  # 식당 간단정보
  store_region = soup.select('.cate > a')
  # 식당 url
  store_id = soup.select('figure > a')

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
        store_data['store_id'] = p.search(store_id[i]['href']).group()
        
        store_DB.append(store_data)

  context = {
      'store_DB': store_DB,
  }

  return render(request, 'bakeries/shop_list.html', context)

# 빵 종류별 빵집
def shops_by_bread(request, bread_name):
  # 식신페이지
  base_url = 'https://www.siksinhot.com/search?keywords='
  # 검색어
  # keyword = request.GET.get('keyword')
  keyword = f'{bread_name}'
  # 식신페이지 + 검색어
  search_url = base_url + keyword
  # 페이지에 요청하기
  r = requests.get(search_url)
  # 요청한 데이터 텍스트로 불러오기
  soup = BeautifulSoup(r.text, "html.parser")

  # --------------------------------------------------------------
  # 한 페이지 내 모든 가게의 데이터
  store_DB = []
  '''
  [
    {
      'store_name': 식당이름,
      'store_score': 평점,
      'store_img': 썸네일,
      'store_region': 위치정보,
      'store_id': 가게 url,
    }
  ]
  '''

  # 식당 이름
  store_name = soup.select(".textBox > h2")
  # 식당 평점
  store_score = soup.select(".textBox > span")
  # 식당 이미지 주소
  store_img = soup.select("figure > a > img")
  # 식당 간단정보
  store_region = soup.select('.cate > a')
  # 식당 url
  store_id = soup.select('figure > a')

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
        store_data['store_id'] = p.search(store_id[i]['href']).group()
        
        store_DB.append(store_data)

  context = {
      'store_DB': store_DB,
  }

  return render(request, 'bakeries/shop_list.html', context)