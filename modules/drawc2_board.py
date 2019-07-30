# -*- coding: utf-8 -*-
## UnicodeEncodeError: 때문에 임시로 넣어놓음.
#import sys
#import io
#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
import re
import numpy as np
import pandas as pd
import time
from operator import eq
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import board_keyword
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

def get_word(_date):
	word = dict()
	for w in board_keyword.objects.filter(code=boardcode_).order_by('-count'):
		#print(w.keyword)
		word[w.keyword] = w.count
	return word
def draw_wordcloud(match_, _date):
	global dir_excpt
	global dir_font
	global dir_mask
	global dir_static
	
	wordInfo = get_word(_date)

	#a_mask = np.array(Image.open(dir_mask + "prof2.png"))
	wc = WordCloud(width=1600,height=1600,font_path=dir_font + "NanumGothic.ttf", background_color='white').generate_from_frequencies(wordInfo) #, mask=a_mask
	plt.figure(figsize=(20, 20))
	#plt.imshow(wc, interpolation="bilinear")
	plt.imshow(wc, interpolation="lanczos")
	plt.axis("off")
	plt.tight_layout(pad=0)
	outputfile_name = dir_static + "wc/"+match_+".png"
	plt.savefig(outputfile_name, bbox_inches='tight', edgecolor='none')
################################################################
if __name__ == '__main__':
	start_time = time.time()
	
	if(len(sys.argv) == 1):
		raise Exception("날짜를 입력해주세요.")
	else:
		_date = sys.argv[1] #2019-07

	if(len(sys.argv) == 2):
		raise Exception("게시판코드를 입력해주세요.")
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
	if(board_keyword.objects.filter(code=boardcode_).count() == 0):
		print("키워드 테이블이 비었습니다. board_drawc.py를 실행해주세요.")
		#draw_wordcloud('jagae'+_date, _date)
	else:
		tmp = board_keyword.objects.filter(code=boardcode_).order_by('-word_date').first()
		if(str(tmp.word_date)[0:7] == _date[0:7]):
			print("해당 달의 데이터가 DB에 있네요. 진행하시겠습니까? 예[1] 아니오[2]")
			temp = input()
			if(temp == 1 or temp == "1"):
				# db에 있는 해당 월의 데이터 삭제 후 다시하기
				start = datetime(int(_date[0:4]),int(_date[5:7]),1)
				# 나중에 31일까지 있는 월에 한해서 예외처리하기.
				end = datetime(int(_date[0:4]),int(_date[5:7]),30)
				draw_wordcloud(boardfile_+_date, _date)

	#draw_wordcloud(one_list(bc.jayu), 'jagae')
	#draw_wordcloud(one_list(1, '369474'), 'saenaegi')
	if(temp == 1 or temp == "1"):
		print("--- %s seconds ---" % (time.time() - start_time))
