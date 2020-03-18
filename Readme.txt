==자유/새내기/핫 게시판 완성 일지==2019-07-20
#1 (하드코딩 수정 건의)
파일:base.html
<li><a href="{% url 'major' m_id=3 %}">역사콘텐츠학과</a></li>				<li><a href="{% url 'major' m_id=4 %}">지적재산학과</a></li>
... and so on ...
이부분을 하드코딩하지말고 {% for %} 돌려서
처리할 수 없을지?
=> 그러려면, DB에 학과 데이터가 있어야함.
(대학, 학과, 전공 분류로 DB 생성하면 좋을듯)
장점:유지보수하기 좋음.


#2 (에러사항)
url경로:/pf/컴퓨터과학과
로딩이 엄청 걸렸음. (2019-07-20)
이유:학교홈페이지 점검.
교수님 이미지는 www.smu.ac.kr로부터 가져오는데
학교사이트에 접속이 안되어, 이미지를 불러오는데
엄청 오래걸렸음. css 중 첫 로딩화면 원뺑글뺑글
돌아가는거 없애던가, 문제 해결 바람.
차후문제:원본 이미지 경로 변경 등
생각난해결법:처음에 이미지를 다운 해놨다가,
로딩 실패시 다운한 이미지로 대체하기.
html 태그 속성 중 그런 옵션이 있음. 참고바람.


#3 (하드코딩 수정)
파일:views.py
함수:bbs
rendering시에 month와 wc_path 부분 변경함.
기존의 하드코딩 되어있던 것을 동적으로 처리함.
(자동으로 현재 달보다 한 달 전의 워드클라우드를
가져오도록 하였음)

{% static '{{ wc_path }}' %} 는 템플릿 태그
안에 또 태그가 들어가기 때문에 에러가 발생함.
그래서 views.py 자체에서 static 경로 가지고 옴.

최근 업데이트 날짜 updated|date="format"
포맷을 지정하여 출력하도록 하여, 영문을 없앰.
ex) 2019-07-20 11:12


#4 (코드 수정)
파일:jayu_drawc.py
함수:count_word
워드클라우드 생성 시
두글자 이상부터, 최대 50개까지 단어로 생성하도록
만듦.


#5 (예외처리)
파일:views.py
함수:bbs
해당 게시판의 글이 DB에 하나도 저장되어있지
않을 경우에 게시판 프로파일에 모두 0이나 None,
url일 경우에는 #으로 만들었음.
변경사항:
  파일:bbs.html
  만약 키워드 수가 0일 경우엔 top 10이 아예 나오
  지 않도록 변경함. {% if kwdcnt %}{%endif%}


#6 (예외처리)
파일:jayu_parser.py
함수:main
기존의 파싱된 데이터의 존재여부를 확인하는
예외처리에서 각 게시판의 코드를 검사하는 기능을
추가함.
tmp = board.objects.filter(code='게시판코드')
if(tmp and ...이전과 동일)


#7 (제약조건)
파일:models.py
클래스:board
변경사항: 제약조건
중복된 게시물 파싱을 방지하기 위해서,
unique_together("code", "title", "contents")
를 추가하였다.
또 도배글 방지를 위해서이기도 하다.
새내기게시판은 title이 없다 참고로.


#8 (파일추가)
파일:saenaegi_parser.py
파일:saenaegi_drawc.py
파일:saenaegi_drawc2.py


#9 (모듈제작)
파일:saenaegi_parser.py
파일:saenaegi_drawc.py
파일:saenaegi_drawc2.py
기존의 자유게시판 코드를 기반으로 수정함.


#10 (예외처리)
파일:jayu_drawc.py
파일:saenaegi_drawc.py
예외처리:게시판코드를 구분해서 board_keyword
테이블 초기화 시키기.
코드:del_obj.filter(code='게시판코드').delete()


