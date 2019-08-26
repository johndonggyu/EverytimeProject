# -*- coding: utf-8 -*-
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
		if len(msg_txt) > 0:
			pos = kkma.pos(msg_txt)
			for keyword, type in pos:
				# 고유명사 또는 보통명사
				if type == "NNG" or type == "NNP":
					nouns.append(keyword)
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
	#for m in majors.objects.filter(major='컴퓨터과학과'):
		hakgua = m.major
		if(major_ngram_keyword.objects.filter(major=hakgua).count != 0):
				print('ngram 키워드 테이블 비우고 다시 채웁니다.')
				major_ngram_keyword.objects.filter(major=hakgua).delete()
		if not hakgua:
			#계당교양교욱원은 major이 없음
			hakgua = m.college.college
		elif len(hakgua) < 2:
			continue
		if(len(hakgua) > 1):
			s = search_major.objects.filter(major=hakgua)
			for b in s:
				word_list.append(get_tokens(b.board_number))
		for word_l in word_list:
			for word in word_l:
				if(len(word) < 2):
					word_l.remove(word)
		words_ngram = flatten(Make_Ngram(word_list, 3))
		one = major_synonym.objects.filter(major=hakgua).first()
		synlist = one.synonym.split('|')
		if len(words_ngram) == 0:
			print(str(hakgua)+' : 리스트가 비어서 워드클라우드를 제작할 수 없습니다.')
		else:
			print(str(hakgua)+" : 워드클라우드 제작 중 입니다.")
			ngram3_major_top100 = nltk.FreqDist(words_ngram).most_common(50)
			for tags, counts in ngram3_major_top100:
				try:
					major_ngram_keyword(major=hakgua, keyword=tags, word_date=datetime.now(), count=counts).save()
				except Exception as e:
					print(e)
					pass

	print("--- %s seconds ---" % (time.time() - start_time))
