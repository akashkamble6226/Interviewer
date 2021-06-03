
from os import name
from django.conf.urls import url
from . import views

urlpatterns=[
    
    url(r'^$',views.login,name='login'),
    url('login',views.login,name='login',),
    url('mainpage',views.mainpage,name='mainpage',),
    url('register',views.register,name='register'),
    url('logout',views.logout,name='logout'),
    url('adminPanel',views.adminPanel,name='adminPanel'),
    url('addQuestion',views.addQuestion,name='addQuestion'),
    url('showQuestions',views.showQuestions,name='showQuestions'),
    url('edit_question/(?P<id>[0-9]+)',views.edit_question,name='edit_question'),
    url('update_question/(?P<id>[0-9]+)',views.update_question,name='update_question'),
    url('delete_question/(?P<id>[0-9]+)',views.delete_question,name='delete_question'),
    url('isAnsGiven/(?P<id>[0-9]+)',views.isAnsGiven,name='isAnsGiven'),
    url('askQuestion/(?P<id>[0-9]+)',views.askQuestion,name='askQuestion'),
    url('giveAnswer/(?P<id>[0-9]+)',views.giveAnswer,name='giveAnswer'),
    url('showReport',views.showReport,name='showReport'),
    url('showAnaysis',views.showAnaysis,name='showAnaysis'),
    
   
    



    


   
    

]