#11 (리팩토링)
파일:bc.py
게시판 코드 담는 파일
사용법:import bc
bc.jagae, bc.saenaegi, bc.hot
bc.jaegaef, bc.saenaegif, bc.hotf
f는 파일이름을 나타냄.
@아직 미사용@

#12 (리팩토링)
파일:board_parser.py
게시판 통합 파서
사용법:python board_parser.py 2019-06 370450
또는 python board_parser.py 2019-06-12 369474
python board_parser.py 2019-06 hotarticle

#13 (리팩토링)
파일:board_drawc.py
게시판 통합 워드클라우드 생성
사용법:
python board_drawc.py 2019-06 370450 jagae
python board_drawc.py 2019-06 369474 saenaegi
python board_drawc.py 2019-06 hotarticle hot

#14 (리팩토링)
파일:board_drawc2.py
board_keyword 기반 워드클라우드 생성
사용법:
python board_drawc2.py 2019-06 370450 jagae
python board_drawc2.py 2019-06 369474 saenaegi
python board_drawc2.py 2019-06 hotarticle hot

#15 (리팩토링)
폴더:old_module
이전 코드 백업용 폴더임


#16 (다른 PC작업시 참고사항)
models.py 변경했기 때문에 다시
makemigrations - migrate 해주길 바람.
migrate할 때 unique 관련 에러 뜨면,
db 안의 board 테이블의 내용 다 지우고 다시 해보길 바람.

자유게시판을 테스트 해보아도 좋으나 시간이 많이 걸리기
때문에, 될 수 있으면, 새내기 게시판이나 핫게시판 테스트
해볼 것.

==이상으로 자유/새내기/핫 게시판 프로토타입 완성==
2019-07-20 오전04:57

==워드클라우드 객체화 일지==2019-07-22
#0 jQcloud 소스코드 github 사용법 참고
http://mistic100.github.io/jQCloud/

#1 (경로 추가)
파일:urls.py
path('objectification/', ...)
path('word_cloud/', ...)


#2 (함수 추가)
파일:views.py
def objectification
해당 함수는 objectification.html 로 렌더링한다.

def word_cloud
해당 함수는 board_keyword db에서 키워드, 빈도수를
불러와 json 파일로 만들어서 전달한다.


#3 (템플릿 추가)
파일:objectification.html
기존의 페이지들처럼 header footer를 적용함.
거기에 추가적으로 <div id="word_cloud"></div>를
추가한 거라고 보면됨. 해당 id이름은 다른 파일에서
참조중이니 이름 변경 시 주의바람.


#4 (static 파일들 추가)
css:jqcloud.min.css
js:jqcloud.min.js, script.js
참고사항: jquery기반으로 만들어짐.

워드클라우드 세부 설정은 script.js에서 진행됨.
shape : elliptic, rectangular 이렇게 두개 잇음.
rectangular은 개인적으로 한글로 보면 보기 안좋음.
autoResize : true 창 크기에 따라 글자 크기도 변함. 
center : 0.5 는 속해있는 태그의 중간에 위치함을 의미.
width, height 속성은 가로세로 크기를 의미. 
개발자도구 열어서 직접 확인바람. 없어서는 안됨.
fontSize: 글자 크기를 정함. 작다싶으면 소수점 늘리셈.
colors: 색깔 세부적으로 변경가능함.


#5 (파일 수정)
파일:base.html
static 파일들 <link><script> 태그로 추가함.


#6 (리팩토링) 중요!!
파일:urls.py
path('word_cloud/<str:blog_id>', ...)

파일:views.py
def word_cloud(request, blog_id):
게시판 별로 워드클라우드 출력 가능하도록 변경.
board_keyword.objects.filter(code=blog_id). ...

파일:bbs.html
워드클라우드 출력되는 부분에 <div id="word_cloud">
추가함.

그러므로 기존의 워드클라우드 하단에 클릭 가능한
워드클라우드 출력되도록 변경함.


