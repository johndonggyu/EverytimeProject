# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from .models import smu_professor, lecture_evaluation, lecture_time, board, major_keyword, board_keyword, Eval, professor_keyword, colleges,majors, major_ngram_keyword, ratingProfessor, ratingMajor, major_synonym
from datetime import datetime
import urllib
from django.conf import settings

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import requests
import json

#회원가입 인증메일 보내기 새로 추가한 메소드
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.contrib import auth
#비밀번호 찾기 
from django.contrib.auth.hashers import check_password


# Create your views here.
def home(request):
	return render(request, 'login.html')

#ChartJS 사용위해 importing.
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

def main(request):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	return render(request, 'main3.html', {
		'colleges' : _colleges,
		'majors' : _majors,
		})

def sitemap(request):
	return render(request, 'sitemap.html')

def faq(request):
	return render(request, 'faq.html')

def activate(request, uid64, token):

	uid = force_text(urlsafe_base64_decode(uid64))
	try:
		user = User.objects.get(pk=uid)
	except Exception as e:
		print(e)
		return HttpResponse('비정상적인 접근입니다.[uid]')
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		#auth.login(request, user) #인증되면 바로 로그인하는 것으로부터
		#return redirect('/main') #인증되면 바로 메인페이지로 이동하는것으로부터
		return redirect('/login') #로그인 페이지로 이동하는 것으로 변경함.
	else:
		return HttpResponse('비정상적인 접근입니다.')

def fpw2(request):
    context= {}
    if request.method == "post":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect('/main')
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
    else:
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})

    return render(request, "fpw2.html",context)

class join(View):
	#userID = '';
	def get(self, request, *args, **kwargs):
		#userID = request.POST['userid']
		return render(request, 'join.html')
	def post(self, request, *args, **kwargs):
		condition = False
		response = HttpResponse("<script>alert('이미 존재하는 아이디입니다.');history.back(-1);</script>")
		createID = request.POST['userid']
		createNick = request.POST['nickname']
		createPW = request.POST['password']
		#
		try:
			User.objects.get(username=createID)
		except ObjectDoesNotExist:
			condition = True
		#
		if not condition:
			return response
		else:
			user = User.objects.create_user(createID, createNick, createPW)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			#localhost:8000
			uid = urlsafe_base64_encode(force_bytes(user.pk)).decode().encode()
			token = account_activation_token.make_token(user)
			message = render_to_string('user_activate_email.html', {
				'user':user,
				'domain':current_site.domain,
				'uid':uid,
				'token': token,
			})
			print(uid)
			print(token)
			mail_subject = "[상명타임즈] 회원가입 인증 메일입니다."
			user_email = user.username
			email = EmailMessage(mail_subject, message, to=[user_email])
			email.send()
			return HttpResponse(
			    '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
			    'justify-content: center; align-items: center;">'
			    '입력하신 이메일로 인증 링크가 전송되었습니다.'
			    '</div>'
			)
			return redirect('/main')
		return render(request, 'join.html')
			#response = HttpResponse("<script>alert('회원가입 되었습니다.');window.close();</script>")
			#return response
class fpw1(View):
	#userID = '';
	def get(self, request, *args, **kwargs):
		#userID = request.POST['userid']
		return render(request, 'fpw1.html')
	def post(self, request, *args, **kwargs):
		condition = False
		response = HttpResponse("<script>alert('ID가 틀렸습니다. 다시 입력해주세요.');history.back(-1);</script>")
		userID = request.POST['userid']

		try:
			User.objects.get(username=userID)
		except ObjectDoesNotExist:
			condition = True
		
		if not condition:
			return response
		else:
			response = HttpResponse("<script>location.href='../fpw1/'</script>")
			user.save()
			current_site = get_current_site(request)
			#localhost:8000
			message = render_to_string('activate_email.html', {
				'user':user,
				'domain':current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': account_activation_token.make_token(user),
			})
			mail_subject = "[상명타임즈] 아이디 인증 메일입니다."
			user_email = user.username
			email = EmailMessage(mail_subject, message, to=[user_email])
			email.send()
			return HttpResponse(
			    '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
			    'justify-content: center; align-items: center;">'
			    '입력하신 이메일로 인증 링크가 전송되었습니다.'
			    '</div>'
			)
			return redirect('/fpw2')
		return render(request, 'fpw1.html')


