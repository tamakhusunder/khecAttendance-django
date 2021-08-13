from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm

from django.template.loader import get_template
from xhtml2pdf import pisa


from django.db import connection
from datetime import date,datetime

from .forms import *
from .models import * 	#to save form data in dataset
from django.views.decorators.csrf import csrf_protect

import json
from django.core.mail import send_mail as sm

import numpy as np
# Create your views here.
# def index(request):
#     return HttpResponse('Hello world 2')


#####################################################################
#common function with argument to enter sql
def database_collection(dateArg):
	dateIntable = dateArg
	activeTotal = User.objects.filter(is_staff=True, is_superuser=False).all().count()
	#filter date
	# if request.method=="POST":
	# 	dateIntable=(request.POST["attendanceDate"])
	# 	if len(dateIntable)==0:			#check empty date
	# 		dateIntable=str(date.today())
	#attedance list
	attendSql = AttendanceTb.objects.filter(date=dateIntable).all()
	presentNum = AttendanceTb.objects.filter(date=dateIntable).all().count()
	absentNum = activeTotal-presentNum
	print(attendSql,">>>>",presentNum)
	print("==================")
	#id collection
	presentIdList = []
	# if attendSql.exists():
	for i in attendSql:
		presentIdList.append(i.user_id)
	presentSql = User.objects.filter(is_staff=True, is_superuser=False, id__in = presentIdList)
	absentSql = User.objects.filter(is_staff=True, is_superuser=False).exclude(id__in=presentIdList)
	#present list in given date
	# for p in presentSql:
	# 	for at in attendSql:
	# 		if p.id == at.user_id:
	# 			print(p.profile.name,"-->",p.username,"->",p.profile.desgination,"->Present","->",at.time)
	# for a in absentSql:
	# 	print(a.profile.name,"-->",a.username,"->",a.profile.desgination,"->Absent","->","--")

	return activeTotal, attendSql, presentSql, presentNum, absentSql,absentNum, dateIntable
	

#convert to pdf
def attendancePdf(request):
	#filter date
	dateArg=str(date.today())
	if request.method=="POST":
		if 'printPage' in request.POST:
			dateArg=(request.POST["attendanceDate"])
			dateArg=str(dateArg)
			if len(dateArg)==0:			#check empty date
				dateArg=str(date.today())
	activeTotal,attendSql,presentSql,presentNum,absentSql,absentNum,dateIntable=database_collection(dateArg)
	
	# pdf function
	template_path = 'pdf/attendancePdf.html'
	context = {'activeTotal' : activeTotal,
				'attendSql' : attendSql,
				'presentSql' : presentSql,
				'presentNum' : presentNum,
				'absentSql' : absentSql,
				'absentNum' : absentNum,
				'presentSql' : presentSql,
				'dateIntable' : dateIntable
				}
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="Attendance_sheet.pdf"'
	template = get_template(template_path)
	html = template.render(context)
	pisa_status = pisa.CreatePDF(html, dest=response)
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response


def pie_chart(request):
    mon_label = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
    a = [1,2,3,4,5,0,2,4,3,4]
    # queryset=User.objects.filter(is_superuser=False)[:5]
    print("hukaa")
    # queryset = City.objects.order_by('-population')[:5]
    # for data in queryset:
        # labels .append(data.username)


    context={
    			'a':a,
    			'mon_label':mon_label
    		}

    return render(request, 'piechart/pie_chart.html', context)



########################################################	
# first startup page function
def index(request):
	return render(request,'faceapp/index.html')

#addition in admin page author:Amar Nagaju
def amarTable(request):
	form = YearForm()
	if request.method == 'POST':
		form = YearForm(request.POST)
		if form.is_valid():
			birth_date = form.cleaned_data['birth_date']
			print(birth_date,">>>")
	context = {
				'form' : form
			}
	return render(request,'faceapp/attendance_month.html',context)

