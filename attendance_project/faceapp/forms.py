# from django.core import valiators
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.utils.translation import gettext, gettext_lazy as _


from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
from .models import Profile,Holiday

# To validate phone number in form
def validate_mobile(value):
	firstTwoDigit=int(str(value)[:2])
	if (len(str(value)) != 10 or firstTwoDigit != 98):
		raise ValidationError(
			_('%(value)s is not an valid number'),
            params={'value': value},
        )

GENDER_CHOICES =(
    ("Male", "Male"),
    ("Female", "Female"),
)

WEEK_CHOICES =(
    ("Sunday", "Sunday"),
    ("Monday", "Female"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)

STATE_CHOICES =(
    ("Province No. 1", "Province No. 1"),
    ("Province No. 2", "Province No. 2"),
    ("Bagmati Province", "Bagmati Province"),
    ("Gandaki Province", "Gandaki Province"),
    ("Lumbini Province", "Lumbini Province"),
    ("Sudurpashchim Province", "Sudurpashchim Province"),
    ("Karnali Province", "Karnali Province"),
)

YEARS = [x for x in range(1921,2021)]

''' django login authentication form and we used here for adding bootstrap'''
class LoginForm(AuthenticationForm):
	username=UsernameField(label=_("Employee Id / Username"),widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control', 'placeholder':"Enter Username",}))
	password=forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control', 'placeholder':"Enter Password",}))

# class UserForm(forms.ModelForm):
# 	class Meta:
# 		model = User
# 		fields = ('username',)
# 		widgets={
# 				'username':forms.TextInput(attrs={'class':'form-control'})
# 		}

class UserForm(UserCreationForm):
	username = forms.CharField(label='Employee code', min_length=5, max_length=150, widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control', 'placeholder':"Enter code",}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control', 'placeholder':"Enter Password",}))
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control', 'placeholder':"Confirm password again",}))

	class Meta:
		model=User
		fields=['username']

	def username_clean(self):
		username = self.cleaned_data['username'].lower()
		new = User.objects.filter(username = username)
		if new.count():
			raise ValidationError("User Already Exist")
		return username  

widget=forms.SelectDateWidget(years=YEARS)
class ProfileForm(forms.ModelForm):
	contact = forms.IntegerField(validators=[validate_mobile], widget=forms.NumberInput(attrs={'autofocus':True,'class':'form-control', 'placeholder':"Enter Mobile Number",}))
	gender = forms.ChoiceField(choices = GENDER_CHOICES, widget=forms.Select(attrs={'autofocus':True,'class':'form-control',}))
	dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS,attrs={'autofocus':True,'class':'form-control',}))
	dateOfJoin = forms.DateField(widget=forms.SelectDateWidget(years=YEARS,attrs={'autofocus':True,'class':'form-control',}))
	state = forms.ChoiceField(choices = STATE_CHOICES, widget=forms.Select(attrs={'autofocus':True,'class':'form-control',}))

	class Meta:
		model=Profile
		fields=['name','image','department','desgination','specialization','email','contact','address','active','dob','gender','dateOfJoin','city','state','startYear','endYear','university','college']
		labels={'image':'Profile image*'}
		widgets={
				'image':forms.FileInput(attrs={'required': True,
											'class':'form-control',
                                           	'name': 'inputImage'}),
				'name':forms.TextInput(attrs={'class':'form-control',
											'required': True,
											'placeholder':"Enter Full Name",
											'name': 'inputFullName',
											'tabindex': "3",
											'data-error': "password is required"}),
				'department':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Department",
                                           	'name': 'inputDepartment'}),
				'desgination':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Desgination",
                                           	'name': 'inputDepartment'}),
				'specialization':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Specialization",
                                           	'name': 'inputSpecialization'}),
				'email':forms.EmailInput(attrs={'class':'form-control',
											'placeholder':"Enter email address",
                                           	'name': 'inputEmailAddress',
                                           	'aria-describedby':'emailHelp'}),
				'contact':forms.NumberInput(attrs={'class':'form-control',
											'placeholder':"Enter Contact no.",
                                           	'name': 'inputContactNo'}),
				'address':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Address",
                                           	'name': 'inputAddress'}),
				'active':forms.CheckboxInput(attrs={'class':'form-control',
                                           	'name': 'inputActive'}),
				'dob':forms.DateInput(attrs={'class':'form-control',
											'placeholder':"YYYY-MM-DD",
                                           	'name': 'inputDob'}),
				'gender':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter gender",
                                           	'name': 'inputGender'}),
				'dateOfJoin':forms.DateInput(attrs={'class':'form-control',
											'placeholder':"YYYY-MM-DD",
                                           	'name': 'inputDateJoin'}),
				'city':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter city.",
                                           	'name': 'inputCity'}),
				'state':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter state",
                                           	'name': 'inputState'}),
				'startYear':forms.NumberInput(attrs={'class':'form-control',
											'placeholder':"Enter start Year of college",
                                           	'name': 'inputStartYear'}),
				'endYear':forms.NumberInput(attrs={'class':'form-control',
											'placeholder':"Enter end Year of college",
                                           	'name': 'inputEndYear'}),
				'university':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter university",
                                           	'name': 'inputUniversity'}),
				'college':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter College",
                                           	'name': 'inputCollege'})
	}

class TimeSettingForm(forms.Form):
	entryTime = forms.TimeField(label='Entry Time',widget=forms.TimeInput(attrs={'type': 'time','class':'form-control',}))
	exitTime = forms.TimeField(label='Exit Time',widget=forms.TimeInput(attrs={'type': 'time','class':'form-control',}))
	tolerance = forms.IntegerField(label='Tolerance time in minutes',widget=forms.NumberInput(attrs={'autofocus':True,'class':'form-control', 'placeholder':"Enter in minutes",}))


YEARS2 = [x for x in range(2021,2099)]

class HolidayForm(forms.Form):
	weekend = forms.ChoiceField(choices = WEEK_CHOICES, widget=forms.Select(attrs={'autofocus':True,'class':'form-control',}))
	date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS2,attrs={'autofocus':True,'class':'form-control',}))
	


class LeaveForm(forms.Form):
	leaveType = forms.CharField(label='Leave Type')
	startDate = forms.DateField(label='Start Date', error_messages={'required':'Enter Date'})
	endDate = forms.DateField(label='End Date', error_messages={'required':'Enter Date'})
	reason = forms.CharField(max_length=225, widget=forms.Textarea)
	halfday = forms.BooleanField(label='Half Day', initial=False, required=False)

# class HolidayForm(forms.Form):
# 	weekend = forms.CharField(label='Weekend Holiday')
# 	date = forms.DateField(label='Start Date', error_messages={'required':'Enter Date'})




# YEARS= [x for x in range(2010,2021)]
BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']

# form for year and month in search
class YearForm(forms.Form):
    birth_date= forms.DateField(label='Select Date',
    							widget=forms.SelectDateWidget(years=YEARS)
    							)


class SendEmail(forms.Form):
	subject = forms.CharField(label='Suject', max_length=150, widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control', 'placeholder':"Enter subject",}))
	message = forms.CharField(label='message', widget=forms.Textarea(attrs={'class':'form-control',}))
	