# def fpw1(request):
# 	return render(request, 'fpw1.html')

class loGin(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'login.html')
	def post(self, request, *args, **kwargs):
		response = HttpResponse("<script>alert('ID/PW가 틀렸습니다. 다시 입력해주세요.');history.back(-1);</script>")
		userID = request.POST['userid']
		userPW = request.POST['password']

		user = authenticate(request, username=userID, password=userPW)

		if user is None:
			return response
		else:
			response = HttpResponse("<script>location.href='../main/'</script>")
			login(request, user)
		return response

def logOut(request):
	logout(request)
	return HttpResponse("<script>alert('로그아웃 되었습니다.');location.href='../login/'</script>")

class prejoin(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'prejoin.html')
	def post(self, request, *args, **kwargs):
		stdno = request.POST['userid']
		password = request.POST['password']
		url='http://smsg.smuc.ac.kr:9100/haksa/loginProc.jsp?memnonob='+stdno+'&apssrowd='+password+'&loginMode=normal&PWD=&STD_NO=&KRVENC='
		html=requests.get(url)
		code=html.text
		ch=code[128]
		if ch=='>':
			return HttpResponse("<script>alert('인증되었습니다.');location.href='../join';</script>")
		else:
			return HttpResponse("<script>alert('인증실패하였습니다.');history.back(-1);</script>")

def individual(request,dept,pname):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	if(dept and pname):
		bcnt = Eval.objects.filter(comment_prof__professor__professor__major=dept,comment_prof__professor__professor__professor=pname).count()
		## kwdcnt ==> wordcloud
		kwdcnt = professor_keyword.objects.filter(major=dept,professor=pname).count()

		p = smu_professor.objects.get(professor=pname,major=dept)
		ppic = p.picture
		pinfo = p.information

		## updated ==> wordcloud
		a = professor_keyword.objects.filter(major=dept,professor=pname).order_by('-word_date').last()
		if(a):
			updated = a.word_date
		else:
			print('something went wrong')
			return render(request, 'professor_individual.html', {
				'pname1' : pname,
				'major1' : dept,
				'bcnt' : 0,
				'kwdcnt' : 0,
				'updated' : '',
				't10kwd' : 0,
				'wc_path' : '/static/img/nodata.png',
				'ppic' : ppic,
				'pinfo' : pinfo,
				'colleges' : _colleges,
				'majors' : _majors,
				})
		## t10kwd ==> wordcloud
		t10kwd = professor_keyword.objects.filter(major=dept,professor=pname).order_by('-count')[:10]
		## wc_path : wordcloud 이미지 경로
		y = str(datetime.now().year)
		#m = str(datetime.now().month - 1)
		wc_path = settings.STATIC_URL+"wc/"+ pname + "-" + dept + y + ".png"
		## month : wordcloud가 몇월달 건지. 이것도 자동으로 한달 전으로



		return render(request, 'professor_individual.html', {
			'pname1' : pname,
			'major1' : dept,
			'bcnt' : bcnt,
			'kwdcnt' : kwdcnt,
			'updated' : updated,
			't10kwd' : t10kwd,
			'ppic' : ppic,
			'pinfo' : pinfo,
			'colleges' : _colleges,
			'majors' : _majors,
			})

def us(request):
	return render(request, 'us.html')

def comment(request):
	return render(request, 'comment.html')

def userinfo(request):
	return render(request, 'userinfo.html')

def keyword(request):
	return render(request, 'keyword.html')