# admin dashboard
@login_required(login_url='/login/')
def home(request):
	userAdmin = User.objects.get(pk=request.user.id)
	sqlUser = User.objects.filter(is_superuser=False).all()
	sqlTotalNum = User.objects.filter(is_superuser=False).all().count()
	sqlInactiveNum = User.objects.filter(is_staff=False,is_superuser=False).all().count()
	print(sqlTotalNum)
	todayDate=str(date.today())
	activeTotal,attendSql,presentSql,presentNum,absentSql,absentNum,dateIntable=database_collection(todayDate)
	# sqlActiveNum= sqlTotal-sqlInactiveNum
	context = {
				'userAdmin' : userAdmin,
				'sqlTotalNum' : sqlTotalNum,
				'sqlUser' : sqlUser,
				'sqlInactiveNum' : sqlInactiveNum,
				'sqlActiveNum' : sqlTotalNum-sqlInactiveNum,
				'presentNum' : presentNum,
				'absentNum' : absentNum
				}
	return render(request,'faceapp/home.html',context)
	# if request.user.is_authenticated:
	# 	if request.user.is_superuser:
	# 		##Profiles,sql_totstaff,sql_present,sql_absent,presentDetail,absentDetail,dateintable=database_collection()
	# # return render(request,'faceapp/home.html',{'Profiles':Profiles,'sql_totstaff':sql_totstaff,'sql_present':sql_present,'sql_absent':sql_absent})
	# 		##return render(request,'faceapp/home.html',{'Profiles':Profiles,'sql_totstaff':sql_totstaff,'sql_present':sql_present,'sql_absent':sql_absent,'presentDetail':presentDetail,'absentDetail':absentDetail,'dateintable':dateintable})
	# 		return render(request,'faceapp/home.html')
	# 	else:
	# 		return render(request,'faceapp/pages-401.html',{})
	# else:
	# 	return HttpResponseRedirect('/login/')


def attendanceTable(request):
	#filter date
	dateArg=str(date.today())
	if request.method=="POST":
		if 'searchDate' in request.POST:
			print('searchDate')
			dateArg=(request.POST["attendanceDate"])
			if len(dateArg)==0:			#check empty date
				dateArg=str(date.today())
		# if 'printPage' in request.POST:
		# 	dateArg=(request.POST["attendanceDate"])
		# 	dateArg=str(dateArg)
		# 	if len(dateArg)==0:			#check empty date
		# 		dateArg=str(date.today())
	activeTotal,attendSql,presentSql,presentNum,absentSql,absentNum,dateIntable=database_collection(dateArg)
	context = {
				'activeTotal' : activeTotal,
				'attendSql' : attendSql,
				'presentSql' : presentSql,
				'presentNum' : presentNum,
				'absentSql' : absentSql,
				'absentNum' : absentNum,
				'presentSql' : presentSql,
				'dateIntable' : dateIntable
			}
	print(context)
	return render(request,'faceapp/attendance_table.html',context)

# view list of staff in grid format
#inactive portion little wrong
@login_required(login_url='/login/')
def inActiveList(request):
	sqlInactive=User.objects.filter(is_staff=False,is_superuser=False).all()
	print(sqlInactive)
	context ={
				'sqlInactive':sqlInactive,
				'status': 'inactive'
			}
	return render(request,'faceapp/inActiveList.html',context)

@login_required(login_url='/login/')
def activeList(request):
	sqlActive=User.objects.filter(is_staff=True,is_superuser=False).all()
	print(sqlActive)
	context ={
				'sqlInactive':sqlActive,
				'status': 'active'
			}
	return render(request,'faceapp/inActiveList.html',context)

@login_required(login_url='/login/')
def staffList(request):
	userSql=User.objects.filter(is_superuser=False).all()
	context ={
				'userSql':userSql
			}
	return render(request,'faceapp/staffList.html',context)

# view staff detail in indiviual page
#change password also attached in this function
@login_required(login_url='/login/')
def staffDetail(request,userID):
	userSql = User.objects.get(pk=userID)
	#change password form
	form = SetPasswordForm(user=userSql)
	if request.method == 'POST':
		form = SetPasswordForm(user=userSql, data=request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)  # Important!
			messages.success(request, 'Password was successfully changed!')
		else:
			messages.error(request, 'Please correct the error below.')
	context ={
				'userSql':userSql,
				'form': form
			}
	return render(request,'faceapp/staffDetail.html',context)



