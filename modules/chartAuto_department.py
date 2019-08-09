import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
import django
django.setup()
import sys
from backend.parsed_data.models import lecture_evaluation, Eval, smu_professor, lecture_time, professor_keyword
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


########################### 현재 test2.py에서 실험중.

#===========================================#
#               global variables            #
#===========================================#
dir_static = './Web/static/chart/'
#===========================================#

sns.set(style="whitegrid", context="talk")
rs = np.random.RandomState(8)

font_name = font_manager.FontProperties(fname="./modules/raw_data/fonts/malgun.ttf").get_name()
rc('font', family=font_name)
style.use('ggplot')


############################이하 현재 코드 작동하는 부분.#######################################

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
    #print(match_)
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


major = ['역사콘텐츠학과','지적재산학과','문헌정보학과','공간환경학부','공공인재학부','가족복지학과','국가안보학과','국어교육과','영어교육과','교육학과','수학교육과','경제금융학부','경영학부','글로벌경영학과','융합경영학과','휴먼지능정보공학과','전기공학과','융합전자공학과','컴퓨터과학과','생명공학과','화학에너지공학과','화공신소재학과','게임학과','식품영양학과','의류학과','스포츠건강관리학과','무용예술학과','조형예술학과','생활예술학과','음악학부','계당교양교육원']

major_list = ()
each_Professor_classess = list() #각 교수님의 강의명 리스트
objective_list = list() #목표로 채우려는 교수님 with 강의명 리스트
print(len(major))
print(major[0])
for i in range(0, len(major)):
    for yo in smu_professor.objects.filter(major=major[i]):
        each_Professor_classess = get_tokens(yo.professor, yo.major)
        objective_list.append(each_Professor_classess)
    print(objective_list[0])
    major_list[i].append(objective_list)

