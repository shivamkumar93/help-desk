from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from tms.models import *


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_welcome_email(sender, instance, created, **kwargs):
   # print(f"New user Created : {instance.username}")
    if created:
        subject = "welcome to helpdesk ticket management system!"
        message = f"Hi {instance.username}, thank you for registering at helpdesk ticket management system."
        from_email = "bcashivam11@gmail.com"
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        #print(f"welcome email sent successfully ")

@receiver(post_save, sender = TicketSupport)
def create_ticket_email(sender, instance, created, **kwargs):
    #print(f"send email successfully!..")
    if created:
        subject = "your ticket was created successfully!"
        #show ticket information in your email box 
        message = f""" Hello {instance.created_by.username}, Your ticket has been created successfully.
        Ticket Title: {instance.title}
        Description: {instance.description}
        Status: {instance.status}"""
        from_email = "bcashivam11@gmail.com"
        recipient_list = [instance.created_by.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)


