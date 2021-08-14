from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'), 

    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

# <<<<<<<<<<<<<----admin url--->>>>>>>>>>>>
    # admin page addition author:Amar Nagaju
    path('table/', views.amarTable, name='table'),
    path('timeSetting/', views.timeSetting, name='timeSetting'),
    path('holiday/', views.holiday, name='holiday'),
    path('leave/', views.leave, name='leave'),

    #view staffinActiveList
    path('inActiveList/', views.inActiveList, name='inActiveList'),
    path('activeList/', views.activeList, name='activeList'),
    path('staffList/', views.staffList, name='staffList'),
    path('staffDetail/<int:userID>', views.staffDetail, name='staffDetail'),
   

    #register staff
    path('addStaffNew/', views.addStaffNew, name='addStaffNew'),
    path('addStaffNewDetail/<int:userID>', views.addStaffNewDetail, name='addStaffNewDetail'),

    #edit staff
    path('editStaff/<int:userID>/',views.editStaff,name='editStaff'),
    path('deletestaff/<int:userID>',views.deletestaff,name='deletestaff'),
    path('editTable/',views.editTable,name='editTable'),

    #xhtml2pdf --print pdf
    path('attendancePdf/',views.attendancePdf,name='attendancePdf'),
    # pie-chart
    path('pie-chart/', views.pie_chart, name='pie-chart'),


    path('home/', views.home, name='home'), 
    path('attendance/',views.attendanceTable,name='attendance'),
    path('dashboard/',views.dashboardStaff,name='dashboardStaff'),


    # path('home/datesearch',views.datesearch,name='datesearch'),
    # path('attendance/datesearch2',views.datesearch2,name='datesearch2'),
    # path('addstaff/addstaffDB/',views.addstaffDB,name='addstaffDB'),

    path('contactList/',views.contactList,name='contactList'),
    path('sendEmail/<int:code>/',views.sendEmail,name='sendEmail'),
    path('contactUs/',views.contactUs,name='contactUs'),

# <<<<<<<<<<<<<----customer url--->>>>>>>>>>>>
    #user page addition author:Amar Nagaju
    path('userDash/', views.userDash, name='userDash'),
    path('userProfile/', views.userProfile, name='userProfile'),
    path('user_setting/', views.user_setting, name='user_setting'),

    

# <<<<<<<<<<<<<----application--->>>>>>>>>>>>
    path('face-application/',views.face_exe,name='face_exe'),
    path('chart/',views.chart,name='chart'),
    path(r'face-application/facecapture', views.captureface, name='capturefaces'),
    path('recognization/', views.recognization, name='recognizations'),

]