def get_tokens_for_chart_department(each_Professor): #추후 구현 type_ =3, match_ = 한종배 교수님
    tokens = list() #토큰을 리스트 형태로 생성
    #카운트 올릴 변수들 초기화
    nOfclasses=0
    #교수님 총점 평균 계산
    sumScore = 0
    averageScore =0
    #과제 비율 계산 변수
    assignmentMany = 0
    assignmentNorm = 0
    assignmentNone = 0
    #조모임 계산 변수
    team_projectMany = 0
    team_projectNorm = 0
    team_projectNone = 0
    #학점 비율 계산 변수
    creditGod = 0
    creditProportion = 0
    creditTough = 0
    creditFbomb = 0
    #출결 어떤지 계산 변수
    attendanceMix = 0
    attendanceDirect = 0
    attendanceDesignated = 0
    attendanceElectronic = 0
    attendanceNone = 0
    #시험 횟수 많은지 계산 변수
    test4above = 0
    test3 = 0
    test2 = 0
    test1 = 0
    testNone = 0
    #함수 중요 변수 및 메서드
    everytime_data = each_Professor
    print()
    #교수님 평균 별점 계산하는 함수
    if len(everytime_data) <= 0:
        print('db가 비었습니다 : from get_tokens()')
        return 0
    for datum in everytime_data: #객체화 시킨 데이터들을 한줄씩 불러 읽음
        floatScore1 = datum.score #교수님 별점
        nOfclasses+=1
        if floatScore1 == 0.0:
            nOfclasses-=1 #0.0은 포함이 되지 않아야 하므로 각 교수님 수업의 개수에서 제외
        sumScore += floatScore1
    averageScore = sumScore / nOfclasses #교수님 평균 별점
    print (everytime_data[0].professor.professor.major+" 교수님 평균 별점 : %.2f" %(averageScore))
    print()
    tokens.append(averageScore)
    #교수님 과제분량 어떤지 확인하는 함수
    for datum in everytime_data: #객체화 시킨 데이터들을 한줄씩 불러 읽음
        strAssignment = datum.assignment #교수님 과제분량 많음?
        if strAssignment == '많음':
            assignmentMany+=1
        elif strAssignment == '보통':
            assignmentNorm+=1
        elif strAssignment == '없음':
            assignmentNone+=1
    print(everytime_data[0].professor.professor.major+" 과제 분량")
    print ("많음 : %d" % (assignmentMany))
    print ("보통 : %d" % (assignmentNorm))
    print ("없음 : %d" % (assignmentNone))
    print()
    tokens.append(assignmentMany)
    tokens.append(assignmentNorm)
    tokens.append(assignmentNone)
    #교수님 교수님 팀플이 평소에 많은지 확인하는 함수
    for datum in everytime_data: #객체화 시킨 데이터들을 한줄씩 불러 읽음
        strTeam_project = datum.team_project # 교수님 팀플 많이 내주심?
        if strTeam_project == '많음':
            team_projectMany+=1
        elif strTeam_project == '보통':
            team_projectNorm+=1
        elif strTeam_project == '없음':
            team_projectNone+=1
    print(everytime_data[0].professor.professor.major+" 팀플 분량")
    print ("많음 : %d" % (team_projectMany))
    print ("보통 : %d" % (team_projectNorm))
    print ("없음 : %d" % (team_projectNone))
    print()
    tokens.append(team_projectMany)
    tokens.append(team_projectNorm)
    tokens.append(team_projectNone)
    #교수님 학점을 잘 주시는지 확인하는 함수
    for datum in everytime_data: #객체화 시킨 데이터들을 한줄씩 불러 읽음
        strCredit = datum.credit # 교수님 학점 잘주심? F폭격기임?
        if strCredit == '학점느님':
            creditGod+=1
        elif strCredit == '비율 채워줌':
            creditProportion+=1
        elif strCredit == '매우 깐깐함':
            creditTough+=1
        elif strCredit == 'F폭격기':
            creditFbomb+=1
    print(everytime_data[0].professor.professor.major+" 학점 비율")
    print ("학점느님 : %d" % (creditGod))
    print ("비율채워줌 : %d" % (creditProportion))
    print ("매우깐깐함 : %d" % (creditTough))
    print ("F폭격기 : %d" % (creditFbomb))
    print()
    tokens.append(creditGod)
    tokens.append(creditProportion)
    tokens.append(creditTough)
    tokens.append(creditFbomb)
    #교수님이 출결을 평소에 어떻게 부르시는가
    for datum in everytime_data: #객체화 시킨 데이터들을 한줄씩 불러 읽음
       strAttendance = datum.attendance #출결 체크는 어떻게 하시는가?
       if strAttendance == '혼용':
            attendanceMix+=1
       elif strAttendance == '직접호명':
            attendanceDirect+=1
       elif strAttendance == '지정좌석':
            attendanceDesignated+=1
       elif strAttendance == '전자출결':
            attendanceElectronic+=1
       elif strAttendance == '반영안함':
            attendanceNone+=1
    print(everytime_data[0].professor.professor.major+" 출결 어떻게 부르나요")
    print ("혼용 : %d" % (attendanceMix))
    print ("직접호명 : %d" %(attendanceDirect))
    print ("지정좌석 : %d" % (attendanceDesignated))
    print ("전자출결 : %d" % (attendanceElectronic))
    print ("반영안함 : %d" % (attendanceNone))
    print()
    tokens.append(attendanceMix)
    tokens.append(attendanceDirect)
    tokens.append(attendanceDesignated)
    tokens.append(attendanceElectronic)
    tokens.append(attendanceNone)
    #교수님 시험의 몇번 치루나요?
    for datum in everytime_data: #객체화 시킨 데이터들을 한줄씩 불러 읽음
        strTest = datum.test #교수님 시험의 몇번 치루나요?
        if strTest == '네번이상':
            test4above+=1
        elif strTest == '세 번':
            test3+=1
        elif strTest == '두 번':
            test2+=1
        elif strTest == '한 번':
            test1+=1
        elif strTest == '없음':
            testNone+=1
    print(everytime_data[0].professor.professor.major+" 강의별 시험 횟수")
    print ("네번이상 : %d" % (test4above))
    print ("세번 : %d" % (test3))
    print ("두번 : %d" % (test2))
    print ("한번 : %d" % (test1))
    print ("없음 : %d" % (testNone))
    print()
    tokens.append(test4above)
    tokens.append(test3)
    tokens.append(test2)
    tokens.append(test1)
    tokens.append(testNone)
    return tokens

