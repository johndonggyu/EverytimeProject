import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os
import time
from operator import eq
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
import django
django.setup()
from backend.parsed_data.models import EverytimeData, EvalData, LectEvalData
from multiprocessing import Pool
from urllib import parse
# 전역변수 공간#
#############################
i = 0 	   				 ####
BNUM = 100 				 ####
ID = 'johndonggyu'		 ####
PW = 'everytime1234!@#$' ####              
#############################
def eval_crawling(s, data, m):
	print(m+" 크롤링 중 입니다. 잠시만 기다려주세요.")
	start_num = 0
	global i
	url = parse.urlparse('https://everytime.kr/find/lecture/list/keyword?keyword='+m)
	query = parse.parse_qs(url.query)
	q = parse.urlencode(query, doseq=True)
	gangyipyeong = s.get('https://everytime.kr/find/lecture/list/keyword?'+q)

	e = ET.fromstring(gangyipyeong.text)
	for board in e.iter('lecture'):
		#print(board.attrib)
		id = board.attrib['id']
		#print(id) #게시물 id 
		board_src = "https://everytime.kr/find/lecture/article/list?school_id=13&limit_num=200&lecture_id="
		link = board_src + id

		## 과목 강의평가 정보 가져오기
		post_one = s.get(link)
		e2 = ET.fromstring(post_one.text)

		## 강의평 lecture, rate, details
		post = e2.find('./lecture')
		lect_name = post.attrib['name']
		prof_name = post.attrib['professor']
		
		post = e2.find('./rate')
		rate = post.text
		
		post = e2.find('./details')
		grade = post.attrib['assessment_grade']
		homework = post.attrib['assessment_homework']
		team = post.attrib['assessment_team']
		attendance = post.attrib['assessment_attendance']
		exam_times = post.attrib['exam_times']

		contents = []
		
		cnt = 0
		for p in e2.iter('article'):
			contents.append(p.attrib['text'])
			cnt += 1

		data.append([])
		data[i].append(lect_name)
		data[i].append(prof_name)
		data[i].append(rate)
		data[i].append(grade)
		data[i].append(homework)
		data[i].append(team)
		data[i].append(attendance)
		data[i].append(exam_times)
		#data[i].append([])
		#data[i][8].append(contents)
		data[i].append(contents)

		i += 1

def board_crawling(s, data, bid, limit_num):
	print(bid+"크롤링 중 입니다. 잠시만 기다려주세요. " + str(limit_num) + "개 게시물")
	start_num = 0
	global i

	## limit_num 예외처리
	if limit_num < 20:
		raise Exception('제한 페이지 수가 20이하입니다! 20이상으로 해주세요')

	while(start_num < limit_num):
			gaesipan = s.get('https://everytime.kr/find/board/article/list?id='+bid+'&limit_num=20&start_num='+str(start_num)+'&moiminfo=false')
			start_num += 20

			e = ET.fromstring(gaesipan.text)
			
			for board in e.iter('article'):
				#print(board.attrib)
				id = board.attrib['id']
				#print(id) #게시물 id 
				board_src = "https://everytime.kr/find/board/comment/list?id="
				link = board_src + id + "&limit_num=-1&moiminfo=false"

				## 자유게시판의 게시물 정보 가져오기
				post_one = s.get(link)
				e2 = ET.fromstring(post_one.text)
				post = e2.find('./article')
				title2 = post.attrib['title']
				contents = post.attrib['text']
				created_at = post.attrib['created_at']

				data.append([])
				data[i].append(title2)
				data[i].append(link)
				data[i].append(contents)
				data[i].append(created_at)
				data[i].append(bid)
				i += 1
def parse_everytime(type_):
	global ID
	global PW
	global BNUM
	data = []
	## 로그인할 유저정보를 넣어줍시다. (모두 문자열입니다)
	LOGIN_INFO = {
		'userid': ID,
		'password': PW
	}
	LOGIN_INFO = {**LOGIN_INFO}
	with requests.Session() as s:	
		login_req = s.post('https://everytime.kr/user/login', LOGIN_INFO)
		#print(login_req.status_code)
		if login_req.status_code != 200:
			raise Exception('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')
		if eq(str(type_), str(1)):
			board_crawling(s, data, '370450', BNUM) #자유게시판 session, data, board_id, limit_num
			#board_crawling(s, data, '369474', BNUM) #새내기게시판
			#board_crawling(s, data, 'hotarticle') #핫게시판
		elif eq(str(type_), str(2)): #위에거가 if 문이면, elif로 변경하기
			eval_crawling(s, data, '한종대') #자유게시판 session, data, prof_name 학기당 돌리기
	return data
def save_data_board(everytime_data):
	t = everytime_data[0]
	l = everytime_data[1]
	c = everytime_data[2]
	a = everytime_data[3]
	b = everytime_data[4]
	EverytimeData(title=t, links=l, contents=c, created_at=a, board_id=b).save()
def save_data_eval(everytime_data):
	l = everytime_data[0]
	p = everytime_data[1]
	r = everytime_data[2]
	g = everytime_data[3]
	h = everytime_data[4]
	t = everytime_data[5]
	a = everytime_data[6]
	e = everytime_data[7]
	led = LectEvalData(lecture=l, professor=p, 
		score=r, assignment=h, team_project=t,
		credit=g,attendance=a, test=e)
	led.save()
	for c in everytime_data[8]:
		EvalData(eval_number=led, comment=c).save()
## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만
## 아래 코드가 동작하도록 한다.
if __name__ == '__main__':
	start_time = time.time()

	pool = Pool(processes=4) # 4개의 프로세스를 사용.
	pool.map(save_data_board, parse_everytime(1))
	i = 0
	pool.map(save_data_eval, parse_everytime(2))

	print("--- %s seconds ---" % (time.time() - start_time))