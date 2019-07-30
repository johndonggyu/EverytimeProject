import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import board, search_major

major1 = '컴퓨터과학과'
word_list = []
index = 0

#for bbs in board.objects.all():
#    w = search_major.objects.filter(board_number=bbs, major=major1)

#data.append()