def bbs(request,blog_id):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	## bcode
	if(blog_id == "370450" or blog_id == 370450):
		bcode = "자유 게시판"
		bcode_file = 'jagae'
	elif(blog_id == "369474" or blog_id == 369474):
		bcode = "새내기 게시판"
		bcode_file = 'saenaegi'
	elif(blog_id == "hotarticle"):
		bcode = "핫 게시판"
		bcode_file = 'hot'
	else:
		bcode = "그냥 게시판"
	## bcnt
	bcnt = board.objects.filter(code=blog_id).count()
	if(bcnt == 0):
		return render(request, 'bbs.html', {
			'bcode':bcode,
			'bcnt':0,
			'kwdcnt':0,
			'updated':0,
			't10kwd' : 0,
			'wc_path' : '/static/img/nodata.png',
			'month' : 0,
			'colleges' : _colleges,
			'majors' : _majors,
			})
	## kwdcnt ==> wordcloud
	kwdcnt = board_keyword.objects.filter(code=blog_id).count()
	## updated ==> wordcloud
	a = board_keyword.objects.filter(code=blog_id).order_by('-word_date').last()
	updated = a.word_date
	## t10kwd ==> wordcloud
	t10kwd = board_keyword.objects.filter(code=blog_id).order_by('-count')[:10]
	## wc_path : wordcloud 이미지 경로
	if(datetime.now().month - 1 < 10):
		optstr = "-0"
	else:
		optstr = "-"
	y = str(datetime.now().year)
	m = str(datetime.now().month - 1)

	#현재 달보다 한달 전으로 자동 설정하게 하기.
	month = datetime.now().month - 1

	return render(request, 'bbs.html', {
		'bcode' : bcode,
		'bcnt' : bcnt,
		'kwdcnt' : kwdcnt,
		'updated' : updated,
		't10kwd' : t10kwd,
		'month' : month,
		'colleges' : _colleges,
		'majors' : _majors,
		})

def pf(request, pf_id):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	professor = get_list_or_404(smu_professor, major=pf_id)
	majoring = professor[0].major
	try:
		#print(professor)
		#for p in professor:
			#print(p)
		return render(request, 'professor_dept.html', {
			'professor': professor,
			'error_message': "Something went wrong",
			'majoring': majoring,
			'colleges' : _colleges,
			'majors' : _majors,
			'major' : pf_id,
			})
	except:
		print("professor view error")
	return render(request, 'professor_dept.html')

def major(request, dept):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	if(dept):
		try:
			e = major_synonym.objects.get(major=dept)
			majorList = e.synonym.split('|')
			bcnt = 0
			for majorSyn in majorList:
				bcnt += board.objects.filter(contents__contains=majorSyn).count()
		except Exception as e:
			print(e)
			pass
		## kwdcnt ==> wordcloud
		kwdcnt = major_keyword.objects.filter(major=dept).count()
		## updated ==> wordcloud
		a = major_keyword.objects.filter(major=dept).order_by('-word_date').last()
		if(a):
			updated = a.word_date
		else:
			return render(request, 'department_profiling.html', {
				'colleges' : _colleges,
				'majors' : _majors,
				'major' : dept,
				'bcnt' : 0,
				'kwdcnt' : 0,
				'updated' : 0,
				't10kwd' : 0,
				'wc_path' : '/static/img/nodata.png',
				'wc_ng3_path' : '/static/img/nodata.png',
			})
		## t10kwd ==> wordcloud
		t10kwd = major_keyword.objects.filter(major=dept).order_by('-count')[:10]
		## wc_path : wordcloud 이미지 경로
		y = str(datetime.now().year)
		#m = str(datetime.now().month - 1)
		return render(request, 'department_profiling.html', {
			'colleges' : _colleges,
			'majors' : _majors,
			'major' : dept,
			'bcnt' : bcnt,
			'kwdcnt' : kwdcnt,
			'updated' : updated,
			't10kwd' : t10kwd,
			})
	else:
		print('something went wrong')
		#return render_to_response('myView.html')
		return render(request, 'department_profiling.html')


def word_cloud(request, blog_id):
	try:
		words_json = [{'text': bkey.keyword, 'weight': bkey.count, 'link': "/"+bkey.keyword} for bkey in board_keyword.objects.filter(code=blog_id).order_by('-count')]
		# [dict, dict, dcit, ...]
		return HttpResponse(json.dumps(words_json))
	except Exception as e:
		print(e)
		return HttpResponse("[]")
