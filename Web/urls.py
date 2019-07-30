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
    #path('blog/<int:blog_id>', views.bbs, name='bbs'),
    path('blog/<str:blog_id>', views.bbs, name='bbs'),
    #path('pf/<int:pf_id>', frontexnd.blog.views.pf, name='pf'),
    path('pf/<str:pf_id>', views.pf, name='pf'),
    path('major/<str:dept>', views.major, name='major'),
    #path('major/<int:m_id>', views.major, name='major'),
    path('main/', views.main, name='main'),
    path('login/', views.loGin.as_view(), name='login'),
    path('logout/', views.logOut, name='logout'),
    path('join/', views.join.as_view(), name='join'),
    path('prejoin/', views.prejoin.as_view(), name='prejoin'),
    path('faq/', views.faq, name='faq'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('us/', views.us, name='us'),
    path('individual/<str:dept>/<str:pname>/', views.individual, name='individual'),
    #path('individual/', views.individual, name='individual'),
    path('comment/', views.comment, name='comment'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('keyword/', views.keyword, name='keyword'),
    path('word_cloud/mn/<str:major_id>', views.word_cloud4, name='word_cloud4'),
    path('word_cloud/m/<str:major_id>', views.word_cloud3, name='word_cloud3'),
    path('word_cloud/<str:blog_id>', views.word_cloud, name='word_cloud'),
    path('word_cloud/<str:major_id>/<str:pf_id>', views.word_cloud2, name='word_cloud2'),
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
