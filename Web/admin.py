## paresd_data/admin.py
from django.contrib import admin
## models에서 EverytimeDAta를 import 해준다.
from .models import board, Eval, lecture_evaluation, board_keyword, professor_keyword, major_keyword, lecture_time, smu_professor, search_major, major_synonym, colleges, majors
## 아래의 코드를 입력하면 EverytimeData를 admin 페이지에서 관리할 수 있다.
class boardAdmin(admin.ModelAdmin):
	list_display = ['code','title','contents','date']
	list_display_links = ['title']
	list_filter = ['code','date']
	search_fields = ['title','contents']
admin.site.register(board, boardAdmin)
class EvalAdmin(admin.ModelAdmin):
	model = Eval
	list_display = ['get_comment_prof']
	list_display_links = ['get_comment_prof']
	search_fields = ['get_comment_prof','comment']
	def get_comment_prof(self,obj):
		return obj.comment_prof.professor.professor.professor + "=" + obj.comment_prof.professor.lecture
admin.site.register(Eval, EvalAdmin)
class lectevalAdmin(admin.ModelAdmin):
	list_display = ['professor','score','assignment','team_project','credit','attendance','test']
	list_display_links = ['professor']
	search_fields = ['professor']
admin.site.register(lecture_evaluation, lectevalAdmin)
class smProfAdmin(admin.ModelAdmin):
	list_display = ['major','professor','information']
	list_display_links = ['major','professor']
	list_filter = ['major']
	search_fields = ['major','professor']
admin.site.register(smu_professor,smProfAdmin)
class bkAdmin(admin.ModelAdmin):
	list_display = ['code','keyword','word_date','count','pos_percent','neg_percent']
	list_display_links = ['keyword']
	list_filter = ['code','word_date']
	search_fields = ['keyword','pos_percent','neg_percent']
admin.site.register(board_keyword,bkAdmin)
class pkAdmin(admin.ModelAdmin):
	list_display = ['major','professor','keyword','word_date','count','pos_percent','neg_percent']
	list_display_links = ['major','professor','keyword']
	list_filter = ['major','word_date']
	search_fields = ['major','professor','keyword','pos_percent','neg_percent']
admin.site.register(professor_keyword,pkAdmin)
class mkAdmin(admin.ModelAdmin):
	list_display = ['major','keyword','word_date','count','pos_percent','neg_percent']
	list_display_links = ['major','keyword']
	list_filter = ['major','word_date','count']
	search_fields = ['major','keyword','pos_percent','neg_percent']
admin.site.register(major_keyword,mkAdmin)
class smAdmin(admin.ModelAdmin):
	list_display = ['major','board_number']
	list_display_links = ['major','board_number']
	list_filter = ['major']
	search_fields = ['major']
admin.site.register(search_major,smAdmin)
class lectimeAdmin(admin.ModelAdmin):
	search_fields = ['lecture']
admin.site.register(lecture_time,lectimeAdmin)
class mSynAdmin(admin.ModelAdmin):
	list_display = ['major','synonym']
	list_display_links = ['major','synonym']
	search_fields = ['major','synonym']
admin.site.register(major_synonym,mSynAdmin)
class collegesAdmin(admin.ModelAdmin):
	list_display = ['college']
	list_display_links = ['college']
	search_fields = ['college']
admin.site.register(colleges,collegesAdmin)
class majorsAdmin(admin.ModelAdmin):
	list_display = ['college','major']
	list_display_links = ['major']
	list_filter = ['college']
	search_fields = ['major']
admin.site.register(majors,majorsAdmin)