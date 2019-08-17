# -*- coding: utf-8 -*-
from django.db import models  
# Create your models here.

class colleges(models.Model):
	college = models.CharField(default='',max_length=20)
	
	class Meta:
		unique_together = (("college"),)

	def __str__(self):
		return self.college
class majors(models.Model):
	college = models.ForeignKey(colleges,null=True,on_delete=models.CASCADE)
	major = models.CharField(null=True,default='',max_length=20)
	
	class Meta:
		unique_together = (("college", "major"),)

	def __str__(self):
		return self.major
class major_keyword(models.Model):
	## primary_key를 하나 이상으로 두면 에러가 남.
	major = models.CharField(default='',max_length=20)
	keyword = models.CharField(default='',max_length=100)
	word_date = models.DateTimeField(default='')
	count = models.IntegerField(null=True)
	pos_percent = models.FloatField(null=True,default=0.00)
	neg_percent = models.FloatField(null=True,default=0.00)

	class Meta:
		unique_together = (("major", "keyword", "word_date"),)

	def __str__(self):
		return self.keyword
class major_ngram_keyword(models.Model):
	## primary_key를 하나 이상으로 두면 에러가 남.
	major = models.CharField(default='',max_length=20)
	keyword = models.CharField(default='',max_length=100)
	word_date = models.DateTimeField(default='')
	count = models.IntegerField(null=True)
	pos_percent = models.FloatField(null=True,default=0.00)
	neg_percent = models.FloatField(null=True,default=0.00)

	class Meta:
		unique_together = (("major", "keyword", "word_date"),)

	def __str__(self):
		return self.keyword

class professor_keyword(models.Model):
	## primary_key를 하나 이상으로 두면 에러가 남.
	major = models.CharField(default='',max_length=20)
	professor = models.CharField(default='',max_length=20)
	keyword = models.CharField(default='',max_length=100)
	word_date = models.DateTimeField(default='')
	count = models.IntegerField(null=True)
	pos_percent = models.FloatField(null=True,default=0.00)
	neg_percent = models.FloatField(null=True,default=0.00)

	class Meta:
		unique_together = (("major", "professor", "keyword", "word_date"),)

	def __str__(self):
		return self.keyword

class board_keyword(models.Model):
	## primary_key를 하나 이상으로 두면 에러가 남.
	#board = models.ForeignKey(board,null=True,on_delete=models.CASCADE)
	code = models.CharField(default='',max_length=20)
	keyword = models.CharField(default='',max_length=100)
	word_date = models.DateTimeField(default='')
	count = models.IntegerField(null=True)
	pos_percent = models.FloatField(null=True,default=0.00)
	neg_percent = models.FloatField(null=True,default=0.00)

	class Meta:
		unique_together = (("code", "keyword", "word_date"),)

	def __str__(self):
		return self.keyword

class board(models.Model):
	board_number = models.AutoField(primary_key=True)
	code = models.CharField(null=True,default='',max_length=20)
	title = models.CharField(null=True,default='',max_length=200)
	contents = models.CharField(null=True,default='',max_length=1000)
	date = models.DateTimeField(null=True,default='')

	class Meta:
		ordering = ['-date']
		unique_together = (("code", "title", "contents"),)

	def __str__(self):
		return self.title

class smu_professor(models.Model):
	major = models.CharField(null=True,default='',max_length=20)
	professor = models.CharField(null=True,default='',max_length=20)
	information = models.CharField(null=True,default='',max_length=100)
	picture = models.CharField(null=True,default='',max_length=100)

	class Meta:
		unique_together = (("major", "professor"),)

	def __str__(self):
		return self.professor

#class search_professor(models.Model): #게시판에서 해당 교수님 이름 검색 결과
#	board_number = models.ForeignKey(board,null=True,on_delete=models.CASCADE)
#	major = models.ForeignKey(smu_professor,null=True,on_delete=models.CASCADE)
#	#professor #major이 애초에 smu_professor의 foreignkey object라
#	def __str__(self):
#		return self.board_number

class search_major(models.Model): #게시판에서 해당 학과 이름 검색 결과
	board_number = models.ForeignKey(board,null=True,on_delete=models.CASCADE)
	major = models.CharField(null=True,default='',max_length=20)
	class Meta:
		unique_together = (("board_number", "major"),)

	def __str__(self):
		return self.board_number.title
class lecture_time(models.Model):
	lecture = models.CharField(null=True,default='',max_length=30)
	professor = models.ForeignKey(smu_professor,null=True,default='',on_delete=models.CASCADE)
	#major
	#college = models.CharField(null=True,default='',max_length=20)

	class Meta:
		unique_together = (("lecture", "professor"),)

	def __str__(self):
		return self.professor.professor + "("+self.professor.major+")" + " - " + self.lecture

class lecture_evaluation(models.Model):
	eval_number = models.AutoField(primary_key=True)
	professor = models.ForeignKey(lecture_time, on_delete=models.CASCADE, null=True)
	#lecture = models.CharField(null=True,default='',max_length=30)
	score = models.FloatField(null=True,default=0.00)
	assignment = models.CharField(null=True,default='',max_length=20)
	team_project = models.CharField(null=True,default='',max_length=20)
	credit = models.CharField(null=True,default='',max_length=20)
	attendance = models.CharField(null=True,default='',max_length=20)
	test = models.CharField(null=True,default='',max_length=20)
	def __str__(self):
		return self.professor.professor.professor + " - " + self.professor.lecture

class Eval(models.Model):
	comment_number = models.AutoField(primary_key=True)
	comment_prof = models.ForeignKey(lecture_evaluation, on_delete=models.CASCADE, null=True)
	comment = models.CharField(null=True,default='',max_length=1000)
	def __str__(self):
		return self.comment_prof.professor.professor.professor

class major_synonym(models.Model):
	major = models.CharField(primary_key=True, max_length=20)
	synonym = models.CharField(null=True,default='',max_length=20)

	def __str__(self):
		return self.major

class ratingProfessor(models.Model):
	prof = models.ForeignKey(smu_professor, on_delete=models.CASCADE, null=True)
	countEval = models.IntegerField(null=True)
	countKeyword = models.IntegerField(null=True)

	class Meta:
		ordering = ['-countEval','-countKeyword']

	def __str__(self):
		return self.prof.professor + "(" + self.prof.major + ")"

class ratingMajor(models.Model):
	major = models.ForeignKey(majors, on_delete=models.CASCADE, null=True)
	countBoard = models.IntegerField(null=True)
	countKeyword = models.IntegerField(null=True)

	class Meta:
		ordering = ['-countBoard','-countKeyword']

	def __str__(self):
		return self.major.major + "(" + self.major.college + ")"