#7 (파일 삭제 및 변경)
파일:views.py
def objectification 제거함. 리팩토링을 통해 쓸모없어짐.

파일:urls.py
path('objectification/', ...) 도 마찬가지로 제거함.

==워드클라우드 객체화 일지==2019-07-22 01:34

==교수님 프로파일링 일지==2019-07-22

#1 (DB 설계 오류 수정)
해당 테이블: Eval, lecture_evaluation
관계가 잘못되었음.
한 교수님의 lecture_evaluation이 여러 강의평(Eval)을
가질 수 있어야함.

원래:
eval (1) ---- lecture_evalution (다)
이후:
lecture_evaluation (1) ---- eval (다)

파일:models.py
수정하였음.


#2 (파일 추가)
파일:prof_individual_parser.py
smu_professor db에 들어가있는 교수님 명단에 따라서
해당 교수님 강의평가 크롤링함.

컴퓨터과학과 교수님들 강의평가 모두 크롤링 하는데
걸린 시간 약 4분.
모든 학과 교수님 강의평 크롤링하는데 걸릴시간은..흠..

문제점: 동명이인

해결방법1: 강의평가 검색어를 교수님 이름 교과명으로 변경
=> 불가능. 에브리타임에서 ex) 강상욱 정보보호 로 검색
하면 아무것도 안나옴.

해결방법2: 어쩌피 데베에는 lecture_evaluation에는
교수님이름 + 교과목명이 같이 저장되고,
eval 에서는 해당 교수님 + 교과목명의 강의평으로 이어지기
때문에 워드클라우드 생성 시에 lecture_time에 있는
교수님 명 + 교과목명을 참고해서 생성하면 된다.

교수님이름:smu_professor
교과목명:lecture_time

의문1:시간표 교과목명이 강의평가에 나오는 교과목명이랑 
다를 경우가 있을지? 있으면 귀찮아짐. 
없을거라고 생각하겠음.


#3 (파일 추가)
파일:lecture_time_parser.py
해님이가 준 코드를 토대로 lecture_time 테이블 형성

해님이가 준 코드는 중복 데이터 예외처리가 되지않아,
DB models.py에서 unique meta class로 예외처리 적용함

특이사항: 에타 시간표에는 게임학과로 검색 시 
민경하 자료구조가 존재함.
lecture_time_parser.py 에서는 smu_professor 테이블
에서 우선 해당 교수가 있는 지 확인 후에 존재하면
그제서야 lecture_time에 등록하게 된다.
이유는 ForeignKey 제약 조건 때문임.
근데 만약 이런 상황(민경하 게임학과 자료구조)에서는
게임학과에 민경하 교수님이 없어서 에러가 뜬다.
하지만 애초에 동명이인을 걸러내기 위한 테이블이므로
별 의미가 없으므로 무시해도 된다는 판단이 선다.

한번만 돌려놓으면 당분간 돌릴일 거의 없다지만,
이것도 시간 좀 걸리니 주의바람.

또 해님이가 준 코드가 2018~2019년도 1학기까지에
해당하는 시간표만 크롤링한 것이기 때문에...........
모든 데이터가 있는 것은 아님@!@!#!@#!@#!#!@!#
(이게 또 문제가 학기별로 categoryId가 다 달라서,
패턴이 있으면 좋을텐데, 못찾음. 하드코딩해야되는 문제)


#4 (동명이인 처리 의문점)
컴퓨터과학과 빼고는 다 되는데, 컴퓨터과학과만 안됨.
이유가 뭘까?

확인 해보니, lecture_time 테이블에도 컴과만 안들어옴.
그렇다면 파싱과정에서 잘못되었다는 건데,,,
역시, 컴퓨터과학과가 아니라 공학과라고 되어있었던 것이
원인이었음. => ㅇ_ㅇ


#5 (테스트)
이 순서에 따라 실행 시켜야함. foreign key 연결이 그러함.
1>python get_smu_professor.py (smu_professor DB)
교양 또는 학과별 교수님 목록 가져오기.

