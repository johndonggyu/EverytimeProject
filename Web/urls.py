# -*- coding: utf-8 -*-
"""EverytimeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('blog/<str:blog_id>', views.bbs, name='bbs'),
    path('pf/<str:pf_id>', views.pf, name='pf'),
    path('major/<str:dept>', views.major, name='major'),
    path('main/', views.main, name='main'),
    path('login/', views.loGin.as_view(), name='login'),
    path('logout/', views.logOut, name='logout'),
    path('join/', views.join.as_view(), name='join'),
    path('activate/<str:uid64>/<str:token>', views.activate, name='activate'),
    path('prejoin/', views.prejoin.as_view(), name='prejoin'),
    path('faq/', views.faq, name='faq'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('us/', views.us, name='us'),
    path('individual/<str:dept>/<str:pname>/', views.individual, name='individual'),
    path('comment/', views.comment, name='comment'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('keyword/', views.keyword, name='keyword'),
    path('word_cloud/mn/<str:major_id>', views.word_cloud4, name='word_cloud4'),
    path('word_cloud/m/<str:major_id>', views.word_cloud3, name='word_cloud3'),
    path('word_cloud/<str:blog_id>', views.word_cloud, name='word_cloud'),
    path('word_cloud/<str:major_id>/<str:pf_id>', views.word_cloud2, name='word_cloud2'),
    path('error/', views.error, name='error'),
    path('fpw1/', views.fpw1, name='fpw1'),
    path('fpw2/', views.fpw2, name='fpw2'),
    path('chart1/<str:dept>/<str:pname>', views.chart1, name='chart1'),
    path('chart2/<str:dept>/<str:pname>', views.chart2, name='chart2'),
    path('chart3/<str:dept>/<str:pname>', views.chart3, name='chart3'),
    path('chart4/<str:dept>/<str:pname>', views.chart4, name='chart4'),
    path('chart5/<str:dept>/<str:pname>', views.chart5, name='chart5'),
    path('chart6/<str:dept>/<str:pname>', views.chart6, name='chart6'),

]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('blog/', RedirectView.as_view(url='#', permanent=True)),
    path('pf/', RedirectView.as_view(url='#', permanent=True)),
    path('major/', RedirectView.as_view(url='#', permanent=True)),
    path('individual/', RedirectView.as_view(url='#', permanent=True)),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
#from . import settings

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
