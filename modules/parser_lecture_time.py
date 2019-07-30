import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
from operator import eq
import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import lecture_time, smu_professor
from multiprocessing import Pool
from urllib import parse
import urllib.request
from selenium import webdriver

if(smu_professor.objects.count() == 0):
	Exception("get_smu_professor.py 부터 먼저 실행해주세요.")

if(lecture_time.objects.count() != 0):
	print('이전데이터는 지워집니다.')
	lecture_time.objects.all().delete()

start_time = time.time()

colleges = []
year = []
sem = []
#2019-1 (0)
year.append(2019)
sem.append(1)
colleges.append([ (155973, '게임학과') , (155977,'생명공학과'), (155979,'전기공학과'), (155984,'컴퓨터과학과'), 
               (155985, '화공신소재학과'),(155986,'화학에너지공학과'), (161320, '융합전자공학과'), (161321,'휴먼지능정보공학과'),
               (155966, '교육학과'), (155967,'국어교육과'), (155969,'수학교육과'), (155970,'영어교육과'),
               (155938,'경영학부'), (155939,'경제금융학부'), (155940,'글로벌경영학과'), (155947,'융합경영학과'),
               (155955,'생활예술학과'), (155957, '스포츠건강관리학과'), (155958,'식품영양학과'), (155962,'의류학과'),
               (155963,'조형예술학과'), (161318,'무용예술학과'), (161319,'음악학부'),
               (155988,'가족복지학과'), (155990,'공간환경학부'), (155991,'공공인재학부'), (155992,'국가안보학과'),
               (155993,'문헌정보학과'), (155997,'역사콘텐츠학과'), (156000,'지적재산권학과'), (156002,'한일문화콘텐츠학과'),
               (155933, '계당교양교육원'),  (155934, '계당교양교육원'), (155935, '계당교양교육원'), (155936, '계당교양교육원')])
                #교선                        #교직                        #교필                       #일선
#2018-2 (1)
year.append(2018)
sem.append(2)
colleges.append([ (137290, '게임학과') , (137294,'생명공학과'), (137296,'전기공학과'), (137298,'컴퓨터과학과'), 
               (137299, '화공신소재학과'),(137300,'화학에너지공학과'), (137295, '융합전자공학과'), (137301,'휴먼지능정보공학과'),
               (137283, '교육학과'), (137284,'국어교육과'), (137286,'수학교육과'), (137287,'영어교육과'),
               (137258,'경영학부'), (137259,'경제금융학부'), (137261,'글로벌경영학과'), (137266,'융합경영학과'),
               (137272,'생활예술학과'), (137274, '스포츠건강관리학과'), (137275,'식품영양학과'), (137279,'의류학과'),
               (137280,'조형예술학과'), (137269,'무용예술학과'), (137278,'음악학부'),
               (137303,'가족복지학과'), (137305,'공간환경학부'), (137306,'공공인재학부'), (137307,'국가안보학과'),
               (137308,'문헌정보학과'), (137312,'역사콘텐츠학과'), (137315,'지적재산권학과'), (137316,'한일문화콘텐츠학과'),
               (137252, '계당교양교육원'),  (137253, '계당교양교육원'), (137254, '계당교양교육원'), (137255, '계당교양교육원')])
                #교선                        #교직                        #교필                       #일선
#2018-1 (2)
year.append(2018)
sem.append(1)
colleges.append([ (38877, '게임학과') , (38881,'생명공학과'), (38898,'전기공학과'), (38911,'컴퓨터과학과'), 
               (38917, '화공신소재학과'),(38923,'화학에너지공학과'), (38892, '융합전자공학과'), (38926,'휴먼지능정보공학과'),
               (38875, '교육학과'), (38880,'국어교육과'), (38885,'수학교육과'), (38890,'영어교육과'),
               (38867,'경영학부'), (38870,'경제금융학부'), (38876,'글로벌경영학과'), (38882,'융합경영학과'),
               (38889,'생활예술학과'), (38909, '스포츠건강관리학과'), (38894,'식품영양학과'), (38899,'의류학과'),
               (38919,'조형예술학과'), (38874,'무용예술학과'), (38914,'음악학부'),
               (38878,'가족복지학과'), (38883,'공간환경학부'), (38887,'공공인재학부'), (38891,'국가안보학과'),
               (38896,'문헌정보학과'), (38910,'역사콘텐츠학과'), (38925,'지적재산권학과'), (38930,'한일문화콘텐츠학과'),
               (38865, '계당교양교육원'),  (38864, '계당교양교육원'), (38868, '계당교양교육원'), (38866, '계당교양교육원')])
                #교선                        #교직                        #교필                       #일선

major_list = []
lecture_list = []
professor_list = []

## 로그인할 유저정보를 넣어줍시다. (모두 문자열입니다)
LOGIN_INFO = {
    'userid': 'johndonggyu',
    'password': 'everytime1234!@#$'
}

LOGIN_INFO = {**LOGIN_INFO}
#print(LOGIN_INFO)
with requests.Session() as s:    
    login_req = s.post('https://everytime.kr/user/login', data=LOGIN_INFO)
    print(login_req.status_code)
    if login_req.status_code != 200:
        raise Exception('LOGIN ERROR !')
    index = 0
    for college in colleges:
        for cid in college:
            sn = 0
            while (True):
                lectime = s.get('https://everytime.kr/find/timetable/subject/list?categoryId='+str(cid[0])+'&campusId=25&year='+str(year[index])+'&semester='+str(sem[index])+'&limitNum=50&startNum='+str(sn))
                #print(jagae.text)

                e = ET.fromstring(lectime.text)
                if(not e):
                    break
                for subj in e.iter('subject'):
                    major_list.append(cid[1])
                    lecture_list.append(subj.attrib['name'])
                    professor_list.append(subj.attrib['professor'])
                sn += 50
        index+=1

data = []

#비효율적
for i in range(0, len(major_list)):
	data.append([])
	data[i].append(major_list[i])
	data[i].append(lecture_list[i])
	data[i].append(professor_list[i])

for a in data:
	#print(a[0], a[1], a[2])
	try:
		sp = smu_professor.objects.get(major=a[0],professor=a[2])
		lecture_time(lecture=a[1], professor=sp).save()
	except Exception as e:
		#print(e)
		pass
print("--- %s seconds ---" % (time.time() - start_time))