@login_required(login_url='/login/')
def timeSetting(request):	
	form = TimeSettingForm()
	if request.method == 'POST':
		form = TimeSettingForm(request.POST)
		if form.is_valid():
			entryTime = form.cleaned_data['entryTime']
			exitTime = form.cleaned_data['exitTime']
			tolerance = form.cleaned_data['tolerance']
			print(type(exitTime))
			print(tolerance)
			print(TimeSetting.objects.all().count(),"....")
			if TimeSetting.objects.all().count() == 0:
				print("doesnot")
				add=TimeSetting(
					entryTime=entryTime,
					exitTime=exitTime,
					tolerance=tolerance
					)
				print(add)
				add.save()
				messages.success(request,'Time has been set')
			else:
				TimeSetting.objects.filter(id=1).update(id=1,entryTime=entryTime,exitTime=exitTime,tolerance=tolerance)
				print("exists")
				# timeSql.entryTime=entryTime
				# timeSql.exitTime=exitTime
				# timeSql.tolerance=tolerance
				# timeSql.save()
				messages.success(request,'Time has been updated')
		form=TimeSettingForm()
	context = {
				"form": form,
			}	
	return render(request,'faceapp/timeSetting.html', context)


@login_required(login_url='/login/')
def holiday(request):
	print("sunder")
	form = HolidayForm()
	if request.method == 'POST':
		print("2222")
		form = HolidayForm(request.POST,request.FILES)
		if form.is_valid():
			image=form.cleaned_data['image']
			active=form.cleaned_data['active']
			weekend = form.cleaned_data['weekend']
			date = form.cleaned_data['date']
			print(weekend,date,"----->",image,active)
			register = Holiday(image=image,active=active,weekend=weekend,date=date)
			register.save()
			print("dinnnner")
	return render(request,'faceapp/holiday.html', {'form':form})

@login_required(login_url='/login/')
def leave(request):
	form=LeaveForm()
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			leaveType = form.cleaned_data['leaveType']
			startDate = form.cleaned_data['startDate']
			endDate = form.cleaned_data['endDate']
			reason = form.cleaned_data['reason']
			halfday = form.cleaned_data['halfday']
			add=Leave(
				name = name,
				image = image,
				code = code,
				desgination = desgination,
				department = department,
				specialization = specialization,
				email = email,
				contact = contact,
				address = address
				)
			print(add)
			add.save()
			messages.success(request,'Leave message created.')
			# return HttpResponseRedirect(reverse(''))
	context = {
				"form": form,
			}				
	return render(request,'faceapp/leave.html',context)

#<<<<<<<----------------- Start Employee --------------->>>>>>>> 
# Add user in user model
@login_required(login_url='/login/')
def addStaffNew(request):
	user_form = UserForm()
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		if user_form.is_valid():
			print(user_form.cleaned_data['username'])
			print(user_form.cleaned_data['password1'])
			user_form.save()
			userSQL = User.objects.latest('id')
			userId = userSQL.id
			print('useer id-->',userId)
			url = '/addStaffNewDetail/'+str(userId)
			print(url)
			return redirect(url)
	return render(request,'faceapp/addStaffNew.html', {'form':user_form})

# add extra detail in profile model with onetoone relation to user model
# @transaction.atomic
@login_required(login_url='/login/')
def addStaffNewDetail(request,userID):
	user = User.objects.get(pk=userID)
	code = user.username
	profile_form = ProfileForm()
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST,request.FILES)
		if profile_form.is_valid():
			name = profile_form.cleaned_data['name']
			image = profile_form.cleaned_data['image']
			desgination = profile_form.cleaned_data['desgination']
			department = profile_form.cleaned_data['department']
			specialization = profile_form.cleaned_data['specialization']
			email = profile_form.cleaned_data['email']
			contact = profile_form.cleaned_data['contact']
			address = profile_form.cleaned_data['address']
			active = profile_form.cleaned_data['active']
			dob = profile_form.cleaned_data['dob']
			gender = profile_form.cleaned_data['gender']
			dateOfJoin = profile_form.cleaned_data['dateOfJoin']
			city = profile_form.cleaned_data['city']
			state = profile_form.cleaned_data['state']
			startYear = profile_form.cleaned_data['startYear']
			endYear = profile_form.cleaned_data['endYear']
			university = profile_form.cleaned_data['university']
			college = profile_form.cleaned_data['college']
			user = User.objects.get(pk=userID)
			user.profile.name=name
			user.profile.image=image
			user.profile.desgination=desgination
			user.profile.department=department
			user.profile.specialization=specialization
			user.profile.email=email
			user.profile.contact=contact
			user.profile.address=address
			user.profile.active=active
			user.is_staff=active    #to change is_Staff in user model
			user.profile.dob=dob
			user.profile.gender=gender
			user.profile.dateOfJoin=dateOfJoin
			user.profile.city=city
			user.profile.state=state
			user.profile.startYear=startYear
			user.profile.endYear=endYear
			user.profile.university=university
			user.profile.college=college
			user.save()
			# profileSql = Profile.objects.get(user_id=userID)
			# profileSql.name=name
			# profileSql.image=image
			# profileSql.desgination=desgination
			# profileSql.department=department
			# profileSql.specialization=specialization
			# profileSql.email=email
			# profileSql.contact=contact
			# profileSql.address=address
			# profileSql.active=active
			# profileSql.dob=dob
			# profileSql.gender=gender
			# profileSql.dateOfJoin=dateOfJoin
			# profileSql.city=city
			# profileSql.state=state
			# profileSql.startYear=startYear
			# profileSql.endYear=endYear
			# profileSql.university=university
			# profileSql.college=college
			# profileSql.save()
			# print(profileSql)
			messages.success(request,'New Staff added.')
			return redirect('/editTable/')
		else:
			messages.error(request, 'Please correct the error below.')
	context = {
				"form": profile_form,
				"codeNum": code
			}				
	return render(request,'faceapp/addStaffNewDetail.html', context)

