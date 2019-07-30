# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import colleges,majors

if(colleges.objects.count() != 0):
	print('테이블을 지우고 다시 실행하겠습니다.')
	colleges.objects.all().delete()
	majors.objects.all().delete()

colleges(college='인문사회과학대학').save()
colleges(college='사범대학').save()
colleges(college='경영경제대학').save()
colleges(college='융합공과대학').save()
colleges(college='문화예술대학').save()
colleges(college='계당교양교육원').save()

c = colleges.objects.get(college='인문사회과학대학')
majors(college=c,major='역사콘텐츠학과').save()
majors(college=c,major='지적재산권학과').save()
majors(college=c,major='문헌정보학과').save()
majors(college=c,major='공간환경학부').save()
majors(college=c,major='공공인재학부').save()
majors(college=c,major='가족복지학과').save()
majors(college=c,major='국가안보학과').save()

c = colleges.objects.get(college='사범대학')
majors(college=c,major='국어교육과').save()
majors(college=c,major='영어교육과').save()
majors(college=c,major='교육학과').save()
majors(college=c,major='수학교육과').save()

c = colleges.objects.get(college='경영경제대학')
majors(college=c,major='경제금융학부').save()
majors(college=c,major='경영학부').save()
majors(college=c,major='글로벌경영학과').save()
majors(college=c,major='융합경영학과').save()

c = colleges.objects.get(college='융합공과대학')
majors(college=c,major='휴먼지능정보공학과').save()
majors(college=c,major='전기공학과').save()
majors(college=c,major='융합전자공학과').save()
majors(college=c,major='컴퓨터과학과').save()
majors(college=c,major='생명공학과').save()
majors(college=c,major='화학에너지공학과').save()
majors(college=c,major='화공신소재학과').save()
majors(college=c,major='게임학과').save()

c = colleges.objects.get(college='문화예술대학')
majors(college=c,major='식품영양학과').save()
majors(college=c,major='의류학과').save()
majors(college=c,major='스포츠건강관리학과').save()
majors(college=c,major='무용예술학과').save()
majors(college=c,major='조형예술학과').save()
majors(college=c,major='생활예술학과').save()
majors(college=c,major='음악학부').save()

c = colleges.objects.get(college='계당교양교육원')
majors(college=c,major='').save()

print('모두 저장되었습니다.')