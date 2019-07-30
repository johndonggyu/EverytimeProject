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
from Web.models import board, search_major, majors, major_synonym, major_ngram_keyword
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from PIL import Image
from datetime import datetime
import nltk
#===========================================#
#               global variables            #
#===========================================#
dir_font = './raw_data/fonts/'
dir_mask = './raw_data/mask/'
dir_static = '../Web/static/'
#===========================================#

flatten = lambda l: [w for s in l for w in s]
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
def get_tokens(bbs):
	everytime_str = bbs.title + " " + bbs.contents
	tokens = get_noun(everytime_str)
	return tokens
def Make_Ngram(l, n):
    ngram_list = [[' '.join(gram) for gram in nltk.ngrams(token, n)] for token in l]
    return ngram_list
###############################################################
if __name__ == '__main__':
	start_time = time.time()

	word_list = []
	
	for m in majors.objects.all():
	#for m in majors.objects.filter(college__college='계당교양교육원'):
		hakgua = m.major
		if(major_ngram_keyword.objects.filter(major=hakgua).count != 0):
				print('ngram 키워드 테이블 비우고 다시 채웁니다.')
				major_ngram_keyword.objects.filter(major=hakgua).delete()

		if not hakgua:
			#계당교양교욱원은 major이 없음
			hakgua = m.college.college
		elif len(hakgua) < 2:
			continue
		print('학과: '+str(hakgua))
		if(len(hakgua) > 1):
			s = search_major.objects.filter(major=hakgua)
			# s.board_number 로 하면 게시물을 알 수 있음
			for b in s:
				word_list.append(get_tokens(b.board_number))
		#게시글들 리스트 word_list
		#해당 게시물 word_l에서 한글자는 리스트에서 제외.
		#이 기능은 형태소분석기의 성능에 전적으로 좌우됨.
		#CODE-A0001
		for word_l in word_list:
			for word in word_l:
				if(len(word) < 2):
					word_l.remove(word)

		words_ngram = flatten(Make_Ngram(word_list, 3))
		one = major_synonym.objects.filter(major=hakgua).first()
		synlist = one.synonym.split('|')
		#ngram3_major = [gram for gram in words_ngram if str(one.synonym) in gram]
		
		ngram3_major = []
		for gram in words_ngram:
			for sl in synlist:
				if sl in gram:
					ngram3_major.append(gram)
					break

		if len(ngram3_major) == 0:
			print(str(hakgua)+' : 리스트가 비어서 워드클라우드를 제작할 수 없습니다.')
		else:
			print(str(hakgua)+" : 워드클라우드 제작 중 입니다.")
			ngram3_major_top100 = nltk.FreqDist(ngram3_major).most_common(100)
			for tags, counts in ngram3_major_top100:
				try:
					major_ngram_keyword(major=hakgua, keyword=tags, word_date=datetime.now(), count=counts).save()
				except Exception as e:
					print(e)
					pass

			wc = WordCloud(relative_scaling = 0.8,width=1600,height=1600,font_path=dir_font + "NanumGothic.ttf", background_color='white').generate_from_frequencies(dict(ngram3_major_top100))
			plt.figure(figsize=(20, 20))
			plt.imshow(wc, interpolation="bilinear")
			plt.axis("off")
			plt.tight_layout(pad=0)
			outputfile_name = dir_static + "wc/"+str(hakgua)+"Ng3_"+str(datetime.now().year)+".png"
			plt.savefig(outputfile_name, bbox_inches='tight', edgecolor='none')
	#

	print("--- %s seconds ---" % (time.time() - start_time))
