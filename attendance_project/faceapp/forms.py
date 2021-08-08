# from django.core import valiators
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile,Holiday

# To validate phone number in form
def validate_mobile(value):
	firstTwoDigit=int(str(value)[:2])
	if (len(str(value)) != 10 or firstTwoDigit != 98):
		raise ValidationError(
			_('%(value)s is not an valid number'),
            params={'value': value},
        )

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

class ProfileForm(forms.ModelForm):
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

class HolidayForm(forms.ModelForm):
	class Meta:
		model=Holiday
		fields=['weekend', 'date','image','active']
		widgets={
				'image':forms.FileInput(attrs={'class':'form-control',
                                           	'name': 'inputImage'}),
				'active':forms.CheckboxInput(attrs={'class':'form-control',
                                           	'name': 'inputActive'}),
				'weekend':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter weekend",
											'name': 'inputWeek',
											'tabindex': "3",
											'data-error': "password is required"}),
				'date':forms.DateInput(attrs={'class':'form-control',
											'placeholder':"Enter date",
											'name': 'inputDate'})
				}


class LeaveForm(forms.Form):
	leaveType = forms.CharField(label='Leave Type')
	startDate = forms.DateField(label='Start Date', error_messages={'required':'Enter Date'})
	endDate = forms.DateField(label='End Date', error_messages={'required':'Enter Date'})
	reason = forms.CharField(max_length=225, widget=forms.Textarea)
	halfday = forms.BooleanField(label='Half Day', initial=False, required=False)

# class HolidayForm(forms.Form):
# 	weekend = forms.CharField(label='Weekend Holiday')
# 	date = forms.DateField(label='Start Date', error_messages={'required':'Enter Date'})


class TimeSettingForm(forms.Form):
	entryTime = forms.TimeField(label='Entry Time')
	exitTime = forms.TimeField(label='Entry Time')
	toleranceTime = forms.IntegerField(label='Tolerance time in minutes')
	reason = forms.CharField(max_length=225, widget=forms.Textarea)
