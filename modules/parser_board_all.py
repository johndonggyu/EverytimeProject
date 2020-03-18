# -*- coding: utf-8 -*-
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
from Web.models import board
from multiprocessing import Pool
from urllib import parse
import sys
from datetime import datetime
# 전역변수 공간#
#############################
i = 0 	   				 ####
#BNUM = 100 			 ####
ID = '아이디'		 ####
PW = '비밀번호' ####
boardcode_ = 0              
#############################
def board_crawling(s, data, bid, limit_date, opt): #limit_num
	print(str(boardcode_) + "게시판 크롤링 중 입니다. 잠시만 기다려주세요. " + str(limit_date) + "까지의 게시물")
	start_num = 0
	only_once = True
	global i

	## limit_num 예외처리
	#if limit_num < 20:
	#	raise Exception('제한 게시글 수가 20이하입니다! 20이상으로 해주세요')

	#while(start_num < limit_num):
	while(True):
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
			created_at = post.attrib['created_at'] #created_at="2019-08-20 19:13:59"

			#if(only_once):
			#	only_once = False
			#	if(limit_date[0:7] > created_at[0:7]):
			#		print("해당 월의 데이터가 없습니다. 날짜를 다시 확인해주세요.")
			#		return

			if(opt == 1): #월별
				if(limit_date <= created_at[0:7]): #0:10하면 일별임
					#해당 월(limit_date)까지/포함해서 파싱한다.
					data.append([])
					data[i].append(title2)
					#data[i].append(link)
					data[i].append(contents) #.replace("<br />", " ").replace("<br/>", " ").replace("</br>", " ").replace("</ br>", " ").replace("<br>", " ")
					data[i].append(created_at)
					data[i].append(bid)
					print(str(i)+'-'+created_at[0:7])
					i += 1
				else:
					return
			elif(opt == 2):
				print("일별은 이 모드에서는 지원되지 않습니다.")
				return
			else:
				print("경고: 월별인지 일별인지 인자값을 확인해주세요")
				return

def parse_everytime(input_date, opt):
	global ID
	global PW
	#global BNUM
	BNUM = input_date
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
		board_crawling(s, data, boardcode_, BNUM, opt) #자유게시판 session, data, board_id, limit_num
		#board_crawling(s, data, '369474', BNUM) #새내기게시판
	return data
def save_data_board(everytime_data):
	t = everytime_data[0]
	c = everytime_data[1]
	d = everytime_data[2]
	o = everytime_data[3]
	#l = everytime_data[1]
	try:
		#board(title=t, contents=c, date=d, code=o).save()
		board(title=t, contents=c, date=d, code=o).save()
	except:
		#print('게시물 중복 에러!')
		pass
## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만
## 아래 코드가 동작하도록 한다.
if __name__ == '__main__':
	if len(sys.argv) is 1:
		print("사용법: python parser_board_all.py 년도-월(예: 2018-01) 게시판코드(예: 370450)")
		print("사용예시: python parser_board_all.py 2018-01 370450")
		print("날짜는 해당 년도와 월까지의 모든 데이터를 역순으로 파싱한다. 예를 들어 현재 날짜가 2019-08일 경우, 2019-08, 07, 06, ... 2018-01까지 파싱한다.")
		raise Exception('')
	start_time = time.time()

	date = sys.argv[1] #2019-07
	boardcode_ = sys.argv[2]

	if(len(date) == 7):
		opt = 1 #월별
	elif(len(date) == 10):
		opt = 2 #일별
	else:
		raise Exception('잘못된 날짜 형식입니다.')

	pool = Pool(processes=4) # 4개의 프로세스를 사용.
	temp = 0
	if(board.objects.filter(code=boardcode_).count() == 0):
		print("테이블이 비었습니다.")
		pool.map(save_data_board, parse_everytime(date, opt))
		temp = 1
	else:
		tmp = board.objects.filter(code=boardcode_,date__month=date[5:7]).first()
		if(tmp and str(tmp.date)[0:7] == date[0:7]):
			print("이미 파싱한 월의 데이터 입니다.\n그래도 파싱하시겠습니까? 예[1] 아니오[2]")
			temp = input()
			if(temp == 1 or temp == "1"):
				pool.map(save_data_board, parse_everytime(date, opt))
		#elif(tmp and str(tmp.date)[0:7] > date[0:7]):
		#	print("이미 파싱한 월의 데이터가 더 최근달의 데이터입니다.\n그래도 파싱하시겠습니까? 예[1] 아니오[2]")
		#	temp = input()
		#	if(temp == 1 or temp == "1"):
		#		pool.map(save_data_board, parse_everytime(date, opt))
		else:
			print("다른 날짜의 데이터가 DB에 있습니다.")
			pool.map(save_data_board, parse_everytime(date, opt))
	
	#pool.map(save_data_board, parse_everytime(date, opt))
	if(temp == 1):
		print("--- %s seconds ---" % (time.time() - start_time))
		print("--- %s boards ---" % (board.objects.filter(code=boardcode_).count()))