def word_cloud2(request, major_id, pf_id):
	try:
		words_json = [{'text': bkey.keyword, 'weight': bkey.count, 'link': "/"+bkey.keyword} for bkey in professor_keyword.objects.filter(major=major_id,professor=pf_id).order_by('-count')]
		# [dict, dict, dcit, ...]
		return HttpResponse(json.dumps(words_json))
	except Exception as e:
		print(e)
		return HttpResponse("[]")
def word_cloud3(request, major_id):
	try:
		#print('is this working?!??!?')
		words_json = [{'text': bkey.keyword, 'weight': bkey.count, 'link': "/"+bkey.keyword} for bkey in major_keyword.objects.filter(major=major_id).order_by('-count')]
		# [dict, dict, dcit, ...]
		return HttpResponse(json.dumps(words_json))
	except Exception as e:
		print(e)
		return HttpResponse("[]")
def word_cloud4(request, major_id):
	try:
		#print('is this working?!??!?')
		words_json = [{'text': bkey.keyword, 'weight': bkey.count, 'link': "/"+bkey.keyword} for bkey in major_ngram_keyword.objects.filter(major=major_id).order_by('-count')]
		# [dict, dict, dcit, ...]
		return HttpResponse(json.dumps(words_json))
	except Exception as e:
		print(e)
		return HttpResponse("[]")
## 메인페이지 인기 키워드 10개
def topKeywords(request):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	try:
		keywords = [{'professor': bkey.keyword, 'count': bkey.count} for bkey in board_keyword.objects.all().order_by('-count')[:10]]
		return HttpResponse(keywords)
		#return render(request, 'blahblahblah.html', {
		#	'colleges' : _colleges,
		#	'majors' : _majors,
		#	'keywords' : keywords,
		#	})
	except Exception as e:
		print(e)
		return HttpResponse("[]")
## 메인페이지 인기 교수님 3명
def topProfessors(request):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	try:
		topProf = [{'professor': bkey.prof.professor, 'count': bkey.countEval + bkey.countKeyword} for bkey in ratingProfessor.objects.order_by('-countEval','-countKeyword')[:3]]
		return HttpResponse(topProf)
		#return render(request, 'blahblahblah.html', {
		#	'colleges' : _colleges,
		#	'majors' : _majors,
		#	'topProf' : topProf,
		#	})
	except Exception as e:
		print(e)
		return HttpResponse("[]")
## 인기 관련 초기화
def initTops(request):
	# 인기 교수님 & 학과 초기화
	try:
		ratingProfessor.objects.all().delete()
		ratingMajor.objects.all().delete()

		b = smu_professor.objects.all()
		for a in b:
			bcnt = Eval.objects.filter(comment_prof__professor__professor__major=a.major,comment_prof__professor__professor__professor=a.professor).count()
			kwdcnt = professor_keyword.objects.filter(major=a.major,professor=a.professor).count()
			ratingProfessor(prof=a,countEval=bcnt,countKeyword=kwdcnt).save()
		
		d = majors.objects.all()
		for c in d:
			try:
				e = major_synonym.objects.get(major=c.major)
				majorList = e.synonym.split('|')
				bcnt = 0
				for majorSyn in majorList:
					bcnt += board.objects.filter(contents__contains=majorSyn).count()
				kwdcnt = major_keyword.objects.filter(major=c.major).count()
				ratingMajor(major=c,countBoard=bcnt,countKeyword=kwdcnt).save()
			except Exception as e:
				print(e)
				pass
		return HttpResponse("초기화 완료")
	except Exception as e:
		print(e)
		return HttpResponse("초기화 에러")
## 메인페이지 인기 학과 5개
def topMajors(request):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	try:
		topMajor = [{'major': bkey.major.major, 'count': bkey.countBoard + bkey.countKeyword} for bkey in ratingMajor.objects.order_by('-countBoard','-countKeyword')[:5]]
		return HttpResponse(topMajor)
		#return render(request, 'blahblahblah.html', {
		#	'colleges' : _colleges,
		#	'majors' : _majors,
		#	'topMajor' : topMajor,
		#	})
	except Exception as e:
		print(e)
		return HttpResponse("[]")

