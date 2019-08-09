#장고 사용위해 import한 부분
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
import time
from operator import eq
import django
django.setup()
from backend.parsed_data.models import board
from datetime import datetime
import sys

#감성분석 사용위해 import한 부분
from konlpy.tag import Okt
import json
from pprint import pprint
import nltk
import numpy as np


#데이터베이스 연결위해 import한 부분
import sqlite3
con = sqlite3.connect("db.sqlite3")
#이유는 모르겠으나 db.sqlite3.sqlite3는 안되고, db.sqlite3는 인식을 넘나 잘한다 어쩌면 그냥 파일이름이 db이고 파일형식이 sqlite3였을지도 모른다... 내가 멍청했던건가보다.


# 파일 로드를 위한 함수
def read_data(filename):
    with open(filename, 'r', encoding='UTF8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        # txt 파일의 헤더(id document label)는 제외하기
        data = data[1:]
    return data

train_data = read_data('ratings_train.txt') #데이터불러오기
test_data = read_data('ratings_test.txt') #데이터불러오기
# 1) morphs : 형태소 추출
# 2) pos : 품사 부착(Part-of-speech tagging)
# 3) nouns : 명사 추출
okt = Okt()
# 테스트
print(okt.pos(u'이 밤 그날의 반딧불을 당신의 창 가까이 보낼게요'))

def tokenize(doc):
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

if os.path.isfile('train_docs.json'): #파일이존재하면
    with open('train_docs.json', encoding='UTF8') as f:
        train_docs = json.load(f)
    with open('test_docs.json', encoding='UTF8') as f:
        test_docs = json.load(f)
else:
    train_docs = [(tokenize(row[1]), row[2]) for row in train_data]
    test_docs = [(tokenize(row[1]), row[2]) for row in test_data]
    # JSON 파일로 저장
    with open('train_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
    with open('test_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(test_docs, make_file, ensure_ascii=False, indent="\t")

pprint(train_docs[0]) #tokenize된 학습데이터 첫번째 테스트출력

tokens = [t for d in train_docs for t in d[0]]
print(len(tokens)) #학습데이터의 총 토큰개수
print(type(tokens)) #tokens의 타입은 list. 토큰들이 들어가있다.

text = nltk.Text(tokens, name='NMSC')

# 전체 토큰의 개수
print(len(text.tokens))

# 중복을 제외한 토큰의 개수
print(len(set(text.tokens)))

# 출현 빈도가 높은 상위 토큰 10개
pprint(text.vocab().most_common(10))

# 출현빈도가 높은 상위 토큰을 몇개 가져올건지 정하여 정확도높이기
# 시간이 꽤 걸립니다! 시간을 절약하고 싶으면 most_common의 매개변수를 줄여보세요.
# most_common(100) 의 수를 높일 수록 정확도가 올라갑니다.
selected_words = [f[0] for f in text.vocab().most_common(1000)]

selected_words
def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

train_x = [term_frequency(d) for d, _ in train_docs]
test_x = [term_frequency(d) for d, _ in test_docs]
train_y = [c for _, c in train_docs]
test_y = [c for _, c in test_docs]

x_train = np.asarray(train_x).astype('float32')
x_test = np.asarray(test_x).astype('float32')
y_train = np.asarray(train_y).astype('float32')
y_test = np.asarray(test_y).astype('float32')

from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
from keras import losses
from keras import metrics

model = Sequential()
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss=losses.binary_crossentropy, metrics=[metrics.binary_accuracy])

model.fit(x_train, y_train, epochs=10, batch_size=512)
results = model.evaluate(x_test, y_test)

def predict_pos_neg(review):
    token = tokenize(review)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if(score > 0.5):
        print("[{}]는 {:.2f}% 긍정\n".format(review, score * 100))
    else:
        print("[{}]는 {:.2f}% 부정\n".format(review, (1 - score) * 100))


# 테스트
predict_pos_neg("할줄아는거 없고 해낼 자신도 없는데 한심하고 착잡하다")
predict_pos_neg("슬픈 영화 보고 그냥 펑펑 울고 싶은데 추천 좀 해주세요")
predict_pos_neg("겨드랑이에서 삼겹살 냄새 나는듯")
predict_pos_neg("진짜 너무 심심한데 놀아줄사람")
predict_pos_neg("튜터링 돈 언제 주냐 ㅋㅋㅋㅋㅋ")
predict_pos_neg("노트북 브랜드 추천점")
predict_pos_neg("문제다 문제 우리나라 정치나 학교 총학이나 나 자신이나 전부 문제야....")

# [할줄아는거 없고 해낼 자신도 없는데 한심하고 착잡하다]는 95.76% 부정
# [슬픈 영화 보고 그냥 펑펑 울고 싶은데 추천 좀 해주세요]는 97.36% 긍정
# [겨드랑이에서 삼겹살 냄새 나는듯]는 56.33% 긍정
# [진짜 너무 심심한데 놀아줄사람]는 78.00% 부정
# [튜터링 돈 언제 주냐 ㅋㅋㅋㅋㅋ]는 89.45% 부정
# [노트북 브랜드 추천점]는 59.35% 긍정
# [문제다 문제 우리나라 정치나 학교 총학이나 나 자신이나 전부 문제야....]는 88.27% 부정

#########################################################################################
#                                           #
#  아래 소스코드부터는 에브리타임 자유게시판 게시물 하드코딩 데이터를 가지고     #
#  하나하나 일일이 하드코딩하여 분석한 결과입니다. DB에서 분석할 데이터를 가져와서    #
#  반복문을 돌려 실행해주세요!!!                            #
#                                           #
#  분석한 결과를 DB에 넣을 때에는 ...................................................   #
# 게시판 프로파일링일 경우                             #
# word table에 분석데이터 입력후  board_keyword table에도 데이터를 입력합니다.      #
# ex) ====word table=======             =======board_keyword=========           #
#      keyword : '싸이'           code : '370450'                 #
#      word_date : '2019-05'        keyword : '싸이'              #
#      count: 12            word_date : '2019-05'               #
#      pos_percent: 40.0                                #
#      neg_percent: 60.0                                #
#                                           #
# 교수별 프로파일링일 경우                             #
# word table에 분석데이터 입력 후 professor_keyword table에도 데이터를 입력합니다.  #
#ex) =====word table========          ========professor_keyword=========        #
#     keyword : '핀토스'       major : '컴퓨터과학과'                #
#     word_date : '2019-05'     professor : '손성훈'               #
#     count : 25            keyword : '핀토스'             #
#     pos_percent : 21.9        word_date : '2019-05'               #
#     neg_percent : 78.1                                #
#                                           #
# 학과별 프로파일링일 경우                             #
# word table에 분석데이터 입력 후 major_keyword table에도 데이터를 입력합니다.      #
# ex) =====word table========   ========major_keyword========               #
#     keyword : '학생회'       major : '경영학과'              #
#     word_date : '2019-05'     keyword : '학생회'             #
#     count : 53            word_date: '2019-05'                #
#     pos_percent : 77.2                                #
#     neg_percent: 22.8                                 #
#                                           #
#########################################################################################
#자동화 시도 시작 새내기 게시판자료를 먼저 시도해본다.

def get_tokens1_369474_data() : #everytime 새내기 게시판으로 부터 객체들 불러오기.
  tokens1 = list() #토큰을 리스트 형태로 생성
  everytime_data = board.objects.all() #새내기 게시판에 들어와있는 컨텐츠들들 객체화 시킴
  if len(everytime_data) <= 0:
        print('db가 비었습니다 : from get_tokens1_369474_data()')
        return 0
  for datum in everytime_data : #객체화시킨데이터들을한줄씩불러읽음
    Contents = datum.contents
    tokens1.append(Contents) #게시판 본문을 토큰에 다 추가시키겠다.
    print("토큰에 다음데이터가 추가되었습니다 : %s" %(Contents))
    print('\n')
  return tokens1

def EmotionAnalysis_newbieBoard() :
  alist = get_tokens1_369474_data() #alist는 게시판의 본문들로 이뤄진 리스트 입니다.
  tokens = list() #tokens has the minimal words having the smallest meaning
  count = 0
  print(len(alist))
  percent_list1 = list()
  pos_percent = 0
  neg_percent = 0
  if type(alist) == type(int):
    if alist <= 0:
        print('토큰이 전달되지 않았습니다. from get_tokens1_369474_data')
        return 0
  for contents in alist : #analyzing the smallest meaning
    length = len(tokenize(contents))
    while(count < length):
        tmp = tokenize(contents)[count]
        tokens.append(tmp)
        count+=1
    #사실상 실제로 분석하는 부분
  for contents in alist : #alist안에 있는 contents 분석하기
    token = tokenize(contents)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if(score > 0.5):
        print("[{}]는 {:.2f}% 긍정\n".format(contents, score * 100))
        pos_percent+=1
        percent_list1.append(score)
    else:
        print("[{}]는 {:.2f}% 부정\n".format(contents, (1 - score) * 100))
        neg_percent+=1
        percent_list1.append(score)
  print(len(percent_list1))
  pos_percent = pos_percent / len(percent_list1) * 100.0
  neg_percent = neg_percent / len(percent_list1) * 100.0
  print('새내기 게시판의 전체 긍정 퍼센트')
  print( "%.2f%%" %(pos_percent))
  print('새내기 게시판의 전체 부정 퍼센트')
  print( "%.2f%%" %(neg_percent))
  tokens2 = tuple(tokens)
  text = nltk.Text(tokens2, name='NMSC')
  print('\n')
  #문자열분석 작은 단위(토큰) 개수
  #중복을 제외한 토큰의 개수
  print('현재 가져온 데이터의 전체 게시글에 사용된 중복을 제외한 전체 단어의 개수 = '+str(len(set(text.tokens))))
  #출현 빈도가 높은 상위 토큰 20개
  print('출현 빈도가 높은 상위 토큰 20개와 그 개수')
  pprint(text.vocab().most_common(20))

########################################################################################################
#sql 연동시켜서 감성분석 시키는 코드 짜기
#일단 table안에 데이터가 불러와져있다고 가정을 하고
#SQL문이 성공했다고 생각을 하자.
def get_tokens2_newBeeBoard_Keyword() : #everytime 교수님 강의평으로 부터 특정 키워드를 포함한 객체들 불러오기.
    SQLScript = "SELECT * FROM parsed_data_board WHERE code = 369474 AND contents LIKE '%수업%';"
    tokens3 = list()
    nOfdata = 0
    cur = con.cursor()
    cur.execute(SQLScript)
    for row in cur:
        print(row)
        tmp=row[2]
        tokens3.append(tmp) #이렇게 하면 리스트에 '수업'이라는 단어가 포함된 comment 열 내용들이 리스트에 추가가되겠지
        nOfdata+=1
    print(nOfdata)
    #여기까지 리스트에 sql구문으로 필요데이터를 추가해봤음
    #그러면 이제 아까처럼 반복!
    return tokens3

def EmotionAnalysis_professor_keyword() :
  blist = get_tokens2_newBeeBoard_Keyword() #blist has only data of comments
  tokens = list() #tokens has the minimal words having the smallest meaning
  count = 0
  print(len(blist))
  percent_list1 = list()
  pos_percent = 0
  neg_percent = 0
  if type(blist) == type(int):
    if blist <= 0:
        print('토큰이 전달되지 않았습니다. get_tokens2_professor_evaldata_keyword()')
        return 0
  for contents in blist : #analyzing the smallest meaning
    length = len(tokenize(contents))
    while(count < length):
        tmp = tokenize(contents)[count]
        tokens.append(tmp)
        count+=1
    #사실상 실제로 분석하는 부분
  for contents in blist : #blist 있는 contents 분석하기
    token = tokenize(contents)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if(score > 0.5):
        print("[{}]는 {:.2f}% 긍정\n".format(contents, score * 100))
        pos_percent+=1
        percent_list1.append(score)
    else:
        print("[{}]는 {:.2f}% 부정\n".format(contents, (1 - score) * 100))
        neg_percent+=1
        percent_list1.append(score)
  print(len(percent_list1))
  pos_percent = pos_percent / len(percent_list1) * 100.0
  neg_percent = neg_percent / len(percent_list1) * 100.0
  print('새내기 게시판 게시글 중 키워드: 수업 포함한 게시글들의 전체 긍정 퍼센트')
  print( "%.2f%%" %(pos_percent))
  print('새내기 게시판 게시글 중 키워드: 수업 포함한 게시글들의 전체 부정 퍼센트')
  print( "%.2f%%" %(neg_percent))
  tokens2 = tuple(tokens)
  text = nltk.Text(tokens2, name='NMSC')
  print('\n')
  #문자열분석 작은 단위(토큰) 개수
  #중복을 제외한 토큰의 개수
  print('현재 가져온 데이터의 전체 게시글에 사용된 중복을 제외한 전체 단어의 개수 = '+str(len(set(text.tokens))))
  #출현 빈도가 높은 상위 토큰 20개
  print('출현 빈도가 높은 상위 토큰 20개와 그 개수')
  pprint(text.vocab().most_common(20))

########################################################################

print('데이터 분석중 ...')
print('\n')

EmotionAnalysis_newbieBoard()
EmotionAnalysis_professor_keyword()
