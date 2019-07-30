# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import board_keyword, board, Eval, major_synonym, lecture_evaluation, lecture_time, major_keyword, professor_keyword, search_major, smu_professor, colleges, majors


try:
	board_keyword.objects.all().delete()
	board.objects.all().delete()
	Eval.objects.all().delete()
	major_synonym.objects.all().delete()
	lecture_evaluation.objects.all().delete()
	lecture_time.objects.all().delete()
	major_keyword.objects.all().delete()
	professor_keyword.objects.all().delete()
	search_major.objects.all().delete()
	smu_professor.objects.all().delete()
	colleges.objects.all().delete()
	majors.objects.all().delete()
	print('모두 정상적으로 지워졌습니다.')
except Exception as e:
	print('지우는데 에러가 났어요.')
	print(e)
	pass