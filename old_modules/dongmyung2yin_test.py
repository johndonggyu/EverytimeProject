import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
import django
django.setup()
from backend.parsed_data.models import lecture_evaluation, Eval, smu_professor, lecture_time

match_='강상욱'
match2_='화학에너지공학과'

match_lect = lecture_time.objects.filter(professor__professor=match_,professor__major=match2_)
match_eval = lecture_evaluation.objects.filter(professor__professor__professor=match_)

lect = []
for a in match_lect:
    lect.append(a.lecture)

c = []
for item in match_eval:
    if(item.professor.lecture in lect):
        d = {}
        #print(item.professor,item.lecture)
        d[item.professor.professor.professor] = item.professor.lecture
        c.append(d)

#print(c)
#print(len(c))
print(c[0][match_])

f = []

for i in range(0, len(c)):
    e = Eval.objects.filter(comment_prof__professor__professor__professor=match_,comment_prof__professor__lecture=c[i][match_])
    #print(len(e))
    if(len(e) == 0):
        continue
    if(len(e) > 1):
        for it in e:
            f.append(it.comment)
        else:
            f.append(e[0].comment)
#print(f)

