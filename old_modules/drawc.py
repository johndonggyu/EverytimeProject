## UnicodeEncodeError: 때문에 임시로 넣어놓음.
#import sys
#import io
#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
import re
import numpy as np
import pandas as pd
from konlpy.tag import Kkma
import os
import time
from operator import eq
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
import django
django.setup()
from backend.parsed_data.models import board, Eval
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from PIL import Image

#===========================================#
#               global variables            #
#===========================================#
dir_font = './raw_data/fonts/'
dir_mask = './raw_data/mask/'
dir_excpt = './raw_data/except_dic/'
dir_static = './frontend/static/'
#===========================================#

# 단어 예외처리 파일 불러오기
def get_except_keyword(filename):
	keyword_list = list()
	with open(filename, encoding='utf-8') as f:
		for keyword in f.readlines():
			keyword_list.append(keyword.strip())
	f.close()
	return keyword_list
def get_noun(msg_txt):
	kkma = Kkma()
	nouns = list()
	# ㅋㅋ, ㅠㅠ, ㅎㅎ 등등 필터링
	pattern = re.compile("[ㄱ-ㅎㅏ-ㅣ"
							"\U0001F600-\U0001F64F"  # emoticons
			                "\U0001F300-\U0001F5FF"  # symbols & pictographs
			                "\U0001F680-\U0001F6FF"  # transport & map symbols
			                "\U0001F1E0-\U0001F1FF"  # flags (iOS)
							"]+")
	## 1000개 게시물 했을 때 팅김 현상 해결하기
	msg_txt = re.sub(pattern, "", msg_txt).strip()
	if len(msg_txt) > 0:
		pos = kkma.pos(msg_txt)
		for keyword, type in pos:
			# 고유명사 또는 보통명사
			if type == "NNG" or type == "NNP":
				nouns.append(keyword)
		#print(msg_txt, "->", nouns)
	return nouns
##문자열로 만들어 get_noun에 문자열을 보내어 단어들로 이루어진 리스트를 가져온다. 게시물마다 리스트로 이뤄져, 결과적으로 2차원 리스트가 된다.
## ex) tokens = [['안녕', '천재', '바보'], ['하이', '단어', '리스트']]
def get_tokens(type_, match_):
	tokens = list()
	if type_ == 1:
		everytime_data = board.objects.all()
		for datum in everytime_data:
			if eq(datum.board_id, match_):
				everytime_str = datum.title + " " + datum.contents
				tokens.append(get_noun(everytime_str))
	elif type_ == 2:
		everytime_data = board.objects.all()
		cnt = 0
		pattern = re.compile(match_)
		for datum in everytime_data:
			everytime_str = datum.title + " " + datum.contents
			if bool(re.search(pattern, everytime_str)):
				cnt += 1
				tokens.append(get_noun(everytime_str))
		print(match_ + ' : 매칭되는 수 : ' + str(cnt))
	elif type_ == 3:
		everytime_data = Eval.objects.all()
		for datum in everytime_data:
			str1 = str(datum.eval_number).split(' - ')[0] #한종대
			str2 = str(match_)
			if eq(str1, str2):
				everytime_str = datum.comment
				tokens.append(get_noun(everytime_str))
	return tokens
## one_list() 에서는 2차원 리스트를 1차원 리스트로 변환 해준다. 
def one_list(type_, nid):
	a_list = list()
	a_list = get_tokens(type_, nid)
	a_list = list(itertools.chain.from_iterable(a_list))
	return a_list
##############################################################
#### 아래는 wordcloud 관련된 함수 
##############################################################
def count_word(count):
	word = dict()
	#상위 50개 단어 return
	for tags, counts, in count.most_common(150):
		if(len(str(tags)) > 1):
			word[tags] = counts
			#print("%s : %d" % (tags, counts))
	return word
class MyList(list):
	def __init__(self, *args):
		super(MyList, self).__init__(*args)
	def __sub__(self, other):
		return self.__class__([item for item in self if item not in other])
def draw_wordcloud(kkma_result, match_):
	global dir_excpt
	global dir_font
	global dir_mask
	global dir_static
	if len(kkma_result) == 0:
		print(match_+' : 리스트가 비어서 워드클라우드를 제작할 수 없습니다.')
		return
	else:
		print(match_+" : 워드클라우드 제작 중 입니다.")
	## 특정 단어 필터링 후 워드클라우드 만들기
	if eq(match_, 'jagae') or eq(match_, 'saenaegi') or eq(match_, 'hot'):
		except_keyword = get_except_keyword(dir_excpt + "except_word.txt")
	elif eq(match_, 'cs') or eq(match_, 'hi'):
		except_keyword = get_except_keyword(dir_excpt + "except_word_m.txt")
	elif eq(str(match_), '한종대'):
		except_keyword = get_except_keyword(dir_excpt + "except_word_jongdae.txt")
	else:
		except_keyword = get_except_keyword(dir_excpt + "except_word.txt")
	## get_except_keyword 에 있는 list를 제외한 list만들기
	kkma_result = MyList(kkma_result) - MyList(except_keyword)

	count = Counter(kkma_result)
	##50개 단어만 가져오게 만들기
	wordInfo = count_word(count)

	a_mask = np.array(Image.open(dir_mask + "prof2.png"))
	wc = WordCloud(font_path=dir_font + "NanumGothic.ttf", background_color='white', mask=a_mask).generate_from_frequencies(wordInfo)
	plt.figure(figsize=(30, 30))
	plt.imshow(wc, interpolation="bilinear")
	plt.axis("off")
	outputfile_name = dir_static + "wc/"+match_+".png"
	plt.savefig(outputfile_name)
################################################################
if __name__ == '__main__':
	start_time = time.time()
	
	###### 변수 공간 ######
	######################
	JAGAE = '370450'    ##
	SAENAEGI = '369474' ##
	#hot = 'hotarticle' ##
	######################

	##위에 선언되어 있음
	#자유게시판 : jagae, 새내기게시판: saenaegi, 핫게시판: hotarticle
	draw_wordcloud(one_list(1, JAGAE), 'jagae')
	#draw_wordcloud(one_list(1, SAENAEGI), 'saenaegi')

	### 학과별 워드클라우드 만들기
	##학과이름 정규식(정확하게), '저정할 파일 이름'
	#draw_wordcloud(one_list(2, '컴과|컴퓨터과학|컴퓨터과학과'), 'cs')
	#draw_wordcloud(one_list(2, '휴먼|휴지|휴먼지능정보공학과|휴먼지능정보공학'), 'hi')

	### 교수별 워드클라우드 만들기(검색어+강의평)
	## type 2는 게시판에서 검색, type 3은 강의평에서 검색
	draw_wordcloud((one_list(2, '한종대|한종대교수님') + one_list(3, '한종대')), 'jongdaehan') #교수님 검색어 + 강의평
	#draw_wordcloud(one_list(3, '장백철'), 'bakchul') #교수님 검색어 + 강의평

	print("--- %s seconds ---" % (time.time() - start_time))