#function to edit Profile
@login_required(login_url='/login/')
def editStaff(request,userID):
	user = User.objects.get(pk=userID)
	code = user.username
	if request.method=='POST':
		st_id=Profile.objects.get(user_id=userID)
		form=ProfileForm(request.POST,request.FILES,instance=st_id)
		if form.is_valid():
			active = form.cleaned_data['active']    #to change in is_staff in usermodel
			user.is_staff = active
			form.save()
			user.save()
			messages.success(request,'Data Updated!!!')
	else:
		st_id=Profile.objects.get(user_id=userID)
		form=ProfileForm(instance=st_id)
	context = {
				"form": form,
				"codeNum": code
			}	
	return render(request,'faceapp/editStaff.html', context)


# function to delete staff
@login_required(login_url='/login/')
def deletestaff(request,userID):
	if request.method=='POST':
		st_id=User.objects.get(pk=userID)
		st_id.delete()
		return redirect('/editTable/')

# function for table edit
@login_required(login_url='/login/')
def editTable(request):
	userSql=User.objects.filter(is_superuser=False).all()
	print(userSql)
	for u in userSql:
		print("---------------")
		print(u.username)
		print(u.profile.name)
	return render(request, 'faceapp/editTables.html', {'userSql':userSql})


def contactUs(request):
	return render(request, 'contact/contactUs.html')
#<<<<<<<----------------- End Employee --------------->>>>>>>> 


###############   --login-- logout---dashboard######

