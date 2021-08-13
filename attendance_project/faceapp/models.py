from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
	"""database/table for staffs"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	name = models.CharField(max_length=255, blank=True)
	image = models.ImageField(upload_to='faceapp/images/staffs', blank=True, default='../static/faceapp/images/admin/defaultProfile.png')
	# code = models.CharField(primary_key=True, max_length=255, blank=True)
	department=models.CharField(max_length=255, blank=True)
	desgination = models.CharField(max_length=255, blank=True)
	specialization = models.CharField(max_length=255, blank=True)
	email = models.EmailField(max_length=255, blank=True)
	contact = models.BigIntegerField(null=True)
	address = models.CharField(max_length=255, blank=True)
	# role = models.CharField(max_length=255, default='staff')
	active = models.BooleanField(default=False)
	dob = models.DateTimeField(default=None,blank=True,null=True)
	gender = models.CharField(max_length=255, blank=True)
	dateOfJoin = models.DateTimeField(default=None,blank=True,null=True)
	city = models.CharField(max_length=255, blank=True)
	state = models.CharField(max_length=255, blank=True)
	startYear = models.IntegerField(null=True)
	endYear = models.IntegerField(null=True)
	university = models.CharField(max_length=255, blank=True)
	college = models.CharField(max_length=255, blank=True)
	createdDate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	updatedDate = models.DateTimeField(auto_now=True)

	# timestamp = models.DateField(auto_now_add=True,auto_now=False,blank=True)

	def __str__(self):
		# return self.name+'-->'+self.code+'-->'+self.department	#--> will be shown in database doesnot effect anything
		return f"Profile('{self.name}', '{self.email}', {self.department})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class AttendanceTb(models.Model):
	"""table for attendance from webcame"""
	# status_choices=[
	# 	('PRESENT','Present'),
	# 	('ABSENT','Absent'),
	# 	]
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date = models.DateField()
	time = models.TimeField()
	late_time = models.IntegerField(null=True)
	status = models.CharField(max_length=255,blank=True)
	# # attendanceCreated = models.DateField(auto_now_add=True,auto_now=True,blank=True)
	# createdDate = models.DateTimeField(auto_now_add=True,blank=True,null=True,default=None)
	# updatedDate = models.DateTimeField(auto_now=True,default=None)

	def __str__(self):
		return f"AttendanceTb('{self.user}', '{self.date}', '{self.time}', '{self.late_time}')"


class Leave(models.Model):
	userProfile = models.ForeignKey('Profile',on_delete=models.CASCADE)
	leaveType = models.CharField(max_length=255)
	startDate = models.DateField(auto_now=True)
	endDate = models.DateField(auto_now=True)
	reason = models.CharField(max_length=255)
	halfday = models.BooleanField()
	# createdDate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	# updatedDate = models.DateTimeField(auto_now=True)


	def __str__(self):
		return f"Leave('{self.userProfile}', '{self.leaveType}', '{self.reason}')"

class Holiday(models.Model):
	active = models.BooleanField(default=False)
	image = models.ImageField(upload_to='faceapp/images/staffs', blank=True)
	weekend = models.CharField(max_length=255)
	date = models.DateField()
	# createdDate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	# updatedDate = models.DateTimeField(auto_now=True)


	def __str__(self):
		return f"Holiday('{self.weekend}', '{self.date}')"

class TimeSetting(models.Model):
	entryTime = models.TimeField()
	exitTime = models.TimeField()
	tolerance = models.IntegerField(default=0,null=True)
	# createdDate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	# updatedDate = models.DateTimeField(auto_now=True)


	def __str__(self):
		return f"TimeSetting('{self.entryTime}', '{self.exitTime}')"
