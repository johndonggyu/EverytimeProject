# -*- coding: utf-8 -*-
## UnicodeEncodeError: 때문에 임시로 넣어놓음.
#import sys
#import io
#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
import re
import numpy as np
import pandas as pd
from konlpy.tag import Kkma
import time
from operator import eq
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import board, board_keyword
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from PIL import Image
from datetime import datetime

#===========================================#
#               global variables            #
#===========================================#
dir_font = './raw_data/fonts/'
dir_mask = './raw_data/mask/'
dir_excpt = './raw_data/except_dic/'
dir_static = '../Web/static/'
boardcode_ = 0
boardfile_ = "none"
#===========================================#

# 단어 예외처리 파일 불러오기
def get_except_keyword(filename):
	keyword_list = list()
	try:
		with open(filename, encoding='utf-8') as f:
			for keyword in f.readlines():
				keyword_list.append(keyword.strip())
		f.close()
	except:
		print('file read error')
	return keyword_list
def get_noun(msg_txt):
	kkma = Kkma()
	nouns = list()
	try:
		#한글만 뽑아내기
		hanguleng = re.compile('[^ ㄱ-ㅣ가-힣]+')
		msg_txt = hanguleng.sub('', msg_txt)
		# ㅋㅋ, ㅠㅠ, ㅎㅎ 등등 필터링
		pattern = re.compile("[ㄱ-ㅎㅏ-ㅣ]+")
		msg_txt = re.sub(pattern, '', msg_txt).strip()
	except:
		print('msg_txt strip error')
	try:
		#print(msg_txt)
		if len(msg_txt) > 0:
			pos = kkma.pos(msg_txt)
			for keyword, type in pos:
				# 고유명사 또는 보통명사
				if type == "NNG" or type == "NNP":
					nouns.append(keyword)
			#print(msg_txt, "->", nouns)
	except:
		print("get_noun Error!")
		print(msg_txt)

	return nouns
##문자열로 만들어 get_noun에 문자열을 보내어 단어들로 이루어진 리스트를 가져온다. 게시물마다 리스트로 이뤄져, 결과적으로 2차원 리스트가 된다.
## ex) tokens = [['안녕', '천재', '바보'], ['하이', '단어', '리스트']]
def get_tokens(match_, _date):
	tokens = list()
	start = datetime(int(_date[0:4]),int(_date[5:7]),1)
	end = datetime(int(_date[0:4]),int(_date[5:7]),30)
	everytime_data = board.objects.filter(date__range=(start, end),code=boardcode_)
	for datum in everytime_data:
		if eq(datum.code, match_):
			everytime_str = datum.title + " " + datum.contents
			tokens.append(get_noun(everytime_str))
	return tokens
## one_list() 에서는 2차원 리스트를 1차원 리스트로 변환 해준다. 
def one_list(nid, _date):
	a_list = list()
	a_list = get_tokens(nid, _date)
	a_list = list(itertools.chain.from_iterable(a_list))
	return a_list
##############################################################
#### 아래는 wordcloud 관련된 함수 
##############################################################
def count_word(count, _date):
	# 해당 게시판 키워드의 데이터가 이미 있다면, 지우기.
	if(board_keyword.objects.filter(code=boardcode_).count != 0):
				board_keyword.objects.filter(code=boardcode_).delete()
	
	word = dict()
	#상위 150개 단어 return
	#print(count)
	#try:
	for tags, counts, in count.most_common(50):
		if(len(str(tags)) > 1):
			word[tags] = counts
			#print("%s : %d" % (tags, counts))
			start = datetime(int(_date[0:4]),int(_date[5:7]),1)
			try:
				board_keyword(code=boardcode_, keyword=tags, word_date=start, count=counts).save()
			except Exception as e:
				print(e)
				pass
	#except:
	#	print('count word error')
	return word
class MyList(list):
	def __init__(self, *args):
		super(MyList, self).__init__(*args)
	def __sub__(self, other):
		return self.__class__([item for item in self if item not in other])