2>python lecture_time_parser.py (lecture_time DB)
실행해서 시간표 기반으로 획득한 동명이인 처리 테이블
db저장. 어느 학과의 어느 교수님이 어느 과목을 가르치는
지 알 수 있는 테이블임.

2>python prof_individual_parser.py 
(lecture_evaluation DB && Eval DB)
강의평가 관련 데이터 저장함.
일단 이건 임시로 컴퓨터과학과 교수님만 파싱하도록함.
너무 오래걸림.

3>python prof_individual_drawc.py 
(워드클라우드 생성)
이것도 마찬가지로 임시로 컴퓨터과학과만 해놓음.


#6 (models 변경)
기존의 lecture_evaluation 모델을 DB 설계대로 변경하였음
그래서 lecture을 지우고, professor을 lecture_time을
참조하도록 만들었음.

이후 실행 테스트 완료.


#7 (board_keyword에 삽입)
파일:prof_individual_drawc.py
교수님별 프로파일링에 쓰인 키워드들도
count_word 함수에서 board_keyword에 삽입하도록 함.
단, code를 교수명-학과로 설정함.

#8 (템플릿 적용)
파일:urls.py
path('individual/<str:dept>/<str:pname>', ...)

파일:views.py
def individual(request,dept,pname):
pname : 교수명
major : 학과명
bcnt : 강의평 개수
kwdcnt : 키워드 개수(board_keyword)
updated : 워드클라우드 업데이트 날짜
t10kwd : top 10 keyword
wc_path : 교수별 워드클라우드 경로

ppic : 교수님 사진
pinfo : 교수님 설명

/individual/컴퓨터과학과/한종대

#9 (models.py 재설계)
기존의 DB설계에 따라, professor_keyword테이블 생성
후 이전 0722_2_Websaver 코드에서는 board_keyword
로 교수님 관련 데이터를 집어넣었던 것을 제대로된 위치인
professor_keyword 테이블에 넣게 만들었다.


#10 (models.py 추가)
class search_professor
class search_major
DB설계에 따라 추가하였음.

search_professor은 게시글 내에서 교수님 이름에 대해
검색하면 나온 게시글의 키워드를 추출

search_major은 게시글 내에서 학과 이름/유사이름에 대해
검색하면 나온 게시글의 키워드를 추출


====교수님 프로파일링 완성==== 2019-07-22 18:17
====교수님 프로파일링 완성==== 2019-07-22 18:53


==학과 프로파일링 일지==
#1 (의견)
학과 프로파일링할 때 컴퓨터과학과라면,
컴과|컴퓨터과학 등의 유의어들도 검색해야하는데,
학과별 유의어에 대한 데이터베이스도 있으면 어떨까?

major(PK)
synonym


#2 (파일추가)
파일:get_majors
하드코딩으로 학과명과 학과명과 유사한 단어를
regex형태로 구별해서 저장함.
DB:keyword_synonym


#3 (파일추가)
파일:major_drawc.py
학과별 프로파일링 워드클라우드 생성기
동시에 count_word 함수에서
major_keyword 테이블에도 50개까지 키워드를 넣는다.

일단은 ngram3으로 하지 않고, 일반 워드클라우드로 함.


#4 (템플릿 작업)
파일:views.py
def major(request, dept)
major
bcnt
kwdcnt
updated
t10kwd
wc_path
파일:department_profiling.html


#5 (에러 페이지, 404.html 건의)
사용자가 파라미터를 잘못입력했을 경우 에러페이지로
이동할 수 있도록, 에러페이지좀 만들어주세욤.


#6 (테스트)
/major/음악학부
(다른 학과는 게시판 크롤링을 안해서, 안나옴.)
(운좋게 음악학부가 걸림)
(어떻게 걸렸는지는 major_drawc.py 실행하면 알 수 있음)


