# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import major_synonym

###### 학과 별 유의단어 설정하여 major_synonym 테이블에 저장하는 코드입니다. 
## 자음으로 이루어진 학과이름은 고려하지 않았습니다. 
## 아이디어 있으시면 추가바랍니다.
if(major_synonym.objects.count() != 0):
	print('테이블을 지우고 다시 실행하겠습니다.')
	major_synonym.objects.all().delete()

major_synonym(major='게임학과',synonym='게임학과|게임학|겜학과').save()
major_synonym(major='생명공학과',synonym='생명공학과|생명공학|생명학과').save()
major_synonym(major='전기공학과',synonym='전기공학과|전기공학|전기과').save()
major_synonym(major='컴퓨터과학과',synonym='컴퓨터과학과|컴퓨터과학|컴과').save()
major_synonym(major='화공신소재학과',synonym='화공신소재학과|화공과|화공신소재|화공').save()
major_synonym(major='화학에너지공학과',synonym='화학에너지공학과|화학과|화학에너지').save()
major_synonym(major='융합전자공학과',synonym='융합전자공학과|융전|융합전자공학').save()
major_synonym(major='휴먼지능정보공학과',synonym='휴먼지능정보공학과|휴지|휴먼지능학과|휴먼지능과').save()
major_synonym(major='교육학과',synonym='교육학과|교육과').save()
major_synonym(major='국어교육과',synonym='국어교육과|국어과|국교|국교과').save()
major_synonym(major='수학교육과',synonym='수학교육과|수교과|수교').save()
major_synonym(major='영어교육과',synonym='영어교육과|영교과|영교').save()
major_synonym(major='경영학부',synonym='경영학부').save()
major_synonym(major='경제금융학부',synonym='경제금융학부|경금|경금학부|경제금융').save()
major_synonym(major='글로벌경영학과',synonym='글로벌경영학과|글경|글경학과|글경과').save()
major_synonym(major='융합경영학과',synonym='융합경영학과|융경|융합경영').save()
major_synonym(major='생활예술학과',synonym='생활예술학과|생예과|생활예술|생활예술학').save()
major_synonym(major='스포츠건강관리학과',synonym='스포츠건강관리학과|스포츠건강|스건과|스건').save()
major_synonym(major='식품영양학과',synonym='식품영양학과|식품영양|식영과|식영').save()
major_synonym(major='의류학과',synonym='의류학과|의류학').save()
major_synonym(major='조형예술학과',synonym='조형예술학과|조예과|조형예술과|조형예술').save()
major_synonym(major='무용예술학과',synonym='무용예술학과|무용과|무용예술|무용예술학').save()
major_synonym(major='음악학부',synonym='음악학부|음악학과').save()
major_synonym(major='가족복지학과',synonym='가족복지학과|가복과|가복|가족복지|가족복지학').save()
major_synonym(major='공간환경학부',synonym='공간환경학부|공간환경|공간환경학과|공환과').save()
major_synonym(major='공공인재학부',synonym='공공인재학부|공공인재').save()
major_synonym(major='국가안보학과',synonym='국가안보학과|국가안보학|국가안보').save()
major_synonym(major='문헌정보학과',synonym='문헌정보학과|문헌정보|문헌정보학|문정과|문정').save()
major_synonym(major='역사콘텐츠학과',synonym='역사콘텐츠학과|역콘과|역콘|역사콘텐츠학|역사콘텐츠').save()
major_synonym(major='지적재산권학과',synonym='지적재산권학과|지적재산학|지적재산|지재과|지재').save()
major_synonym(major='한일문화콘텐츠학과',synonym='한일문화콘텐츠학과|한문콘|한문콘과|한일문화콘텐츠|한콘').save()
major_synonym(major='계당교양교육원',synonym='계당교양교육원|계당교양|계당교양교육|교양').save()