#1차원 배열로 token안에 변수들값이 저장이 됨
#1. 교수님 총점 평균 계산 averageScore , index [0] 별모양으로 만듦
#2. 과제 비율 계산 변수 assignmentMany assignmentNorm assignmentNone , index [1-3] 차트 완료
#3. 조모임 계산 변수 team_projectMany team_projectNorm  team_projectNone , index [4-6] 차트 완료
#4. 학점 비율 계산 변수 creditGod  creditProportion  creditTough  creditFbomb , index [7-10]
#5  출결 어떤지 계산 변수 attendanceMix attendanceDirect  attendanceDesignated attendanceElectronic attendanceNone , index [11-15]
#6. 시험 횟수 많은지 계산 변수 test4above test3 test2 test1 testNone , index [16-20]

def draw_piechart_assignment_and_teamProject():
    alist = get_tokens_for_chart_department(each_Professor)
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_piechart_assignment_and_teamProject()')
            return 0
    labels = ['많음', '보통','없음']
    titles = ['컴퓨터과학과 과제 분량', '컴퓨터과학과 팀플 분량']
    data   = [[alist[1], alist[2], alist[3]], # 과제
              [alist[4], alist[5], alist[6]]] # 팀플

    #### 2. matplotlib의 figure 및 axis 설정
    rcParams.update({'font.size': 10})
    fig, axes = plt.subplots(1,2,figsize=(10,5))
    plt.subplots_adjust(wspace=0.5) # subplot간의 너비 간격 조절

    #### 3. 각 subplot에 pie plot 그리기
    explode = (0, 0.1, 0) # 퍼짐 정도 조절
    for i in range(2):
        ax = axes[i] # subplot 선택
        wedges, texts, autotexts = ax.pie(data[i], explode=explode, labels=labels,
                                          autopct='%1.1f%%', pctdistance=0.85,
                                          shadow=True, startangle=90)
        for w in wedges: # 조각 설정
            w.set_linewidth(0)
            w.set_edgecolor('w')

        for t in texts: # label 설정
            t.set_color('k')
            t.set_fontsize(12)

        for a in autotexts: # 퍼센티지 설정
            a.set_color('k')
            a.set_fontsize(10)
        '''
        NOTE. 아래의 2줄은 파이차트를 도넛차트로 보이게끔 하는 trick임
        '''
        centre_circle = plt.Circle((0,0), 0.70, color='black', fc='white', linewidth=0)
        ax.add_artist(centre_circle)

        ax.set_title(titles[i])
        ax.axis('equal')

    #### 4. 그래프 저장하고 출력하기
    plt.savefig('./frontend/static/chart/'+each_Professor[0].professor.professor.major+' ex_pieplot.png', format='png', dpi=400)
    plt.show()

def draw_barPlot_professor_Assignment():
    alist = get_tokens_for_chart_department(each_Professor)
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_barPlot_professor_Assignment()')
            return 0
    list_assignment= [int(i) for i in alist]
    ds_assignment=[
        {'설문조사':1, '과제':'많음', '학생 응답 수':list_assignment[1]},
        {'설문조사':2, '과제':'보통', '학생 응답 수':list_assignment[2]},
        {'설문조사':3, '과제':'없음', '학생 응답 수':list_assignment[3]}
                    ]
    df_assignment = pd.DataFrame(ds_assignment)
    sns.barplot(x="과제", y="학생 응답 수",palette="Set2", data=df_assignment, linewidth=2.5, edgecolor=".2");
    plt.title(objective_list[0].professor.professor.major+' 과제 분량') #차트에 제목 붙이기
    outputfile_name = dir_static+everytime_data[0].professor.professor.major+" bar_chart_professor_Assignment.png"
    plt.savefig(outputfile_name)
     #차트 이미지로 저장하기
    plt.show()

def draw_barPlot_professor_TeamProject():
    alist = get_tokens_for_chart_department(each_Professor)
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_barPlot_professor_TeamProject()')
            return 0
    list_assignment= [int(i) for i in alist]
    ds_TeamProject=[ #index [4-6]
        {'설문조사':1, '팀플':'많음', '학생 응답 수':list_assignment[4]},
        {'설문조사':2, '팀플':'보통', '학생 응답 수':list_assignment[5]},
        {'설문조사':3, '팀플':'없음', '학생 응답 수':list_assignment[6]}
                    ]
    df_TeamProject = pd.DataFrame(ds_TeamProject)
    sns.barplot(x="팀플", y="학생 응답 수",palette="Set2", data=df_TeamProject, linewidth=2.5, edgecolor=".2");
    plt.title(objective_list[0].professor.professor.major+' 팀플 비율') #차트에 제목 붙이기
    outputfile_name = dir_static+each_Professor[0].professor.professor.major+" bar_chart_professor_TeamProject.png"
    plt.savefig(outputfile_name)
     #차트 이미지로 저장하기
    plt.show()

