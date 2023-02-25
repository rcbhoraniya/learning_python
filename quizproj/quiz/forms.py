from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Max
from django.forms import formset_factory, BaseFormSet, inlineformset_factory
from .models import *
from django.contrib.auth.models import User


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course_name'].widget.attrs.update({'class': 'form-control','placeholder':'Course name'})

    class Meta:
        model = Course
        fields = ['course_name']

class ChapterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
        self.fields['course'].widget.attrs.update({'class': 'form-select'})
        self.fields['chapter_name'].widget.attrs.update({'class': 'form-control','placeholder':'Chapter name'})

    class Meta:
        model = Chapter
        fields = ['course','chapter_name']


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chapter'].queryset = Chapter.objects.filter(course=3)
        self.fields['chapter'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control','placeholder':'Question title'})
        self.fields['have_table'].widget.attrs.update({'class': "form-check"})
        self.fields['difficulty'].widget.attrs.update({'class': 'form-control','placeholder':'Difficulty'})
        self.fields['language'].widget.attrs.update({'class': 'form-select'})
        self.fields['question_pic'].widget.attrs.update({'class':'form-control','type':'file'})

    class Meta:
        model = Question
        fields = '__all__'
            # ['id','chapter','title','difficulty','language']

class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['question'].widget.attrs.update({'class': 'form-control'})
        self.fields['answer_text'].widget.attrs.update({'class': 'form-control','placeholder':'Answer option'})
        self.fields['is_right'].widget.attrs.update({'class': "form-check"})
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionTableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['column1'].widget.attrs.update({'class': 'form-control','placeholder':'column1'})
        self.fields['column2'].widget.attrs.update({'class': "form-control",'placeholder':'column2'})
        self.fields['column3'].widget.attrs.update({'class': 'form-control','placeholder':'column3'})

    class Meta:
        model = QuestionTable
        fields = '__all__'

QuestionTableFormset = inlineformset_factory(Question, QuestionTable, form=QuestionTableForm,fields=('column1','column2','column3',), extra=6,max_num=6,can_delete=False,can_order=True)

class QuestionAnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chapter'].queryset = Chapter.objects.filter(course=3)
        self.fields['chapter'].widget.attrs.update({'class': 'form-select'})
        self.fields['question_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['difficulty'].widget.attrs.update({'class': 'form-control'})
        self.fields['language'].widget.attrs.update({'class': 'form-select'})
        self.fields['option1'].widget.attrs.update({'class': 'form-control'})
        self.fields['option2'].widget.attrs.update({'class': 'form-control'})
        self.fields['option3'].widget.attrs.update({'class': 'form-control'})
        self.fields['option4'].widget.attrs.update({'class': 'form-control'})
        self.fields['answer'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = QuestionAnswer
        fields = '__all__'


# formset used to render multiple 'InvoiceItemForm'
# AnswerFormset = formset_factory(AnswerForm,extra=0)
AnswerFormset = inlineformset_factory(Question, Answer, form=AnswerForm,fields=('answer_text','is_right',), extra=4,max_num=4,can_delete=False,can_order=True)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control','placeholder':'Password'})

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder':'Conform Password'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': True,'placeholder':'email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'First name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder':'Last name'})

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email','first_name','last_name')
        widgets = {'password1': forms.PasswordInput(), 'password2': forms.PasswordInput(),
                   'email': forms.EmailInput()}

    # def save(self, commit=True):
    #     user = super(NewStudentForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control','placeholder':'Address.'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control','placeholder':'Mobile no.'})
        self.fields['profile_pic'].widget.attrs.update({'class':'form-control','type':'file','placeholder':'Photo'})
        self.fields['language'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Student
        fields = ['address', 'mobile', 'profile_pic','language']

class TeacherForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control','placeholder':'Address'})
        self.fields['mobile'].widget.attrs.update({'class': 'form-control','placeholder':'Mobile no.'})
        self.fields['salary'].widget.attrs.update({'class': 'form-control','placeholder':'Salary'})
        self.fields['status'].widget.attrs.update({'class': 'form-check'})
        self.fields['profile_pic'].widget.attrs.update({'class':'form-control','type':'file'})
        self.fields['language'].widget.attrs.update({'class': 'form-select'})

    class Meta:
        model = Teacher
        fields = ['address', 'mobile', 'profile_pic','status','salary','language']