#7 (models.py 수정)
search_major 모델 추가 및 적용


#8 (교수 프로파일링 의문)
DB:search_professor
search_professor은 게시판에서 해당 교수님을 검색해서
데이터를 긁어오는건데, 게시물에 있어서 동명이인은 어떻게
처리할 것인지? => 안하는 걸로.


==2019-07-25==
#1 (리팩토링)
파일 이름 일관성 있게 변경함.
의미 중심으로 변경함.


#2 (파일 추가)
파일:delete_all.py
모든 db를 초기화 시키는 모듈


#3 (파일 추가)
파일:make_all.py
모든 db에 값을 넣는 모듈

(DB: keyword_synonym 쓰기)
python save_major_synonym.py

(DB: board 쓰기)
python parser_board.py 2019-06 370450
python parser_board.py 2019-06 369474
python parser_board.py 2019-06 hotarticle

(DB: board 읽기, board_keyword 쓰기)
python drawc_board.py 2019-06 370450 jagae
python drawc_board.py 2019-06 369474 saenaegi
python drawc_board.py 2019-06 hotarticle hot

(DB: board_keyword 읽기)
python drawc2_board.py 2019-06 370450 jagae
python drawc2_board.py 2019-06 369474 saenaegi
python drawc2_board.py 2019-06 hotarticle hot

(DB: smu_professor 쓰기)
python save_smu_professor.py

(DB: lecture_time 쓰기)
python parser_lecture_time.py

(DB: lecture_evaluation 쓰기, Eval 쓰기)
python parser_prof_individual.py

(DB: Eval 읽기, professor_keyword 쓰기)
python drawc_prof_individual.py

(DB: board 읽기, major_keyword 쓰기, search_major 쓰기)
python drawc_major.py

사용법: python make_all.py
위 명령이 모두 순차적으로 실행이 되도록하는 모듈임.
그리고 모두 얼마의 시간이 걸렸는지도 체크할 수 있음.


#4 (수정)
대메뉴 동적으로 출력할 수 있도록, models.py에
colleges, majors 추가하였고, views.py에도 메뉴
정상적으로 보일 수 있도록, 적용하였음.


#5 (TIL-Today I Learned)
WordCloud(
	font_path = fontpath,
	stopwords = stopwords_kr,
	background_color = backcolor,
	width = 800, height = 600,
	...
)
stopwords 속성을 사용해서 워드클라우드에 표시되지않을
단어들의 리스트를 정할 수 있음.
MyList(l) - MyList(l2) 할 필요가 없어짐.
width와 height를 정하면 어떤변화가 있는지 테스트해보기.


#6 parser_board.py 오기 수정
board(title=t, contents=c, date=datetime.now(), code=o).save() 로 되어있던걸 date=d로 변경함.
board_keyword로 오인함.


#7 워드클라우드 수정
여백 완전 없애고 화질 개선.
정사각형으로 변환.


#8 교수/학과 프로파일링 객체화 완성
관련 파일:urls.py, script.js, views.py


#8 대메뉴 중 계당교양교육원 클릭 에러
클릭안되는 문제 해결.


#9 교양학과 교수님만 워드클라우드 만들어지지 않는 현상 해결
parser_prof_individual.py 에서 교수님별 강의평가를 크롤링
하는데, 이 때 동명이인 체크를 위해서, lecture_time
테이블에 들어가있는 교수님인지 확인하는데, parser_lecture
_time.py 에서는 교양교수님을 파싱하지 않기에 생긴문제였다.
또 각 학과 뿐만 아니라, 교양에서도 동명이인이 있을 수 있지
않은가!

해결법:parser_lecture_time.py 파일에서 college 리스트에
계당교양교육원 교수님 교과목도 파싱하게 만들기.