# login for both admin and user
def loginUser(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			form=LoginForm(request=request,data=request.POST)
			if form.is_valid():
				uname=form.cleaned_data['username']
				upassword=form.cleaned_data['password']
				user = authenticate(username=uname,password=upassword)
				if user is not None:
					login(request,user)
					# messages.success(request,'Welcome admin !!')
					return HttpResponseRedirect('/dashboard/')
		else:
			form=LoginForm()
		return render(request,'faceapp/login.html',{'form':form})
	else:
		return HttpResponseRedirect('/dashboard/')

def logoutUser(request):
	logout(request)
	return HttpResponseRedirect('/login/')

#data is transfer from login -> to check admin or user to pass respective pages
def dashboardStaff(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			# return render(request,'faceapp/home.html')
			return HttpResponseRedirect('/home/')
		else:
			return redirect('/userDash/')
	else:
		return HttpResponseRedirect('/login/')



###############  end of --login-- logout---dashboard######


#<<<<<<----------User/Customer site----->>>>>>>>

#addition in user page author:Amar Nagaju
@login_required(login_url='/login/')
def userDash(request):
	currentUser = request.user.id
	userSql = User.objects.get(pk=currentUser)
	context = {
				'userSql':userSql
			}
	return render(request,'user/user_dashboard.html', context )

@login_required(login_url='/login/')
def userProfile(request):
	currentUser = request.user.id
	userSql = User.objects.get(pk=currentUser)
	context = {
				'userSql':userSql
			}
	return render(request,'user/user_profile.html', context)



#End of addition by amar

############# old code ###############################

# def datesearch(request):
# 	Profiles=Profile.objects.all()
# 	sql_totstaff = Profile.objects.all().count()
# 	dateintable=str(date.today())
# 	if request.method=="POST":
# 		dateintable=str(request.POST["attendanceDate"])
# 		print(dateintable,'<<<<<<<<-----------')

# 	sql_present = AttendanceTb.objects.filter(status='p',date=dateintable).count()
# 	sql_absent=sql_totstaff-sql_present

# 	cursor=connection.cursor()
# 	sql_presentDetail='''SELECT faceapp_Profile.image,faceapp_Profile.name,faceapp_Profile.code,faceapp_Profile.desgination,faceapp_AttendanceTb.status,faceapp_AttendanceTb.time FROM faceapp_Profile,faceapp_AttendanceTb WHERE faceapp_Profile.code=faceapp_AttendanceTb.t_id AND faceapp_AttendanceTb.date="{}"'''.format(dateintable)
# 	cursor.execute(sql_presentDetail)
# 	presentDetail=cursor.fetchall()
# 	sql_absentdetail='''SELECT * FROM faceapp_Profile WHERE NOT EXISTS(SELECT * FROM faceapp_AttendanceTb WHERE faceapp_Profile.code=faceapp_AttendanceTb.t_id AND faceapp_AttendanceTb.date="{}")'''.format(dateintable)
# 	cursor.execute(sql_absentdetail)
# 	absentDetail=cursor.fetchall()
			
# 	return render(request,'faceapp/home.html',{'Profiles':Profiles,'sql_totstaff':sql_totstaff,'sql_present':sql_present,'sql_absent':sql_absent,'presentDetail':presentDetail,'absentDetail':absentDetail,'dateintable':dateintable})

# def datesearch2(request):
# 	Profiles=Profile.objects.all()
# 	sql_totstaff = Profile.objects.all().count()
# 	dateintable=str(date.today())
# 	if request.method=="POST":
# 		dateintable=str(request.POST["attendanceDate"])
# 		print(dateintable,'<<<<<<<<-----------')

# 	sql_present = AttendanceTb.objects.filter(status='p',date=dateintable).count()
# 	sql_absent=sql_totstaff-sql_present

# 	cursor=connection.cursor()
# 	sql_presentDetail='''SELECT faceapp_Profile.image,faceapp_Profile.name,faceapp_Profile.code,faceapp_Profile.desgination,faceapp_AttendanceTb.status,faceapp_AttendanceTb.time FROM faceapp_Profile,faceapp_AttendanceTb WHERE faceapp_Profile.code=faceapp_AttendanceTb.t_id AND faceapp_AttendanceTb.date="{}"'''.format(dateintable)
# 	cursor.execute(sql_presentDetail)
# 	presentDetail=cursor.fetchall()
# 	sql_absentdetail='''SELECT * FROM faceapp_Profile WHERE NOT EXISTS(SELECT * FROM faceapp_AttendanceTb WHERE faceapp_Profile.code=faceapp_AttendanceTb.t_id AND faceapp_AttendanceTb.date="{}")'''.format(dateintable)
# 	cursor.execute(sql_absentdetail)
# 	absentDetail=cursor.fetchall()
			
# 	return render(request,'faceapp/attendance_table.html',{'Profiles':Profiles,'sql_totstaff':sql_totstaff,'sql_present':sql_present,'sql_absent':sql_absent,'presentDetail':presentDetail,'absentDetail':absentDetail,'dateintable':dateintable})



# #form to save in database of newstaff
# def addstaffDB(request):
# 	if request.method=='POST':
# 		if request.POST['inputFirstName'] and request.POST['inputLastName'] and request.POST['inputCodeNo'] and request.POST['inputDesignation'] and request.POST['inputDepartment'] and request.POST['inputSpecialization'] and request.POST['inputEmailAddress'] and request.POST['inputContactNo'] and request.POST['inputAddress']:
# 			print('----------------->saved')
# 			# saverecord=Profile()
# 			f_name=request.POST.get('inputFirstName')
# 			l_name=request.POST['inputLastName']
# 			name=f_name+' '+l_name
# 			image='faceapp/images/staffs/'+request.POST['inputImg']
# 			code=request.POST['inputCodeNo']
# 			designation=request.POST['inputDesignation']
# 			department=request.POST['inputDepartment']
# 			specialization=request.POST['inputSpecialization']
# 			email=request.POST['inputEmailAddress']
# 			contact=request.POST['inputContactNo']
# 			address=request.POST['inputAddress']
# 			ins_record=Profile(name=name,image=image,code=code,department=department,desgination=designation,specialization=specialization,email=email,contact=contact,address=address)
# 			ins_record.save()
# 			print(name,image,code,designation,department,specialization,email,contact,address,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
# 			print("++++++++++++++++++record set in database")
# 			# messages.success(request,'Record Saved Successfully...')
# 			# return render(request,'faceapp/home.html')
# 		return redirect('/addstaff/')
# 		# return render(request,'faceapp/add_new_staff.html',{})
# 	else:
# 		print('------------>not saved')
# 		# return redirect('/')
# 		return render(request,'faceapp/add_new_staff.html',{})

################## end of old code


def face_exe(request):
	return render(request,'faceapp/face_exe.html',{})

def chart(request):
	return render(request,'faceapp/charts.html',{})



def contactList(request):
	userList=User.objects.filter(is_staff=True, is_superuser=False).all()
	print(userList)
	return render(request,'faceapp/contactList.html',{'userList':userList})

def sendEmail(request,code):
	user = User.objects.get(pk=code)
	useremail=user.profile.email
	emailList=[]
	emailList.append(useremail)
	form = SendEmail()
	if request.method == 'POST':
		print("sunder")
		form = SendEmail(request.POST)
		if form.is_valid():
			print("ttt")
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			print(subject,message)
			res = sm(
				subject = subject,
				message = message,
				from_email = 'comp2073@gmail.com',
				recipient_list = emailList,
				fail_silently=False,
				)  
			messages.success(request, 'Message is send Successfully')
	return render(request,'faceapp/sendEmail.html',{'user':user,'form':form})


'''####trying form--->model form
from .forms import ProfileForm
def addstaffDB(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        return redirect('/addstaff/')

    else:
        print("error")

    return render(request,'faceapp/add_new_staff.html',{})'''



# <<<<<<<<<----application code--->>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<< 1.Capture the face>>>>>>>>>>>>>>>>
def captureface(request):
	from os import listdir
	from os.path import isfile, join
	import os
	import cv2
	import dlib
	import numpy as np

	from attendancesite.settings import BASE_DIR
	
	# POST input_name of user input collected
	val_name=str(request.POST["ipname"])
	print(val_name)
	# path for making folder for input name
	path_name=BASE_DIR+r'\\media\\faceapp\\images\\capture\\'+val_name
	
	if not os.path.exists(path_name):
		print(path_name)
		print('<<<<<<<<<<<<<<<<<sunder>>>>>>>>>>>>>>>>>>>>>>>>>>')
		os.makedirs(path_name)
	
		# <<<<<<<<<<<<< code of capturing picture>>>>>>>>>>
		detector = dlib.get_frontal_face_detector()

		# Initialize Webcam
		cap = cv2.VideoCapture(0)
		# img_size = 64
		margin = 0.2
		frame_count = 0

		while True:
		    ret, frame = cap.read()
		    frame_count += 1
		    print(frame_count)   
		    input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		    img_h, img_w, _ = np.shape(input_img)
		    detected = detector(frame, 1)
		    faces = []
		    
		    if len(detected) > 0:
		        for i, d in enumerate(detected):
		            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
		            xw1 = max(int(x1 - margin * w), 0)
		            yw1 = max(int(y1 - margin * h), 0)
		            xw2 = min(int(x2 + margin * w), img_w - 1)
		            yw2 = min(int(y2 + margin * h), img_h - 1)
		            face =  frame[yw1:yw2 + 1, xw1:xw2 + 1, :]
		            file_path = path_name
		            file_name = file_path+r"\\"+val_name+str(frame_count)+"_"+str(i)+".jpg"
		            print(file_name)
		            dim = (224,224)
		            face = cv2.resize(face,dim)
		            cv2.imwrite(file_name, face)
		            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
		    cv2.imshow("Face Capturing..", frame)
		    if cv2.waitKey(1) == 13 or frame_count == 5 : #13 is the Enter Key and plz put value of frame_count as per photo to be clicked
		        break

		cap.release()
		cv2.destroyAllWindows()      

	return redirect('face_exe')


# <<<<<<<<<<<<<<3.Recognize the face>>>>>>>>>>>>>>>>>
def recognization(request):
	# Load our model
	from tensorflow.keras.models import load_model
	from datetime import datetime

	from os import listdir
	from os.path import isfile, join
	import os
	import cv2
	import numpy as np
	from tensorflow.keras.preprocessing.image import ImageDataGenerator
	from tensorflow.keras.preprocessing.image import img_to_array
	import dlib


	from attendancesite.settings import BASE_DIR

	# file_name = os.path.dirname(__file__) +'\\datasets\\test_catvnoncat.h5'
	# test_dataset = h5py.File(file_name, "r")

	model_path=BASE_DIR+r'\\static\\faceapp\\train_model\\face_new_model3.h5'
	Project7Sem = load_model(model_path)

	face_classes = {0: 'Amar Naga', 1: 'Anirudh Basukala', 2: 'Manish Kharbuja', 3: 'Manish Nhuchhe', 4: 'SKSir',5: 'Sunder'}


	def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
	               font_scale=0.8, thickness=1):
	    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
	    x, y = point
	    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
	    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness, lineType=cv2.LINE_AA)
	    
	margin = 0.2
	t= 1
	# load model and weights
	img_rows, img_cols = 100, 100

	detector = dlib.get_frontal_face_detector()

	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1000)
	temp= []
	temp_face=[]
	while True:
	    ret, frame = cap.read()
	    frame = cv2.resize(frame, None, fx=0.8, fy=0.8, interpolation = cv2.INTER_LINEAR)
	    preprocessed_faces = []           
	 
	    input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	  
	    #cv2.imshow('Test image',input_img )

	    img_h, img_w, _ = np.shape(input_img)
	    detected = detector(frame, 1)
	    faces = np.empty((len(detected), img_h, img_w, 3))
	    
	    preprocessed_faces_emo = []
	    if len(detected) > 0:
	        for i, d in enumerate(detected):
	            x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
	            xw1 = max(int(x1 - margin * w), 0)
	            yw1 = max(int(y1 - margin * h), 0)
	            xw2 = min(int(x2 + margin * w), img_w - 1)
	            yw2 = min(int(y2 + margin * h), img_h - 1)
	            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
	            # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
	            #faces[i, :, :, :] = cv2.resize(frame[yw1:yw2 + 1, xw1:xw2 + 1, :], (img_size, img_size))
	            face =  frame[yw1:yw2 + 1, xw1:xw2 + 1, :]
	            temp_face=face
	            face = cv2.resize(face, (224,224), interpolation = cv2.INTER_AREA)
	            face = face.astype("float") / 255.0
	            face = img_to_array(face)
	            face = np.expand_dims(face, axis=0)
	            preprocessed_faces.append(face)
	           # print(preprocessed_faces)
	       
	        
	        face_labels = []
	        
	        for i, d in enumerate(detected):
	            preds = Project7Sem.predict(preprocessed_faces[i])[0]
	            #print(type(preds))
	           # count = len([i for i in preds if i > 0.3]) 
	        #0.3 is good
	        
	            if (max(preds))>0.60:
	                #print(preds.argmax())
	                #print(face_classes[preds.argmax()])
	                face_labels.append(face_classes[preds.argmax()])
	                
	                if face_classes[preds.argmax()]  not in temp:
	                                temp.append(face_classes[preds.argmax()])
	            else:
	                #print(count)
	#                 date_time = datetime.now()
	#                 d = date_time.strftime("%Y%m%d%H%M%S")
	#                 outpath='D:/unknown_pics/'+d+'.jpg'
	                #t=t+1
	#                 cv2.imwrite(outpath,temp_face)
	                face_labels.append('unknown')
	        # draw results
	        for i, d in enumerate(detected):
	            label = "{}".format(face_labels[i])
	            draw_label(frame, (d.left(), d.top()), label)
	   
	        
	    cv2.imshow("face recognition", frame)
	    if cv2.waitKey(1) == 13: #13 is the Enter Key
	        break

	cap.release()
	cv2.destroyAllWindows()  

	return redirect('/')   




#######

# def home(request):
# 	return render(request,'faceapp/home.html',{})