#OK_수정
def error(request):
	return render(request, '404.html')

def fpw1(request):
	return render(request, 'fpw1.html')

def fpw2(request):
	return render(request, 'fpw2.html')

def change_pw(request):
    context= {}
    if request.method == "POST":
        current_password = request.POST.get("origin_password")
        user = request.user
        if check_password(current_password,user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)
                return redirect("./main3.html")
            else:
                context.update({'error':"새로운 비밀번호를 다시 확인해주세요."})
    else:
        context.update({'error':"현재 비밀번호가 일치하지 않습니다."})

    return render(request, "./main3.html",context)

#ChartJS Experiment
def chart(request, dept, pname):
	#교수님 평점 계산
	try:
		match_lect = lecture_time.objects.filter(professor__professor=pname,professor__major=dept)
		#교수님과 교수님 전공에 해당하는 시간표 객체에 들어있는 데이터 불러오기
		match_eval = lecture_evaluation.objects.filter(professor__professor__professor=pname)
		#교수님의 이름과 매치하는 강의 평가 데이터 가져오기
		lect = []
		for a in match_lect:
			lect.append(a.lecture)
			#lect에다가 교수님 시간표로부터 강의명만 가져오기
		c = []
		#print("---------------------")
		for item in match_eval:
			if(item.professor.lecture in lect):
				#강의평가 데이터에 있는 강의명이 시간표로부터 가져온 강의명과 일치하다면?
				c.append(item)
				#이렇게 하면 일치하고 있는 강의명을 가진 강의 평가 데이터가 c라는 튜플에 추가 될것이다
				#print(item.professor.lecture)
				#실제로 해당 강의 평가 데이터들의 강의명이 들어가있는지 한번 확인해보자.
		#print("---------------------")
		#한 교수님이 강의하는 모든강의명의 제목이 c리스트에 들어가게 된다. 
		tokens = list() #토큰을 리스트 형태로 생성
		#카운트 올릴 변수들 초기화
		nOfclasses=0
		#교수님 총점 평균 계산
		sumScore=0
		averageScore=0
		#카운트 올릴 변수들 초기화
		assignmentMany=0
		assignmentNorm=0
		assignmentNone=0
		#조모임 계산 변수
		team_projectMany=0
		team_projectNorm=0
		team_projectNone=0
		#학점 비율 계산 변수
		creditGod = 0
		creditProportion = 0
		creditTough = 0
		creditFbomb = 0
		#출결 어떤지 계산 변수
		attendanceMix=0
		attendanceDirect=0
		attendanceDesignated=0
		attendanceElectronic=0
		attendanceNone=0
		 #시험 횟수 많은지 계산 변수
		test4above=0
		test3=0
		test2=0
		test1=0
		testNone=0
		#함수 중요 변수 및 메서드
		everytime_data = c 
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
		tokens.append(test4above)
		tokens.append(test3)
		tokens.append(test2)
		tokens.append(test1)
		tokens.append(testNone)
		json_list = []
		chart_json = [{'averageScore': tokens[0], 'assignmentMany': tokens[1], 'assignmentNorm': tokens[2],'assignmentNone': tokens[3],'team_projectMany': tokens[4],'team_projectNorm': tokens[5],'team_projectNone': tokens[6],'creditGod': tokens[7],'creditProportion': tokens[8],'creditTough': tokens[9],'creditFbomb': tokens[10],'attendanceMix': tokens[11],'attendanceDirect': tokens[12],'attendanceDesignated': tokens[13],'attendanceElectronic': tokens[14],'attendanceNone': tokens[15],'test4above': tokens[16],'test3': tokens[17],'test2': tokens[18],'test1': tokens[19],'testNone': tokens[20] }]
		return HttpResponse(json.dumps(chart_json))
	except Exception as e:
		print(e)
		print('something went wrong')
		return HttpResponse("[]")