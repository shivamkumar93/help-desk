from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'superadmin'),
        ('user', 'user'),
        ('staff', 'staff'),
        
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

class TicketSupport(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=(('open','open'),('in_progress','in_progress'),('closed','closed')))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_ticket')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_ticket', blank=True, null=True)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    department = models.CharField(max_length=100, choices=(('support','support'),('technical','technical'),('sells','sells')), null=True, blank=True)

    def __str__(self):
        return self.title
    
class CommentTicket(models.Model):
    ticket = models.ForeignKey(TicketSupport, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class AttachmentTicket(models.Model):
    ticket = models.ForeignKey(TicketSupport, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='ticket_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