방법1: 학과로 구분짓지 말고, 전공/영역을 [전체]로 해서
시간표 검색해서 파싱하기.
방법1문제점: 어떤 교수님이 어떤 학과인지 모름. 알려면, 
수업 코드 (ex: LR10011)대로 어떤 학과인지 알아야하는데,
이에 대한 데이터 부재. 사실 학사정보시스템이나 수강정보시스
템으로부터 가져올 수는 있으나, 확인한 바로는 교과목명을
코드만으로 구분하기가 어려웠음. 서로 다른 학과인데, 같은
코드를 발견함. 예) 사범대학, 일반선택 교양과목, TT~

방법2: college리스트에 계당교양교육원으로 교양과목도 넣기.
교필, 교선, 교직, 일선을 해당과목으로 넣었음.

방법2 채택!!
일단, 기존의 느린 selenium방식을 XML파싱으로 변경함.
속도 1000배 향상함.

parser_lecture_time.py 전반적으로 모두 변경함.


#10 번외
형태소분석기에는 사전기반, 통계기반, 인공지능 기반이 있다.
우리가 사용하는 konlpy(Hannanum, Kkma, Okt)는 사전기반임.
통계기반의 형태소 분석기로는 Soynlp, 인고지능으로는 
카카오에서 만든 Khaiii가 있다(Windows에서 동작안함).
사전기반으로는 한계가 명확하기 때문에, 다른 방법으로 시도할
필요가 있어보인다.


#11 ngram
ngram을 만들기 위해서는 해당 학과이름이 들어간 게시물을
찾아서, 그 게시물의 단어들을 하나의 리스트로 만들고,
모든 게시물들의 ngram리스트를 nltk.ngram 함수에 넣어서
돌린 결과물을 가지고서 워드클라우드로 만들어야한다.

현재로서는 search_major 테이블에서 해당 게시물이 해당
학과이름이 나옴을 알 수 있다. 그러면 해당 게시물에
가서 해당 게시물의 명사들을 하나의 리스트로 만들고,
다음 게시물을 또다시 하나의 리스트로 만들어,
그 모든 리스트들을 하나의 리스트로 묶으면 된다.

또다른 방법으로는 기존의 board_keyword테이블에
board 테이블의 foreignkey를 추가해서, 해당 키워드가
어떤 게시물에서 왔는지 볼 수 있도록 만들어서, 손쉽게
참조가 가능하도록 할 수 있다. 하지만 이 방법의 문제점은
문맥의 흐름이 뒤죽박죽일 수밖에 없다는 것이다. 
board_keyword에 나오는 키워드들이 모두 문장의 흐름에
따라 순서를 정하여 저장된 것이 아니기 때문이다.
이 작업을 강제한다고 가정했을 때는 기존의 코드를 많이
바꾸어야 한다. 불가능한 방법은 아니다.

하지만 현재로서 최선의 방법으로는 search_major에서 
검색된 게시물의 제목+내용을 다시 토큰화 하여, 순서대로
리스트로 저장하여 ngram 함수로 돌리는 방법이다.

drawc_ngram_major.py 로 만들었다.

참고!
ngram은 그럼 컴과, 컴퓨터과학 이런 유의어는 어떻게
처리하였는가? 애초에 search_major자체에서 major_synonym
테이블을 참조해서 게시물을 탐색하였기 때문에, 문제없음.


#12 학과 유의어 관련
만약 현재 사전 기반 형태소 분석기를 사용하고 있다면,
학과 유의어도 사전에 포함시켜야 한다.
관련파일: kkma-2.0 >> noun.dic
그래서 관련 유의어 모두 추가함.
그제서야 인식됨.
문장 : "역콘과는 제법이다"
기존의 결과 :['역','콘','과','는','제법','이','다']
변경후 :['역콘과','는','제법','이','다']


#13 major_synonym (이전 keyword_synoynm)
이름 변경


#14 admin 커스터마이징
admin 창 검색기능, 필터기능, 등 다양한 기능 추가중
가독성 증가.

