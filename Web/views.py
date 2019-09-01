# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from .models import smu_professor, board, major_keyword, board_keyword, Eval, professor_keyword, colleges,majors, major_ngram_keyword
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

def main(request):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	return render(request, 'main3.html', {
		'colleges' : _colleges,
		'majors' : _majors,
		})

def sitemap(request):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	return render(request, 'sitemap.html', {
		'colleges' : _colleges,
		'majors' : _majors,
		})


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
			uid = urlsafe_base64_encode(force_bytes(user.pk))
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
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
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
				'wc_path' : 0,
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
			'wc_path' : wc_path,
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
			'wc_path' : '#',
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

	wc_path = settings.STATIC_URL+"wc/"+ bcode_file + y + optstr + m + ".png"
	## month : wordcloud가 몇월달 건지. 이것도 자동으로 한달 전으로

	#현재 달보다 한달 전으로 자동 설정하게 하기.
	#month = 6
	month = datetime.now().month - 1

	return render(request, 'bbs.html', {
		'bcode' : bcode,
		'bcnt' : bcnt,
		'kwdcnt' : kwdcnt,
		'updated' : updated,
		't10kwd' : t10kwd,
		'wc_path' : wc_path,
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
		bcnt = board.objects.count()
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
				'wc_path' : 0,
				'wc_ng3_path' : 0,
			})
		## t10kwd ==> wordcloud
		t10kwd = major_keyword.objects.filter(major=dept).order_by('-count')[:10]
		## wc_path : wordcloud 이미지 경로
		y = str(datetime.now().year)
		#m = str(datetime.now().month - 1)
		wc_path = settings.STATIC_URL+"wc/"+ dept + y + ".png"
		wc_ng3_path = settings.STATIC_URL+"wc/"+ dept + "Ng3_" + y + ".png"
		## month : wordcloud가 몇월달 건지. 이것도 자동으로 한달 전으로

		return render(request, 'department_profiling.html', {
			'colleges' : _colleges,
			'majors' : _majors,
			'major' : dept,
			'bcnt' : bcnt,
			'kwdcnt' : kwdcnt,
			'updated' : updated,
			't10kwd' : t10kwd,
			'wc_path' : wc_path,
			'wc_ng3_path' : wc_ng3_path,
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
<<<<<<< HEAD
=======
## 메인페이지 인기 키워드 10개
def topKeywords(request):
	_colleges = colleges.objects.all()
	_majors = majors.objects.all()
	try:
		a = board_keyword.objects.filter(code='370450',word_date__year='2019',word_date__month=datetime.now().month-1).order_by('-count').values_list('keyword',flat=True)[:5]
		b = board_keyword.objects.filter(code='370450',word_date__year='2019',word_date__month=datetime.now().month-1).order_by('-count').values_list('count',flat=True)[:5]
		c = board_keyword.objects.filter(code='370450',word_date__year='2019',word_date__month=datetime.now().month-1).order_by('-count').values_list('pos_percent',flat=True)[:5]
		d = board_keyword.objects.filter(code='370450',word_date__year='2019',word_date__month=datetime.now().month-1).order_by('-count').values_list('neg_percent',flat=True)[:5]

		e = [{'keyword': keyword } for keyword in a]
		f = [{'count': count } for count in b]
		g = [{'pos_percent': p } for p in c]
		h = [{'neg_percent': n } for n in d]

		e[0]['count'] = f[0]['count']
		e[1]['count'] = f[1]['count']
		e[2]['count'] = f[2]['count']
		e[3]['count'] = f[3]['count']
		e[4]['count'] = f[4]['count']
		e[0]['pos_percent'] = g[0]['pos_percent']
		e[1]['pos_percent'] = g[1]['pos_percent']
		e[2]['pos_percent'] = g[2]['pos_percent']
		e[3]['pos_percent'] = g[3]['pos_percent']
		e[4]['pos_percent'] = g[4]['pos_percent']
		e[0]['neg_percent'] = h[0]['neg_percent']
		e[1]['neg_percent'] = h[1]['neg_percent']
		e[2]['neg_percent'] = h[2]['neg_percent']
		e[3]['neg_percent'] = h[3]['neg_percent']
		e[4]['neg_percent'] = h[4]['neg_percent']
		keywords = e#[{'keyword': bkey.keyword, 'count': bkey.count, 'pos':bkey.pos_percent, 'neg':bkey.neg_percent} for bkey in board_keyword.objects.filter(code='370450',word_date__year='2019',word_date__month=datetime.now().month).order_by('-count')[:10]]
		return HttpResponse(json.dumps(keywords))
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
		topProf = [{'professor': bkey.prof.professor, 'count': bkey.countEval + bkey.countKeyword, 'major': bkey.prof.major, 'picture': bkey.prof.picture} for bkey in ratingProfessor.objects.order_by('-countEval','-countKeyword')[:3]]
		return HttpResponse(json.dumps(topProf))
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
		topMajor = [{'major': bkey.major.major, 'count': bkey.countBoard + bkey.countKeyword, 'pos_percent':bkey.pos_percent, 'neg_percent':bkey.neg_percent} for bkey in ratingMajor.objects.order_by('-countBoard','-countKeyword')[:5]]
		return HttpResponse(json.dumps(topMajor))
		#return render(request, 'blahblahblah.html', {
		#	'colleges' : _colleges,
		#	'majors' : _majors,
		#	'topMajor' : topMajor,
		#	})
	except Exception as e:
		print(e)
		return HttpResponse("[]")
>>>>>>> eb365d2bb781370da842943e1260e8a62fa9274d

#OK_수정
def error(request):
	return render(request, '404.html')

