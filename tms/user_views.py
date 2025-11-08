from django.shortcuts import render, redirect
from tms.forms import *

def insertTicket(request):
    form = SupportTicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save(commit = False)
            ticket.created_by = request.user
            ticket.status = 'open'
            ticket.save()
            return redirect(userDashboard)
    return render(request, 'user/insertTickets.html', {'form':form})

def userDashboard(request):
    count = {
        "open_ticket" : TicketSupport.objects.filter(status = 'open', created_by = request.user).count(),
        "close_ticket" : TicketSupport.objects.filter(status = 'closed', created_by = request.user).count(),

    }
    return render(request, 'user/userdashboard.html', count)