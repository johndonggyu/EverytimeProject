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
from Web.models import board, major_keyword, major_synonym, search_major
import itertools
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
from PIL import Image
from datetime import datetime

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
def get_tokens(major1, major_):
	tokens = list()
	everytime_data = board.objects.all()
	cnt = 0
	pattern = re.compile(major_)
	for datum in everytime_data:
		everytime_str = datum.title + " " + datum.contents
		if bool(re.search(pattern, everytime_str)):
			try:
				search_major(board_number=datum,major=major1).save()
			except Exception as e:
				pass
			cnt += 1
			tokens.append(get_noun(everytime_str))
	print(major_ + ' : 매칭되는 수 : ' + str(cnt))
	return tokens
def one_list(major, major_):
	# 2차원 리스트를 1차원 리스트로 변환 해준다. 
	a_list = list()
	a_list = get_tokens(major, major_)
	a_list = list(itertools.chain.from_iterable(a_list))
	return a_list
def count_word(major_, count):
	# 해당 학과의 데이터가 이미 있다면, 지우기.
	if(major_keyword.objects.filter(major=major_).count != 0):
				major_keyword.objects.filter(major=major_).delete()
	word = dict()
	for tags, counts, in count.most_common(50):
		if(len(str(tags)) > 1):
			word[tags] = counts
			try:
				major_keyword(major=major_, keyword=tags, word_date=datetime.now(), count=counts).save()
			except Exception as e:
				pass
	return word
def insertKeyword(result, major):
	if len(result) == 0:
		return
	count = Counter(result)
	count_word(major, count)
if __name__ == '__main__':
	start_time = time.time()

	### 학과별 워드클라우드 만들기
	for i in major_synonym.objects.all():
		insertKeyword(one_list(i.major, i.synonym), i.major)

	print("--- %s seconds ---" % (time.time() - start_time))
