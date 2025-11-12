from django.shortcuts import render, redirect, get_object_or_404
from tms.models import *
from tms.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test

# def is_superadmin_or_staff(user):
#     return user.is_authenticated and (user.role in ['superadmin', 'staff'])

@login_required
# @user_passes_test(is_superadmin_or_staff, login_url='/homepage/')
def dashboard(request):
    count = {
        "users" : User.objects.count(),
        "tickets" : TicketSupport.objects.count(),
        "replay" : CommentTicket.objects.count(),
        "agents" : User.objects.filter(role = "staff").count(),
        "resloved_tickets" : TicketSupport.objects.filter(status = "closed").count()
    }

    return render(request, 'admin/dashboard.html', {'count':count})

@login_required
#@user_passes_test(is_admin_or_staff, login_url='/homepage/')
def manage_user(request):
    users = User.objects.filter(is_superuser = False)
    
    return render(request, 'admin/manageUsers.html', {'users': users})

# all ticket manage 
@login_required
#@user_passes_test(is_admin_or_staff, login_url='/homepage/')
def manage_tickets(request):
    tickets = TicketSupport.objects.filter(status= 'open')
    assigned_ticket = TicketSupport.objects.filter(assigned_to= request.user, status = 'in_progress')
    return render(request, "admin/manageTickets.html", {'tickets':tickets, 'assigned_ticket':assigned_ticket})


@login_required
#@user_passes_test(is_admin_or_staff, login_url='/homepage/')
def manage_agents(request):
    users = User.objects.all()
    return render(request, "admin/manageAgent.html",{'users':users})

def delete_user(request, id):
    item = User.objects.get(id=id)
    item.delete()
    return redirect('manageuser')


@login_required
#@user_passes_test(is_admin_or_staff, login_url='/homepage/')
def manage_reports(request):
    return render(request, "admin/reports.html")

#ticket status change logic
@login_required
#@user_passes_test(is_admin_or_staff, login_url='/homepage/')
def change_status(request, id):
    ticket = TicketSupport.objects.get(id=id)
    ticket.status = 'closed'
    ticket.save()
    return redirect('manageticket')

#ticket delete reply
@login_required
#@user_passes_test(is_admin_or_staff, login_url='/homepage/')
def deleteTicket(request, id):
    item = get_object_or_404(TicketSupport, id=id)
    item.delete()
    return redirect('manageticket')

#ticket reply logic
@login_required
#@user_passes_test(is_superadmin_or_staff, login_url='/homepage/')
def ticketReply(request, ticket_id):
    ticket = get_object_or_404(TicketSupport, id=ticket_id)
    replies = ticket.comments.all().order_by('created_at')
    form = TicketCommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.author = request.user
            reply.save()
            ticket.status = 'in_progress'
            ticket.assigned_to = request.user
            ticket.save()
            return redirect('ticketreply', ticket_id=ticket.id)
    
    return render(request, 'admin/ticketreply.html',{'ticket':ticket,'replies':replies, 'form':form})