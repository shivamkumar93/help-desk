from django.shortcuts import render, redirect, get_object_or_404
from tms.forms import *
from tms.models import*

def staff_dashboard(request):
    count = {
        "open_ticket" : TicketSupport.objects.filter(status = 'open').count(),
        "close_ticket" : TicketSupport.objects.filter(status = 'closed').count(),
        "in_process" : TicketSupport.objects.filter(status = 'in_progress').count(),
        "tickets" : TicketSupport.objects.count(),
        "users" : CustomUser.objects.filter(role = 'staff').count()

    }
    return render(request, 'staff/staffdashboard.html', {'count':count})

def manage_staff(request):
    return render(request, 'staff/managestaff.html')

def managestaff_ticket(request):
    tickets = TicketSupport.objects.filter(status = 'open')
    assigned_ticket = TicketSupport.objects.filter(assigned_to= request.user, status = 'in_progress')

    return render(request, 'staff/ticketsmanage.html',{'tickets':tickets, 'assigned_ticket':assigned_ticket} )

def replyComment(request, id):
    ticket = get_object_or_404(TicketSupport, id=id)
    replies = ticket.comments.all().order_by('created_at')
    form = TicketCommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            
            if request.user.role == 'staff' or request.user.is_superuser:
                if ticket.assigned_to is None:
                    ticket.assigned_to = request.user
                if ticket.status != 'in_progress':
                    ticket.status = 'in_progress'
                ticket.save()
            return redirect('replycomment', id=ticket.id)
    return render(request, 'staff/replycomment.html', {'ticket':ticket, 'replies':replies, 'form':form})

def closed_ticket(request, id):
    ticket = TicketSupport.objects.get(id=id)
    ticket.status = 'closed'
    ticket.save()
    return redirect('staffticket')

