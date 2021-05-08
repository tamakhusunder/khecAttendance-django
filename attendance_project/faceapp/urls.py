from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.loginUser, name='login'),
    # path('', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),


    path('home/', views.home, name='home'), 
    # path('', views.index, name='index'),  
    path('attendance/',views.attendanceTable,name='attendance'),
    path('register/',views.register,name='register'),
    path('addstaff/',views.addstaff,name='addnewstaff'),
    path('deletestaff/<int:code>/',views.deletestaff,name='deletestaff'),
    path('<int:code>/',views.editStaff,name='editStaff'),
    path('dashboard/',views.dashboardStaff,name='dashboardStaff'),

    
    path('face-application/',views.face_exe,name='face_exe'),
    path('chart/',views.chart,name='chart'),
    path('table/',views.table,name='table'),
    path(r'face-application/facecapture', views.captureface, name='capturefaces'),
    path('recognization/', views.recognization, name='recognizations'),
    path('offline/',views.offline,name='offline'),

    path('datesearch',views.datesearch,name='datesearch'),
    path('addstaff/addstaffDB/',views.addstaffDB,name='addstaffDB'),



]