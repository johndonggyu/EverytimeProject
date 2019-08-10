import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
import django
import sys
sys.path.append('..')
django.setup()
from Web.models import lecture_evaluation, Eval, smu_professor, lecture_time, professor_keyword
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib
from matplotlib import cm
from matplotlib import font_manager, rc
from matplotlib import style
from matplotlib import rcParams
import pandas as pd
from matplotlib.patches import Circle, Wedge, Rectangle

#추가로 불러온 부분 2019-07-24
import re
from konlpy.tag import Kkma
import time
from operator import eq
import itertools
from collections import Counter
from PIL import Image

#===========================================#
#               global variables            #
#===========================================#
dir_static = '../Web/static/chart/'
#===========================================#

sns.set(style="whitegrid", context="talk")
rs = np.random.RandomState(8)

font_name = font_manager.FontProperties(fname="./raw_data/fonts/malgun.ttf").get_name()
rc('font', family=font_name)
style.use('ggplot')


def get_tokens(match_, match2_):
#교수님별로
    match_lect = lecture_time.objects.filter(professor__professor=match_,professor__major=match2_)
    #교수님과 교수님 전공에 해당하는 시간표 객체에 들어있는 데이터 불러오기
    match_eval = lecture_evaluation.objects.filter(professor__professor__professor=match_)
    #교수님의 이름과 매치하는 강의 평가 데이터 가져오기
    lect = []
    for a in match_lect:
        lect.append(a.lecture)
        #lect에다가 교수님 시간표로부터 강의명만 가져오기
    c = []
    #print("---------------------")
    print(match_)
    for item in match_eval:
        if(item.professor.lecture in lect):
            #강의평가 데이터에 있는 강의명이 시간표로부터 가져온 강의명과 일치하다면?
            c.append(item)
            #이렇게 하면 일치하고 있는 강의명을 가진 강의 평가 데이터가 c라는 튜플에 추가 될것이다
            #print(item.professor.lecture)
            #실제로 해당 강의 평가 데이터들의 강의명이 들어가있는지 한번 확인해보자.
    #print("---------------------")
    return c

#########################################################
#######################실제 파일 실행 부분 ###############
#smu_professor 에서 이름, 학과 꺼내오기.
    #for yo in smu_professor.objects.all():
each_Professor_classess = list()
objective_list = list()
for yo in smu_professor.objects.filter(major='컴퓨터과학과'):
    each_Professor_classess = get_tokens(yo.professor, yo.major)
    objective_list.append(each_Professor_classess)

#print(objective_list[0])
#[<lecture_evaluation: 강상욱 - 선형대수학>, <lecture_evaluation: 강상욱 - 보안프로그래밍>, <lecture_evaluation: 강상욱 - 캡스톤디자인I>, <lecture_evaluation: 강상욱 - 디지털신호처리>, <lecture_evaluation: 강상욱 - 정보보호>, <lecture_evaluation: 강상욱 - 선형대수학>, <lecture_evaluation: 강상욱 - 보안프로그래밍>, <lecture_evaluation: 강상욱 - 캡스톤디자인I>, <lecture_evaluation: 강상욱 - 디지털신호처리>, <lecture_evaluation: 강상욱 - 정보보호>]

#print(objective_list[0][0]) # 강상욱 - 선형대수학
#print(objective_list[0][0].professor.professor.professor) # 강상욱
#print(objective_list[0][0].professor.lecture) # 선형대수학
#print(len(objective_list[0])) # 10
# ---------------------
# 조용주 <---- each_Professor_classess.professor.professor.professor
# 프로그래밍언어론 <-------
# 캡스톤디자인I
# 캡스톤디자인II
# 프로그래밍2
# C프로그래밍1
# 파이썬프로그래밍
# 프로그래밍언어론
# 캡스톤디자인I
# 캡스톤디자인II
# 프로그래밍2
# C프로그래밍1
# 파이썬프로그래밍
# ---------------------

#------------------------------------------------------------------------------
def get_tokens_for_charts(each_Professor): #추후 구현 type_ =3, match_ = 한종배 교수님
    tokens = list() #토큰을 리스트 형태로 생성
    #카운트 올릴 변수들 초기화
    assignmentMany = 0
    assignmentNorm = 0
    assignmentNone = 0
    #함수 중요 변수 및 메서드
    everytime_data = each_Professor #강의평에 들어있는 1|소프트웨어공학|한종대|3.5|보통|보통|비율 채워줌|직접호명|두 번등을 객체화 시킴
    print()
    #교수님 평균 별점 계산하는 함수
    if len(everytime_data) <= 0:
        print('db가 비었습니다 : from get_tokens()')
        return 0
    #교수님 과제분량 어떤지 확인하는 함수
    for datum in everytime_data: #객체화 시킨 데이터들을 한줄씩 불러 읽음
        strAssignment = datum.assignment #교수님 과제분량 많음?
        if strAssignment == '많음':
            assignmentMany+=1
        elif strAssignment == '보통':
            assignmentNorm+=1
        elif strAssignment == '없음':
            assignmentNone+=1
    print(everytime_data[0].professor.professor.professor+"교수님 과제 분량")
    print ("많음 : %d" % (assignmentMany))
    print ("보통 : %d" % (assignmentNorm))
    print ("없음 : %d" % (assignmentNone))
    print()
    tokens.append(assignmentMany)
    tokens.append(assignmentNorm)
    tokens.append(assignmentNone)
    return tokens

#1차원 배열로 token안에 변수들값이 저장이 됨

#2. 과제 비율 계산 변수 assignmentMany assignmentNorm assignmentNone , index [0-2] 차트 완료
def draw_barPlot_professor_Assignment(each_Professor):
    alist = get_tokens_for_charts(each_Professor)
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_barPlot_professor_Assignment()')
            return 0
    list_assignment= [int(i) for i in alist]
    ds_assignment=[
        {'설문조사':1, '과제':'많음', '학생 응답 수':list_assignment[0]},
        {'설문조사':2, '과제':'보통', '학생 응답 수':list_assignment[1]},
        {'설문조사':3, '과제':'없음', '학생 응답 수':list_assignment[2]}
                    ]
    df_assignment = pd.DataFrame(ds_assignment)
    sns.barplot(x="과제", y="학생 응답 수",palette="Set2", data=df_assignment, linewidth=2.5, edgecolor=".2");
    plt.title(each_Professor[0].professor.professor.professor+' 과제 분량') #차트에 제목 붙이기
    outputfile_name = dir_static+each_Professor[0].professor.professor.professor+" assignment.png"
    plt.savefig(outputfile_name)
     #차트 이미지로 저장하기
    plt.show()

#-----------------------------------------------------------------------------------
for i in range(0, len(objective_list)):
    draw_barPlot_professor_Assignment(objective_list[i])
