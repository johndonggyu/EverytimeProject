import os
import sys
sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
import django
django.setup()
from Web.models import LectEvalData
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager, rc
from matplotlib import style
from matplotlib import rcParams
import pandas as pd

sns.set(style="whitegrid", context="talk")
rs = np.random.RandomState(8)

font_name = font_manager.FontProperties(fname="./raw_data/fonts/malgun.ttf").get_name()
rc('font', family=font_name)
style.use('ggplot')

def get_tokens(): #추후 구현 type_ =3, match_ = 한종배 교수님

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
    everytime_data = LectEvalData.objects.all() #강의평에 들어있는 1|소프트웨어공학|한종대|3.5|보통|보통|비율 채워줌|직접호명|두 번등을 객체화 시킴
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
    print ("한종대 교수님 평균 별점 : %.2f" %(averageScore))
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
    print("교수님 과제 분량")
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
    print("교수님 팀플 분량")
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
    print("교수님 학점 비율")
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
    print("교수님 출결 어떻게 부르시나요")
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
    print("교수님 시험 난이도")
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

def draw_chart_professor_assignment():
    alist = get_tokens()
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_chart_professor_assignment()')
            return 0
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    labels = '많음', '보통','없음'
    #labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    #3. 조모임 계산 변수 team_projectMany team_projectNorm  team_projectNone , index [4-6]
    sizes = [alist[4], alist[5], alist[6]]
    explode = (0, 0, 0.1)  # only "explode" the 3rd slice (i.e. '없음')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('./frontend/static/chart/bar_chart_professor_team_project.png') #차트 이미지로 저장하기
    plt.show()

def draw_piechart_assignment_and_teamProject():
    alist = get_tokens()
    if type(alist) == type(int):
        if alist <= 0:
            print('db가 비었습니다 : draw_piechart_assignment_and_teamProject()')
            return 0
    labels = ['많음', '보통','없음']
    titles = ['교수님 과제 분량', '교수님 팀플 분량']
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
    plt.savefig('./frontend/static/chart/ex_pieplot.png', format='png', dpi=400)
    plt.show()

def draw_barPlot_professor_Assignment():
    alist =get_tokens()
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
    plt.title('교수님 과제 분량') #차트에 제목 붙이기
    plt.savefig('./frontend/static/chart/bar_chart_professor_Assignment.png')
    plt.show()

def draw_barPlot_professor_TeamProject():
    alist =get_tokens()
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
    plt.title('교수님 팀플 비율') #차트에 제목 붙이기
    plt.savefig('./frontend/static/chart/bar_chart_professor_TeamProject.png')
    plt.show()

def draw_barPlot_professor_Credit():
    alist =get_tokens()
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
    plt.title('교수님 학점 비율') #차트에 제목 붙이기
    plt.savefig('./frontend/static/chart/bar_chart_professor_Credit.png')
    plt.show()

def draw_barPlot_professor_Attendence():
    alist =get_tokens()
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
    plt.title('교수님 출결 비율') #차트에 제목 붙이기
    plt.savefig('./frontend/static/chart/bar_chart_professor_Attendence.png')
    plt.show()

def draw_barPlot_professor_Test():
    alist =get_tokens()
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
    plt.title('교수님 시험 비율') #차트에 제목 붙이기
    plt.savefig('./frontend/static/chart/bar_chart_professor_Test.png')
    plt.show()
#실제 프로그램 실행 공간
####################################################################
#draw_piechart_assignment_and_teamProject() #일단 성공함
#draw_piechart_credit_and_attendance() #0%글자 깨지는 관계로 보류
draw_barPlot_professor_Assignment()
draw_barPlot_professor_TeamProject()
draw_barPlot_professor_Credit()
draw_barPlot_professor_Attendence()
draw_barPlot_professor_Test()
