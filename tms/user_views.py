from django.shortcuts import render, redirect, get_object_or_404
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
        "in_process" : TicketSupport.objects.filter(status = 'in_progress', created_by = request.user).count(),
        "tickets" : TicketSupport.objects.filter(created_by=request.user)

    }
    return render(request, 'user/userdashboard.html', count)

def ticketDetail(request, ticket_id):
    ticket = get_object_or_404(TicketSupport, id=ticket_id, created_by = request.user)
    replies = ticket.comments.all().order_by('created_at')
    form = TicketCommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.author = request.user
            reply.save()
            ticket.status = 'in_progress'
            ticket.save()
            return redirect(ticketDetail, ticket_id=ticket.id)

    return render(request, 'user/ticketdetail.html', {'ticket':ticket, 'replies':replies, 'form':form})