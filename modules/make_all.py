# -*- coding: utf-8 -*-
import os
import time
import datetime
filelist = [
	'python save_college_major.py',
	'python save_smu_professor.py',
	'python save_major_synonym.py',
	'python parser_board.py 2019-06 370450',
	'python parser_board.py 2019-06 369474',
	'python parser_board.py 2019-06 hotarticle',
	'python drawc_board.py 2019-06 370450 jagae',
	'python drawc_board.py 2019-06 369474 saenaegi',
	'python drawc_board.py 2019-06 hotarticle hot',
	'python parser_lecture_time.py',
	'python parser_prof_individual.py',
	'python drawc_prof_individual.py',
	'python drawc_major.py',
	'python drawc_ngram_major.py',

	# 아래는 drawc를 실행하면 또 실행할 필요 없으므로 주석처리.
	#'python drawc2_board.py 2019-06 370450 jagae',
	#'python drawc2_board.py 2019-06 369474 saenaegi',
	#'python drawc2_board.py 2019-06 hotarticle hot',
]

start_time = time.time()

for file in filelist:
	os.system(file)

seconds = (time.time() - start_time)
print("--- %s seconds ---" % seconds)
mydelta = datetime.timedelta(seconds=int(seconds))
mytime = datetime.datetime.min + mydelta
h, m, s = mytime.hour, mytime.minute, mytime.second
print("%d시간%02d분%02d초 걸렸음." % (h, m, s))