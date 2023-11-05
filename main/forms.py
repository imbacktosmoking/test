from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django import forms
from .models import Student, Post, Teacher
from django.contrib.auth.models import User


class Edit_Form(forms.ModelForm):
     class Meta:
        model = Post 
        fields = ( 'title', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }




class RegistrationForm(UserCreationForm):
    strand = forms.ChoiceField(choices=Student.STRAND_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    grade_level = forms.ChoiceField(choices=Student.GRADE_CHOICES,  widget=forms.Select(attrs={'class': 'form-control'}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password confirmation'
    )
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'strand', 'grade_level']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),  
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),  
            'strand': forms.Select(attrs={'class': 'form-control'}),
            'grade_level': forms.Select(attrs={'class': 'form-control'}),
        }




class PostForm(forms.ModelForm):
    def __init__(self, teacher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        teacher_instance = Teacher.objects.get(teacher=teacher)
        self.fields['subject'].queryset = teacher_instance.subjects.all()

    class Meta:
        model = Post 
        fields = ('subject', 'title', 'file', 'body')
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }



class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})) 
    username =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_superuser =  forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_staff =  forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_active =  forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    date_joined =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))



    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the fields you don't want to display
        del self.fields['last_login']
        del self.fields['is_superuser']
        del self.fields['is_staff']
        del self.fields['is_active']
        del self.fields['date_joined']
        del self.fields['password']



class PasswordChange(PasswordChangeForm):
   
    old_password =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})) 
    new_password1 =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})) 
    new_password2 =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})) 

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'password')