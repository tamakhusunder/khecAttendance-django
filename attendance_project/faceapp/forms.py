# from django.core import valiators
from django import forms
from .models import StaffInfo


class StaffInfoForm(forms.ModelForm):
	class Meta:
		model=StaffInfo
		fields=['name','image','code','department','desgination','specialization','email','contact','address']
		labels={'image':'Profile image*'}
		widgets={
				'name':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Full Name",
											'name': 'inputFullName',
											'tabindex': "3",
											'data-error': "password is required"}),
				'code':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Roll no.",
                                           	'name': 'inputCodeNo'}),
				'department':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Department",
                                           	'name': 'inputDepartment'}),
				'desgination':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Desgination",
                                           	'name': 'inputDepartment'}),
				'specialization':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Specialization",
                                           	'name': 'inputSpecialization'}),
				'email':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter email address",
                                           	'name': 'inputEmailAddress',
                                           	'aria-describedby':'emailHelp'}),
				'contact':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Contact no.",
                                           	'name': 'inputContactNo'}),
				'address':forms.TextInput(attrs={'class':'form-control',
											'placeholder':"Enter Address",
                                           	'name': 'inputAddress'})
	}