def draw_wordcloud(kkma_result, match_, _date):
	global dir_excpt
	global dir_font
	global dir_mask
	global dir_static
	if len(kkma_result) == 0:
		print('게시판 : 리스트가 비어서 워드클라우드를 제작할 수 없습니다.')
		print('아마 해당 월의 데이터가 없을 지도 모르니 확인바랍니다.')
		return
	else:
		print("게시판 : 워드클라우드 제작 중 입니다.")
	## 특정 단어 필터링 후 워드클라우드 만들기
	except_keyword = get_except_keyword(dir_excpt + "except_word.txt")
	## get_except_keyword 에 있는 list를 제외한 list만들기
	kkma_result = MyList(kkma_result) - MyList(except_keyword)
	
	count = Counter(kkma_result)
	##150개 단어만 가져오게 만들기
	wordInfo = count_word(count, _date)

	#a_mask = np.array(Image.open(dir_mask + "prof2.png"))
	wc = WordCloud(width=1600,height=1600,font_path=dir_font + "NanumGothic.ttf", background_color='white').generate_from_frequencies(wordInfo) #, mask=a_mask
	plt.figure(figsize=(20, 20))
	#plt.imshow(wc, interpolation="bilinear")
	plt.imshow(wc, interpolation="lanczos")
	plt.axis("off")
	plt.tight_layout(pad=0)
	outputfile_name = dir_static + "wc/"+match_+".png"
	plt.savefig(outputfile_name, bbox_inches='tight', edgecolor='none')
def insertKeyword(result, _date):
	if len(result) == 0:
		print('게시판 : 리스트가 비어서 워드클라우드를 제작할 수 없음.')
		print('아마 해당 월의 데이터가 없을 지도 모름.')
		return
	else:
		print('게시판 : 워드클라우드를 제작 중 ')
	count = Counter(result)
	count_word(count, _date)
################################################################
if __name__ == '__main__':
	start_time = time.time()
	
	if(len(sys.argv) == 1):
		raise Exception("날짜를 입력해주세요.")
	else:
		_date = sys.argv[1] #2019-07

	if(len(sys.argv) == 2):
		raise Exception("게시판 번호를 입력해주세요.")
	else:
		boardcode_ = sys.argv[2]

	if(len(sys.argv) == 3):
		raise Exception("파일명을 입력해주세요.")
	else:
		boardfile_ = sys.argv[3]

	if(len(_date) == 7):
		opt = 1 #월별
	elif(len(_date) == 10):
		opt = 2 #일별
	else:
		raise Exception('잘못된 날짜 형식입니다.')

	temp = 0
	if(board.objects.filter(code=boardcode_).count() == 0):
		print("크롤링을 먼저 진행 후 실행해주세요.")
	elif(board_keyword.objects.filter(code=boardcode_).count() == 0):
		print("키워드 테이블이 비었습니다. 바로 wordcloud 만들겠습니다.")
		#draw_wordcloud(one_list(boardcode_, _date), boardfile_+_date, _date)
		insertKeyword(one_list(boardcode_, _date), _date)
	else:
		tmp = board_keyword.objects.filter(code=boardcode_).order_by('-word_date').first()
		if(str(tmp.word_date)[0:7] == _date[0:7]):
			print("이미 만든 달의 데이터 입니다.\n그래도 만드시겠습니까? 예[1] 아니오[2]")
			temp = input()
			if(temp == 1 or temp == "1"):
				# db에 있는 해당 월의 데이터 삭제 후 다시하기
				start = datetime(int(_date[0:4]),int(_date[5:7]),1)
				# 나중에 31일까지 있는 월에 한해서 예외처리하기.
				end = datetime(int(_date[0:4]),int(_date[5:7]),30)
				del_obj = board_keyword.objects.filter(word_date__range=(start, end),code=boardcode_)
				del_obj.filter(code=boardcode_).delete()
				print("이미 만든 달의 데이터는 삭제되고 다시 추가됩니다.")
				#draw_wordcloud(one_list(boardcode_, _date), boardfile_+_date, _date)
				insertKeyword(one_list(boardcode_, _date), _date)

	#draw_wordcloud(one_list(boardcode_), 'jagae')
	#draw_wordcloud(one_list(1, '369474'), 'saenaegi')
	if(temp == 1 or temp == "1"):
		print("--- %s seconds ---" % (time.time() - start_time))
