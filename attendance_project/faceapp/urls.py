from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'), 

    # admin page addition author:Amar Nagaju
    path('table/', views.amarTable, name='table'),
    path('staffList/', views.staffList, name='staffList'),
    path('staffDetail/', views.staffDetail, name='staffDetail'),
    path('holiday/', views.holiday, name='holiday'),
    path('leave/', views.leave, name='leave'),

    #user page
    path('userdash/', views.userDash, name='userdash'),

    path('login/', views.loginUser, name='login'),
    path('demo/', views.demo, name='demo'),
    # path('', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),


    path('home/', views.home, name='home'), 
    # path('', views.index, name='index'),  
    path('attendance/',views.attendanceTable,name='attendance'),
    path('register/',views.register,name='register'),
    path('addstaff/',views.addstaff,name='addnewstaff'),
    path('editTable/',views.editTable,name='editTable'),
    path('deletestaff/<int:code>/',views.deletestaff,name='deletestaff'),
    path('<int:code>/',views.editStaff,name='editStaff'),
    path('dashboard/',views.dashboardStaff,name='dashboardStaff'),

    
    path('face-application/',views.face_exe,name='face_exe'),
    path('chart/',views.chart,name='chart'),
    path(r'face-application/facecapture', views.captureface, name='capturefaces'),
    path('recognization/', views.recognization, name='recognizations'),
    path('offline/',views.offline,name='offline'),

    path('home/datesearch',views.datesearch,name='datesearch'),
    path('attendance/datesearch2',views.datesearch2,name='datesearch2'),
    path('addstaff/addstaffDB/',views.addstaffDB,name='addstaffDB'),

    path('contactList/',views.contactList,name='contactList'),
    path('sendEmail/<int:code>/',views.sendEmail,name='sendEmail'),



]