def draw_barPlot_professor_Credit():
    alist = get_tokens_for_chart_department(each_Professor)
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_barPlot_professor_Credit()')
            return 0
    list_assignment= [int(i) for i in alist]
    ds_Credit=[ #index [7-10]
        {'설문조사':1, '학점':'학점느님', '학생 응답 수':list_assignment[7]},
        {'설문조사':2, '학점':'비율 채워줌', '학생 응답 수':list_assignment[8]},
        {'설문조사':3, '학점':'매우깐깐함', '학생 응답 수':list_assignment[9]},
        {'설문조사':4, '학점':'F폭격기', '학생 응답 수':list_assignment[10]}
                    ]
    df_Credit = pd.DataFrame(ds_Credit)
    sns.barplot(x="학점", y="학생 응답 수",palette="Set2", data=df_Credit, linewidth=2.5, edgecolor=".2");
    plt.title(objective_list[0].professor.professor.major+' 학점 비율') #차트에 제목 붙이기
    outputfile_name = dir_static+each_Professor[0].professor.professor.major+" bar_chart_professor_Credit.png"
    plt.savefig(outputfile_name)
    plt.show()

def draw_barPlot_professor_Attendence():
    alist = get_tokens_for_chart_department(each_Professor)
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_barPlot_professor_Attendence()')
            return 0
    list_assignment= [int(i) for i in alist]
    ds_Attendence=[ #index [11-15]
        {'설문조사':1, '출결':'혼용', '학생 응답 수':list_assignment[11]},
        {'설문조사':2, '출결':'직접호명', '학생 응답 수':list_assignment[12]},
        {'설문조사':3, '출결':'지정좌석', '학생 응답 수':list_assignment[13]},
        {'설문조사':4, '출결':'전자출결', '학생 응답 수':list_assignment[14]},
        {'설문조사':5, '출결':'반영안함', '학생 응답 수':list_assignment[15]}
                    ]
    df_Attendence = pd.DataFrame(ds_Attendence)
    sns.barplot(x="출결", y="학생 응답 수",palette="Set2", data=df_Attendence, linewidth=2.5, edgecolor=".2");
    plt.title(objective_list[0].professor.professor.major+' 출결 비율') #차트에 제목 붙이기
    outputfile_name = dir_static+each_Professor[0].professor.professor.major+" bar_chart_professor_Attendence.png"
    plt.savefig(outputfile_name)
    plt.show()

def draw_barPlot_professor_Test():
    alist = get_tokens_for_chart_department(each_Professor)
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_barPlot_professor_Test()')
            return 0
    list_assignment= [int(i) for i in alist]
    ds_Test=[ #index [16-20]
        {'설문조사':1, '시험 몇 번':'네번이상', '학생 응답 수':list_assignment[16]},
        {'설문조사':2, '시험 몇 번':'세 번', '학생 응답 수':list_assignment[17]},
        {'설문조사':3, '시험 몇 번':'두 번', '학생 응답 수':list_assignment[18]},
        {'설문조사':4, '시험 몇 번':'한 번', '학생 응답 수':list_assignment[19]},
        {'설문조사':5, '시험 몇 번':'없음', '학생 응답 수':list_assignment[20]}
                    ]
    df_Test = pd.DataFrame(ds_Test)
    sns.barplot(x="시험 몇 번", y="학생 응답 수",palette="Set2", data=df_Test, linewidth=2.5, edgecolor=".2");
    plt.title(objective_list[0].professor.professor.major+' 시험 비율') #차트에 제목 붙이기
    outputfile_name = dir_static+each_Professor[0].professor.professor.major+" bar_chart_professor_Test.png"
    plt.savefig(outputfile_name)
    plt.show()

#some function definitions
#밑에 두 함수는, 기초 삼각기하학을 통해 게이지의 섹터 (Wedge)를 그릴수 있도록 하기 위해 필요한 함수들이고, 화살표로 하여금 올바른 섹터를 가리킬수 있게끔 도와줍니다.
def degree_range(n):
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint = True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points
def rot_text(ang):
    rotation = np.degrees(np.radians(ang) * np.pi /np.pi -np.radians(90))
    return rotation
