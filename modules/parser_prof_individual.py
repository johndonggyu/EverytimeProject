import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from operator import eq
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import board, lecture_evaluation, Eval, smu_professor, lecture_time
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
	for board_ in e.iter('lecture'):
		try:
			#print(board.attrib)
			id = board_.attrib['id']
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
		except Exception as e:
			print(e)
			pass

		i += 1

def parse_everytime(pname):
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

		eval_crawling(s, data, pname)
	return data

def save_data_eval(everytime_data):
	l = everytime_data[0]
	p = everytime_data[1]
	r = everytime_data[2]
	g = everytime_data[3]
	h = everytime_data[4]
	t = everytime_data[5]
	a = everytime_data[6]
	e = everytime_data[7]
	lt = lecture_time.objects.filter(lecture=l,professor__professor=p)
	if(len(lt) > 0):
		led = lecture_evaluation(professor=lt[0], 
			score=r, assignment=h, team_project=t,
			credit=g,attendance=a, test=e)
		led.save()
		for c in everytime_data[8]:
			Eval(comment_prof=led, comment=c).save()
## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만
## 아래 코드가 동작하도록 한다.
if __name__ == '__main__':
	start_time = time.time()

	pool = Pool(processes=1) # 여기서는 무조건 1개 사용해야함.

	# 차마 all() 하기가 무섭다. 몇분 걸릴지 과연... 
	for pname in smu_professor.objects.all():
	#for pname in smu_professor.objects.filter(major="컴퓨터과학과"):
		i = 0
		pool.map(save_data_eval, parse_everytime(pname.professor))

	print("--- %s seconds ---" % (time.time() - start_time))