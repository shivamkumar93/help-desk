from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    email = forms.EmailField(required=True)


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
    

class SupportTicketForm(ModelForm):
    class Meta:
        model = TicketSupport
        fields = ['title','department','description', 'image']

class TicketCommentForm(ModelForm):
    class Meta:
        model = CommentTicket
        fields = ['comment']

# class TicketAttachmentForm(ModelForm):
#     class Meta:
#         model = AttachmentTicket
#         fields = '__all__'