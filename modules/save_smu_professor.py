from bs4 import BeautifulSoup
import time
from selenium import webdriver
import urllib.request
import re
import pandas as pd
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import smu_professor
from multiprocessing import Pool

def parse_prof():
	#교양 교수님들 정보만 담을 리스트
	nm_name_list = [] #교수명
	nm_major_list = [] #계당교양교육원 교양 교수님들은 교양으로 모두 insert하고, 학과는 학과명으로 insert.
	nm_info_list = [] #교수정보
	nm_picture_list = [] #사진

	#학과 교수님들 정보만 담을 리스트
	name_list = [] #교수명
	major_list = [] #교수님이 속한 학과명으로 insert.
	info_list = [] #교수정보
	picture_list = [] #사진
	#크롬 연결
	driver = webdriver.Chrome('chromedriver')
	driver.implicitly_wait(3)
	#계당교양교육원 교양
	driver.get('https://www.smu.ac.kr/smgs/intro/professor.do?mode=list&&pagerLimit=50&pager.offset=0')
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	name = soup.select('#item_body > div.sub-container > div.content-wrap > div.prof-wrap.con-box > div > div > div > div > ul > li > div.texts > strong')
	info = soup.select('#item_body > div.sub-container > div.content-wrap > div.prof-wrap.con-box > div > div > div > div > ul > li > div.texts > ul')
	for n in name:
		nm_name_list.append(n.text.strip())
		#사이트에서뽑아온 교수님 이름만큼 '교양'이라고 삽입
		nm_major_list.append('계당교양교육원') 
	for n in info:
		nm_info_list.append(n.text.strip())
		
	# 사진 가져오기
	front_url = "https://www.smu.ac.kr"
	ul_tag = soup.find('ul', {'class', 'board-thumb-wrap2 col2'})

	picture = ul_tag.find_all('img', {'class', 'pImg'})
	for images in picture:
		nm_picture_list.append(front_url + images.get('src'))

	#intro = pd.DataFrame()
	#intro['학과/교양']= nm_major_list
	#intro['교수명']=nm_name_list
	#intro['교수정보']=nm_info_list
	#intro['사진정보']=nm_picture_list
	#intro.head(40)

	###총 31개 학과
	major_count=1
	while(True):
		if major_count == 30:  #총 31개 학과이나, 
			#국가안보학과와 융합경영학과는 웹페이지의 구조가 다르므로 따로 추출.
			#29개 학과만 정보추출하고, 30이 되면 빠져나온다.
			break
		#과마다 교수님 수가 20명이 넘어가면, 2페이지로 넘어가기때문에
		#교수소개 한 페이지안에 최대 50명의 교수님을 다 보여주도록 주소설정.
		#소속교수님이 최대 50명을 넘는 학과는 없다. 소속교수님이 가장 많은 학과 최대21명.
	#컴퓨터과학과 교수진
		if major_count==1 :
			driver.get('https://www.smu.ac.kr/cs/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#전기공학과 교수진
		if major_count==2 :
			driver.get('https://www.smu.ac.kr/electric/faculty/faculty.do?https://www.smu.ac.kr/cs/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#융합전자공학과 교수진
		if major_count==3 :
			driver.get('https://www.smu.ac.kr/electronic/faculty/faculty.do?https://www.smu.ac.kr/cs/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#휴먼지능정보공학과 교수진
		if major_count==4 :
			driver.get('https://www.smu.ac.kr/hi/faculty/faculty.do?https://www.smu.ac.kr/cs/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#경제금융학부 교수진
		if major_count==5 :
			driver.get('https://www.smu.ac.kr/economic/faculty/faculty.do?https://www.smu.ac.kr/cs/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#경영학부 교수진
		if major_count==6 :
			driver.get('https://www.smu.ac.kr/smubiz/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#글로벌경영학과 교수진
		if major_count==7 :
			driver.get('https://www.smu.ac.kr/newmajoritb/intro/faculty.do?https://www.smu.ac.kr/cs/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#생활예술학과 교수진
		if major_count==8 :
			driver.get('https://www.smu.ac.kr/smulad/faculity/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#국어교육과 교수진
		if major_count==9 :
			driver.get('https://www.smu.ac.kr/koredu/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#영어교육과 교수진
		if major_count==10 :
			driver.get('https://www.smu.ac.kr/engedu/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#교육학과 교수진
		if major_count==11 :
			driver.get('https://www.smu.ac.kr/peda/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#수학교육과 교수진
		if major_count==12 :
			driver.get('https://www.smu.ac.kr/mathedu/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#지적재산권학과 교수진
		if major_count==13 :
			driver.get('https://www.smu.ac.kr/cc/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#한일문화콘텐츠학과 교수진
		if major_count==14 :
			driver.get('https://www.smu.ac.kr/kjc/intro/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#역사콘텐츠학과 교수진
		if major_count==15 :
			driver.get('https://www.smu.ac.kr/history/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#문헌정보학과 교수진
		if major_count==16 :
			driver.get('https://www.smu.ac.kr/libinfo/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#공공인재학부 교수진
		if major_count==17 :
			driver.get('https://www.smu.ac.kr/public/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#음악학부 교수진
		if major_count==18 :
			driver.get('https://www.smu.ac.kr/music/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#공간환경학부 교수진
		if major_count==19 :
			driver.get('https://www.smu.ac.kr/space/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#가족복지학과 교수진
		if major_count==20 :
			driver.get('https://www.smu.ac.kr/smfamily/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#화학에너지공학과 교수진
		if major_count==21 :
			driver.get('https://www.smu.ac.kr/cee/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#생명공학과 교수진
		if major_count==22 :
			driver.get('https://www.smu.ac.kr/biotechnology/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#화공신소재학과 교수진
		if major_count==23 :
			driver.get('https://www.smu.ac.kr/ichemistry/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#게임학과 교수진
		if major_count==24 :
			driver.get('https://www.smu.ac.kr/game01/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#식품영양학과 교수진
		if major_count==25 :
			driver.get('https://www.smu.ac.kr/foodnutrition/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#의류학과 교수진
		if major_count==26 :
			driver.get('https://www.smu.ac.kr/clothing2/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#스포츠건강관리학과 교수진
		if major_count==27 :
			driver.get('https://www.smu.ac.kr/smpe/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#무용예술학과 교수진
		if major_count==28 :
			driver.get('https://www.smu.ac.kr/dance/intro/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#조형예술학과 교수진
		if major_count==29 :
			driver.get('https://www.smu.ac.kr/finearts/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')


		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		
		
		name = soup.select('#jwxe_main_content > div > div > div > div > ul > li > div.texts > strong')
		for n in name:
			name_list.append(n.text.strip())
			if major_count ==1 :
				major_list.append('컴퓨터과학과')
			if major_count ==2 :
				major_list.append('전기공학과')
			if major_count ==3 :
				major_list.append('융합전자공학과')
			if major_count ==4 :
				major_list.append('휴먼지능정보공학과')
			if major_count ==5 :
				major_list.append('경제금융학부')
			if major_count ==6 :
				major_list.append('경영학부')
			if major_count ==7 :
				major_list.append('글로벌경영학과')
			if major_count ==8 :
				major_list.append('생활예술학과')
			if major_count ==9 :
				major_list.append('국어교육과')
			if major_count ==10 :
				major_list.append('영어교육과')
			if major_count ==11 :
				major_list.append('교육학과')
			if major_count ==12 :
				major_list.append('수학교육과')
			if major_count ==13 :
				major_list.append('지적재산권학과')
			if major_count ==14 :
				major_list.append('한일문화콘텐츠학과')
			if major_count ==15 :
				major_list.append('역사콘텐츠학과')
			if major_count ==16 :
				major_list.append('문헌정보학과')
			if major_count ==17 :
				major_list.append('공공인재학부')
			if major_count ==18 :
				major_list.append('음악학부')
			if major_count ==19 :
				major_list.append('공간환경학부')
			if major_count ==20 :
				major_list.append('가족복지학과')
			if major_count ==21 :
				major_list.append('화학에너지공학과')
			if major_count ==22 :
				major_list.append('생명공학과')
			if major_count ==23 :
				major_list.append('화공신소재학과')
			if major_count ==24 :
				major_list.append('게임학과')
			if major_count ==25 :
				major_list.append('식품영양학과')
			if major_count ==26 :
				major_list.append('의류학과')
			if major_count ==27 :
				major_list.append('스포츠건강관리학과')
			if major_count ==28 :
				major_list.append('무용예술학과')
			if major_count ==29 :
				major_list.append('조형예술학과')

		#정보 가져오기
		info = soup.select('#jwxe_main_content > div > div > div > div > ul > li > div.texts > ul')
		for n in info:
			info_list.append(n.text.strip())
		
		# 사진 가져오기
		front_url = "https://www.smu.ac.kr" 
		ul_tag = soup.find('ul', {'class', 'board-thumb-wrap2 col2'})
		picture = ul_tag.find_all('img', {'class', 'pImg'})
		for images in picture:
			picture_list.append(front_url + images.get('src'))

		major_count+= 1


	#남은 두 학과(국가안보학과, 융합경영학과)도 추출 
	major_count=1

	while(True):
		if major_count == 3: 
			#국가안보학과와 융합경영학과는 웹페이지의 구조가 다르므로 따로 추출.
			#두 학과만 정보추출하고, 3이 되면 빠져나온다.
			break
	#국가안보학과 교수진
		if major_count==1 :
			driver.get('https://www.smu.ac.kr/sdms/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
	#융합경영학과 교수진
		if major_count==2 :
			driver.get('https://www.smu.ac.kr/cm/faculty/faculty.do?mode=list&&pagerLimit=50&pager.offset=0')
			
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
	  
		name = soup.select('#ko > div.common-board > div > ul > li > div.texts > strong')
		for n in name:
			name_list.append(n.text.strip())
			if major_count ==1 :
				major_list.append('국가안보학과')
			if major_count ==2 :
				major_list.append('융합경영학과')
		
		info = soup.select('#ko > div.common-board > div > ul > li > div.texts > ul')
		for n in info:
			info_list.append(n.text.strip())
			
		# 사진 가져오기
		front_url = "https://www.smu.ac.kr" 
		ul_tag = soup.find('ul', {'class', 'board-thumb-wrap2 col2'})
		picture = ul_tag.find_all('img', {'class', 'pImg'})
		for images in picture:
			picture_list.append(front_url + images.get('src'))

		major_count+= 1

		
	#print(len(name_list))
	#print(len(major_list))
	#print(len(info_list))
	#print(len(picture_list))

	#====================================
	# nm_name_list #교양 교수명
	# nm_major_list #그냥 교양
	# nm_info_list #교양 교수 정보
	# nm_picture_list #교양 교수 사진 정보
	#====================================
	# name_list #학과 교수명
	# major_list #학과명
	# info_list #학과 교수 정보
	# picture_list #학과 교수 사진 정보
	#====================================
	# 교양 교수 정보를 학과 교수 정보 뒤에 이어 붙임
	name_list += nm_name_list
	major_list += nm_major_list
	info_list += nm_info_list
	picture_list += nm_picture_list

	####################################

	data = []

	total_count = len(name_list) + len(nm_name_list)
	for i in range(0, total_count):
		data.append([])
		try:
			data[i].append(name_list[i])
			data[i].append(major_list[i])
			data[i].append(info_list[i])
			data[i].append(picture_list[i])
		except:
			#print("list index out of range")
			pass

	driver.close()
	return data
def save_data_prof(prof_data):
	try:
		n = prof_data[0]
		m = prof_data[1]
		i = prof_data[2]
		p = prof_data[3]
		led = smu_professor(major=m,professor=n,information=i,picture=p)
		led.save()
	except:
		#print("save error")
		pass
## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만
## 아래 코드가 동작하도록 한다.
if __name__ == '__main__':
	start_time = time.time()

	pool = Pool(processes=1) # 4개의 프로세스를 사용.

	if(smu_professor.objects.count() != 0):
			print('이전 내용을 지우고 다시 만듭니다.')
			smu_professor.objects.all().delete()

	pool.map(save_data_prof, parse_prof())

	print("--- %s seconds ---" % (time.time() - start_time))