특히!
ngram3 했을 때 결과가 '문 정 역콘' 나오면 이게 왜 이렇게 나왔는지
확인할 길이 everytime에서 직접 검색밖에 없었는데, 이제는
직접 board 테이블에다가 그대로 문 정 역콘 이라고 치면, 관련 데이터가
검색되도록 하였다. => 이로써 직접 단어 추가 또는 유의어 찾기가 가능해짐.
"문 정 역콘"에서 "문 정"의 의미는 문헌정보과였음.


#15 kkma-2.0 폴더 자동으로 압축하고 덮어쓰기하도록 만드는
bat파일 만듦.
파일명: makejarByKDG.bat (kkma폴더에 있음)
noun.dic 수정하고 그냥 저 파일 실행하면 됨.

추가로! 어쩌피 한글자 단어는 워드클라우드에 출력되지 않도록
했기 때문에, 정확성을 위해서 한글자 단어 모두 사전에서 제외함.

추가로!
그래도 왠지모르게 한글자 단어가 출몰!
한글자 나오면 워드클라우드에서 제외시키겠음.
코드: CODE-A0001
코드는 파일에서 검색으로 찾아보기바람.


#16 지적재산권학과 오타
majors테이블에는 지적재산학과라고 오기 되어있음.


#17 계당교양교육원도 학과 프로파일링 메뉴에 속해있음
major_synonym에 교양도 포함시켜야 겠음.


==학과 ngram3 완성== 2019-07-29 오전 9:05
교양이 제일 많이 나옴... 이유? 교양도 유의어 반영함.
기존의 워드클라우드는 최신화 안함.

참고! ngram3은 100개까지 출력하도록 함.
이유: 교양이랑 컴과는 상관없는데, 다른 과는 너무 안나옴.

==2019-07-31==
#1 리팩토링
프로젝트명 websaver => EverytimeProject
어플리케이션명 각 blog, parsed_data로 나뉘어있던걸 => Web으로 통합
현재 쓰이지 않는 모듈은 old_modules 폴더에, 쓰이는 모듈은 modules폴더에
있음.
폰트나, 마스크, 예외처리 파일들은 raw_data 폴더에 있음.
settings.py 는 home에 있음.
데이터베이스 테이블 이름들도 모두 Web_땡땡으로 시작됨.

프론트엔드 관련된 파일들은 Web의 static, templates, urls, views 쪽 참고.
백엔드는 modules폴더, DB관련 파일인 Web폴더 안의 models.py 파일,
url경로마다의 기능은 views.py파일 참고.


#2 major_ngram_keyword 모델 생성함 
- 객체화를 위해 저장이 필요함.
그래서 drawc_ngram_major.py 에 db에 넣는거 적용시킴.


#3 사용법 다시 공지
모듈 실행법: 무조건 modules폴더 안에 들어가서 python 모듈이름.py 실행할것
(안그러면 오류날 거임)
서버 실행법: EverytimeProject 폴더(manage.py 파일 있는 곳)에서
runserver 또는 makemigrations, migrate 할 것.


#4 save_smu_professor.py 수정
기존의 인터넷 창이 뜨던 걸, headless로 변경함으로써, 창이 안뜨도록 만듦.
이렇게 바꾼 이유: 우분투에서도 동작하게 하기 위함.


#5 github 버전만 해당
draw_wordcloud함수 다 제거함.
이미지파일로 워드클라우드 생성 안함.
keyword테이블에 넣기만하고,
객체화로 바로 출력하게함.

===2019-08-05===

#1 이메일 인증 관련
이메일 인증용 계정(gmail)
아이디: 해옥성 지메일
비밀번호: 비밀번호
settings.py 참고

이메일 인증 구현함.
관련파일들: 
views.py(activate, join), tokens.py, templates\user_activate_email.html
추가로 변경한 사항: base.html 에서 로그인 했을 때 로그인한 계정의 이메일이 보이도록
함. 

===이후에는 github commit 참고바람===
==작성종료==
