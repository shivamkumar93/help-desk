from django.shortcuts import render, redirect
from tms.models import *
from tms.forms import *
def dashboard(request):
    count = {
        "users" : User.objects.count(),
        "tickets" : TicketSupport.objects.count(),
        "replay" : CommentTicket.objects.count(),
        "agents" : User.objects.filter(role = "admin").count(),
        "resloved_tickets" : TicketSupport.objects.filter(status = "closed").count()
    }

    return render(request, 'admin/dashboard.html', {'count':count})

def manage_user(request):
    users = User.objects.filter(is_superuser = False)
    
    return render(request, 'admin/manageUsers.html', {'users': users})

def manage_tickets(request):
    tickets = TicketSupport.objects.all()
    return render(request, "admin/manageTickets.html", {'tickets':tickets})



def manage_agents(request):
    return render(request, "admin/manageAgent.html")

def manage_reports(request):
    return render(request, "admin/reports.html")

def change_status(request, id):
    ticket = TicketSupport.objects.get(id=id)
    ticket.status = 'closed'
    ticket.save()
    return redirect('manageticket')