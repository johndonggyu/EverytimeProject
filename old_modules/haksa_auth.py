import requests
import urllib
#import getpass

#print('Input ID')
#stdno=input()
#print('Input Password')
#pw=getpass.getpass()
#password=urllib.parse.quote(pw)
def auth_haksa(stdno, password):
    url='http://smsg.smuc.ac.kr:9100/haksa/loginProc.jsp?memnonob='+stdno+'&apssrowd='+password+'&loginMode=normal&PWD=&STD_NO=&KRVENC='
    html=requests.get(url)
    code=html.text
    ch=code[128]
    if ch=='>':
        return True
     #print('success')
    else:
        return False
     #print('fails')