#메인 게이지 함수
def gauge(each_Professor, labels=['LOW','MEDIUM','HIGH','VERY HIGH','EXTREME'], \
          colors='jet_r', arrow=1, title='', fname=False):
    alist=get_tokens_for_chart_department(each_Professor) #db랑 연동시켜
    list_arrow= [int(i) for i in alist]
    arrow = list_arrow[0]+1 #db랑 연동시킨 교수님의 평균점수를 정수화 시켜서 게이지에 5단계로 표시시켜본다.
    """
    some sanity checks first
    sanity가 무슨말인지 모르지만 일단 먼저 체크를 하시겠데!
    sanity : reasonable and rational behavior
    사전 정의로 봐선, 변수가 함수에 알맞게 들어왔는지 확인하는 부분인 것으로 보인다.
    """
    N = len(labels) #레이블의 개수
    if arrow > N: #화살표가 레이블보단 클 수 없으니까 크면 에러가 뜨겠지
        raise Exception("\n\nThe category ({}) is greated than \
        the length\nof the labels ({})".format(arrow, N))
    """
    if colors is a string, we assume it's a matplotlib colormap
    and we discretize in N discrete colors
    컬러가 문자열이면, matplot라이브러리의 컬러맵을 사용한다고 생각하고 N개의 분리된 색깔로 분리화 시킨다네여!
    """
    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(np.arange(N))
        colors = cmap[::-1,:].tolist()
    if isinstance(colors, list):
        if len(colors) == N:
            colors = colors[::-1]
        else:
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors), N))
    """
    begins the plotting
    그림 그리기를 시작합니다.
    """
    fig, ax = plt.subplots()
    ang_range, mid_points = degree_range(N)
    labels = labels[::-1]
    """
    plots the sectors and the arcs
    섹터들하고 아크.. 이걸 한국어로 뭐라하지 아크를 그려보자!
    """
    patches = []
    for ang, c in zip(ang_range, colors):
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))
    [ax.add_patch(p) for p in patches]
    """
    set the labels (e.g. 'LOW','MEDIUM',...)
    이제 레이블을 세팅한다.
    """
    for mid, lab in zip(mid_points, labels):
        ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=14, \
            fontweight='bold', rotation = rot_text(mid))
        #딱보니 가로 및 세로 중앙정렬 폰트 크기는 14, 글씨두께 굵게하고, 글자는 섹터의 각도 중앙값에 맞게 돌아가게 하는듯.
    """
    set the bottom banner and the title
    사실상 차트의 타이틀을 세팅하는 부분.
    """
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='w', lw=2)
    ax.add_patch(r)
    averageRate_modified = round(alist[0],2)
    ax.text(0, -0.05, title+' : '+str(averageRate_modified)+' star(s)', horizontalalignment='center', \
         verticalalignment='center', fontsize=22, fontweight='bold')
    """
    plots the arrow now
    게이지 화살표를 그려보겠다능
    """
    pos = mid_points[abs(arrow - N)]
    ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))
    """
    removes frame and ticks, and makes axis equal and tight
    프레임 지우고, 틱도 지우고, 축을 동등하고 딱맞게 한다는말인데 뭐,, 여백의 미를 없앤다는 정도의 뜻으로 보임.
    """
    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    plt.tight_layout()
    plt.show()
    if fname:
        fig.savefig(fname, dpi=300)
#실제 프로그램 실행 공간
####################################################################
#draw_piechart_assignment_and_teamProject() #일단 성공함
#draw_piechart_credit_and_attendance() #0%글자 깨지는 관계로 보류
# draw_barPlot_professor_Assignment()
# draw_barPlot_professor_TeamProject()
# draw_barPlot_professor_Credit()
# draw_barPlot_professor_Attendence()
# draw_barPlot_professor_Test()
gauge(objective_list[0],labels=['0-1 star','1-2 stars','2-3 stars','3-4 stars','4-5 stars'], \
      colors='cool_r', arrow=3, title=objective_list[0][0].professor.professor.major+'교수님 만족도', fname = './frontend/static/chart/'+objective_list[0][0].professor.professor.major+'gaugeChart_professor_averageRate.png')
####################################################################
