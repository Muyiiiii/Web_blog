from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(required=True, error_messages={'required': '请填写用户名'})
    pwd = forms.CharField(required=True, error_messages={'required': '请填写密码'})


class LoginForm(forms.Form):
    name = forms.CharField(required=True, error_messages={'required': '请填写用户名'})
    pwd = forms.CharField(required=True, error_messages={'required': '请填写密码'})


class SubmitForm(forms.Form):
    pic = forms.FileField(required=True, error_messages={'required': '请加入图片'})
    title = forms.CharField(required=True, error_messages={'required': '请填写主题'})
    content = forms.CharField(required=True, error_messages={'required': '请填写主要内容'})
    kind = forms.CharField(required=True, error_messages={'required': '请填写类别'})


class MoreInfoForm(forms.Form):
    pic = forms.FileField(required=True, error_messages={'required': '请加入头像'})
    email = forms.CharField(required=True, error_messages={'required': '请填写邮箱'})


class ContactForm(forms.Form):
    real_name = forms.FileField(required=True, error_messages={'required': '请加入您的姓名'})
    email = forms.CharField(required=True, error_messages={'required': '请填写您的邮箱'})
    phone_number = forms.CharField(required=True, error_messages={'required': '请填写您的手机号'})
    subject = forms.CharField(required=True, error_messages={'required': '请填写主题'})
    content = forms.CharField(required=True, error_messages={'required': '请填写主要内容'})
