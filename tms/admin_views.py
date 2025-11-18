from django.shortcuts import render, redirect, get_object_or_404
from tms.models import *
from tms.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm

def is_superadmin(user):
    return user.is_authenticated and user.is_superuser  # ya user.role == 'superadmin'

# Apply decorator to view
@user_passes_test(is_superadmin, login_url='/homepage/',)
def dashboard(request):
    count = {
        "users" : CustomUser.objects.count(),
        "tickets" : TicketSupport.objects.count(),
        "replay" : CommentTicket.objects.count(),
        "agents" : CustomUser.objects.filter(role = "staff").count(),
        "resloved_tickets" : TicketSupport.objects.filter(status = "closed").count()
    }

    return render(request, 'admin/dashboard.html', {'count':count})

@login_required
@user_passes_test(is_superadmin, login_url='/homepage/',)

def manage_user(request):
    users = CustomUser.objects.filter(role = 'user')
    return render(request, 'admin/manageUsers.html', {'users': users})

# all ticket manage 
@login_required
@user_passes_test(is_superadmin, login_url='/homepage/',)
def manage_tickets(request):
    tickets = TicketSupport.objects.filter(status='open')
    assigned_ticket = TicketSupport.objects.filter(status='in_progress')
    closed_ticket = TicketSupport.objects.filter(status='closed')
    return render(request, "admin/manageTickets.html", {'tickets':tickets, "assigned_ticket":assigned_ticket, "closed_ticket":closed_ticket})


@login_required
# manage all staff
@user_passes_test(is_superadmin, login_url='/homepage/',)
def manage_agents(request):
    users = CustomUser.objects.filter(role='staff')
    return render(request, "admin/manageAgent.html",{'users':users})

# delete users
def delete_user(request, id):
    item = CustomUser.objects.get(id=id)
    item.delete()
    return redirect('manageuser')


@login_required
@user_passes_test(is_superadmin, login_url='/homepage/',)
def manage_reports(request):
    return render(request, "admin/reports.html")

#ticket status change logic
@login_required
@user_passes_test(is_superadmin, login_url='/homepage/',)
def change_status(request, id):
    ticket = TicketSupport.objects.get(id=id)
    ticket.status = 'closed'
    ticket.save()
    return redirect('manageticket')

#ticket delete reply
@login_required
@user_passes_test(is_superadmin, login_url='/homepage/',)
def deleteTicket(request, id):
    item = get_object_or_404(TicketSupport, id=id)
    item.delete()
    return redirect('manageticket')

#ticket reply logic
@login_required
@user_passes_test(is_superadmin, login_url='/homepage/',)
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
            if request.user.role == 'staff' or request.user.is_superuser:
                if ticket.assigned_to is None:
                    ticket.assigned_to = request.user
                if ticket.status != 'in_progress':
                    ticket.status = 'in_progress'
                
                ticket.save()
            return redirect('ticketreply', ticket_id=ticket.id)
    
    return render(request, 'admin/ticketreply.html',{'ticket':ticket,'replies':replies, 'form':form})

@login_required
@user_passes_test(is_superadmin, login_url='/homepage/')
def assigned_ticket(request, ticket_id):
    ticket = get_object_or_404(TicketSupport, id=ticket_id)
    form = AssignedTicketForm(request.POST or None, instance=ticket)

    form.fields['assigned_to'].queryset = CustomUser.objects.filter(role='staff')
    if request.method == 'POST':
        if form.is_valid():
            data = form.save(commit=False)
            data.status = 'in_progress'
            data.save()
            return redirect('manageticket')
    return render(request, 'admin/assignTicket.html',{'form':form})


# Create  Agent
@login_required
@user_passes_test(is_superadmin, login_url='/homepage/')
def create_agent(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'staff'
            user.save()
            return redirect('manageagent')
    return render(request, 'admin/createAgent.html', {'form':form})
