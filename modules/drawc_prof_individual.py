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
from Web.models import lecture_evaluation, Eval, smu_professor, lecture_time, professor_keyword
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
	try:
		#한글만 뽑아내기
		hanguleng = re.compile('[^ ㄱ-ㅣ가-힣]+')
		msg_txt = hanguleng.sub('', msg_txt)
		# ㅋㅋ, ㅠㅠ, ㅎㅎ 등등 필터링
		pattern = re.compile("[ㄱ-ㅎㅏ-ㅣ]+")
		msg_txt = re.sub(pattern, '', msg_txt).strip()
	except:
		pass
		#print('msg_txt strip error')
	try:
		#print(msg_txt)
		if len(msg_txt) > 0:
			pos = kkma.pos(msg_txt)
			for keyword, type in pos:
				# 고유명사 또는 보통명사
				if type == "NNG" or type == "NNP":
					nouns.append(keyword)
	except:
		pass
		#print("get_noun Error!")
		#print(msg_txt)

	return nouns
			#print(msg_txt, "->", nouns)
##문자열로 만들어 get_noun에 문자열을 보내어 단어들로 이루어진 리스트를 가져온다. 게시물마다 리스트로 이뤄져, 결과적으로 2차원 리스트가 된다.
## ex) tokens = [['안녕', '천재', '바보'], ['하이', '단어', '리스트']]
def get_tokens(match_, match2_):

	match_lect = lecture_time.objects.filter(professor__professor=match_,professor__major=match2_)
	match_eval = lecture_evaluation.objects.filter(professor__professor__professor=match_)

	lect = []
	for a in match_lect:
	    lect.append(a.lecture)

	c = []
	for item in match_eval:
	    if(item.professor.lecture in lect):
	        d = {}
	        #print(item.professor,item.lecture)
	        d[item.professor.professor.professor] = item.professor.lecture
	        c.append(d)

	#print(c)
	#print(len(c))
	#print(c[0][match_])

	f = []

	for i in range(0, len(c)):
	    e = Eval.objects.filter(comment_prof__professor__professor__professor=match_,comment_prof__professor__lecture=c[i][match_])
	    #print(len(e))
	    if(len(e) == 0):
	        continue
	    if(len(e) > 1):
	        for it in e:
	            f.append(it.comment)
	    else:
	        f.append(e[0].comment)

	#동명이인 처리 완료.
	#print(f) # f 는 list 형태로 강의평들이 들어있음.

	tokens = list()

	for datum in f:
		tokens.append(get_noun(datum))
	return tokens
## one_list() 에서는 2차원 리스트를 1차원 리스트로 변환 해준다. 
#def get_tokens2(major, major_):
#	tokens = list()

	# 해당 학과의 데이터가 이미 있다면, 지우기.
#	if(major_keyword.objects.filter(major=major).count != 0):
#				major_keyword.objects.filter(major=major).delete()

#	everytime_data = board.objects.all()
#	cnt = 0
#	pattern = re.compile(major_)
#	for datum in everytime_data:
#		everytime_str = datum.title + " " + datum.contents
#		if bool(re.search(pattern, everytime_str)):
#			try:
#				search_major(board_number=datum,major=major).save()
#			except Exception as e:
#				#print(e)
#				pass
#			cnt += 1
#			tokens.append(get_noun(everytime_str))
#	print(major_ + ' : 매칭되는 수 : ' + str(cnt))

#	return tokens
def one_list(a, b):
	a_list = list()
	a_list = get_tokens(a, b)
	#b_list = list()
	#b_list = get_tokens2(a, b)
	a_list = list(itertools.chain.from_iterable(a_list))
	#b_list = list(itertools.chain.from_iterable(b_list))
	return a_list #+b_list
##############################################################
#### 아래는 wordcloud 관련된 함수 
##############################################################
def count_word(major, pname, count):
	word = dict()
	#상위 50개 단어 return
	for tags, counts, in count.most_common(50):
		if(len(str(tags)) > 1):
			word[tags] = counts
			#print("%s : %d" % (tags, counts))
			#start = datetime(int(_date[0:4]),int(_date[5:7]),1)
			try:
				professor_keyword(major=major, professor=pname, keyword=tags, word_date=datetime.now(), count=counts).save()
			except Exception as e:
				#print(e)
				pass
	return word
class MyList(list):
	def __init__(self, *args):
		super(MyList, self).__init__(*args)
	def __sub__(self, other):
		return self.__class__([item for item in self if item not in other])
def draw_wordcloud(major, pname, kkma_result, match_):
	global dir_excpt
	global dir_font
	global dir_mask
	global dir_static
	if len(kkma_result) == 0:
		print(str(major)+'-'+str(pname)+'리스트가 비어서 워드클라우드를 제작할 수 없습니다.')
		return
	else:
		print("워드클라우드 제작 중 입니다.")
	## 특정 단어 필터링 후 워드클라우드 만들기	
	#except_keyword = get_except_keyword(dir_excpt + "except_word.txt")
	## get_except_keyword 에 있는 list를 제외한 list만들기
	#kkma_result = MyList(kkma_result) - MyList(except_keyword)

	count = Counter(kkma_result)
	##50개 단어만 가져오게 만들기
	wordInfo = count_word(major, pname, count)

	#a_mask = np.array(Image.open(dir_mask + "prof2.png"))
	wc = WordCloud(width=1600,height=1600,font_path=dir_font + "NanumGothic.ttf", background_color='white').generate_from_frequencies(wordInfo) #, mask=a_mask
	plt.figure(figsize=(20, 20))
	plt.imshow(wc, interpolation="lanczos")
	plt.axis("off")
	plt.tight_layout(pad=0)
	outputfile_name = dir_static + "wc/"+match_+".png"
	plt.savefig(outputfile_name, bbox_inches='tight', edgecolor='none')
def insertKeyword(major, pname, result):
	if len(result) == 0:
		print(str(major)+'-'+str(pname)+'리스트가 비어서, 워드클라우드를 제작할 수 없음.')
		return
	else:
		print(str(major)+'-'+str(pname)+'워드클라우드 제작 중')
	count = Counter(result)
	count_word(major,pname,count)
################################################################
if __name__ == '__main__':
	start_time = time.time()

	if(lecture_evaluation.objects.count() == 0):
		Exception("parser를 먼저 실행해주세요.")

	#smu_professor 에서 이름, 학과 꺼내오기.
	for yo in smu_professor.objects.all():
	#for yo in smu_professor.objects.filter(major='컴퓨터과학과'):
		#draw_wordcloud(yo.major, yo.professor, one_list(yo.professor, yo.major), yo.professor+'-'+yo.major+str(datetime.now().year))
		insertKeyword(yo.professor, yo.major, one_list(yo.professor, yo.major))

	print("--- %s seconds ---" % (time.time() - start_time))
