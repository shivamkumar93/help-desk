from django.shortcuts import render, redirect, get_object_or_404
from tms.models import *
from tms.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from tms.decorators import *



# Apply decorator to view
@login_required
@role_required(allowed_roles=['superadmin'])
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
@role_required(allowed_roles=['superadmin'])
def manage_user(request):
    users = CustomUser.objects.filter(role = 'user')
    return render(request, 'admin/manageUsers.html', {'users': users})

# all ticket manage 
@login_required
@role_required(allowed_roles=['superadmin'])
def manage_tickets(request):
    tickets = TicketSupport.objects.filter(status='open')
    assigned_ticket = TicketSupport.objects.filter(status='in_progress')
    closed_ticket = TicketSupport.objects.filter(status='closed')
    return render(request, "admin/manageTickets.html", {'tickets':tickets, "assigned_ticket":assigned_ticket, "closed_ticket":closed_ticket})


# manage all staff
@login_required
@role_required(allowed_roles=['superadmin'])
def manage_agents(request):
    users = CustomUser.objects.filter(role='staff')
    return render(request, "admin/manageAgent.html",{'users':users})

# delete users
@login_required
@role_required(allowed_roles=['superadmin'])
def delete_user(request, id):
    item = CustomUser.objects.get(id=id)
    item.delete()
    return redirect('manageuser')


@login_required
@role_required(allowed_roles=['superadmin'])
def manage_reports(request):
    return render(request, "admin/reports.html")

#ticket status change logic
@login_required
@role_required(allowed_roles=['superadmin'])
def change_status(request, id):
    ticket = TicketSupport.objects.get(id=id)
    ticket.status = 'closed'
    ticket.save()
    return redirect('manageticket')

#ticket delete reply
@login_required
@role_required(allowed_roles=['superadmin'])
def deleteTicket(request, id):
    item = get_object_or_404(TicketSupport, id=id)
    item.delete()
    return redirect('manageticket')

#ticket reply logic
@login_required
@role_required(allowed_roles=['superadmin'])

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
@role_required(allowed_roles=['superadmin'])
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
@role_required(allowed_roles=['superadmin'])
def create_agent(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'staff'
            user.save()
            return redirect('manageagent')
    return render(request, 'admin/createAgent.html', {'form':form})


#view staff details with all ticketreply
@login_required
@role_required(allowed_roles=['superadmin'])
def view_Staffdetails(request, ticket_id):
    staff = CustomUser.objects.get(id=ticket_id)
    contex = {
            "staff":staff,
            "assigned_ticket" : TicketSupport.objects.filter(assigned_to = staff, status = 'in_progress'),
            "closed_ticket" : TicketSupport.objects.filter(assigned_to = staff, status = 'closed')
    }
    return render(request, 'admin/viewstaffdetail.html', contex)


#view user detail with all ticket
@login_required
@role_required(allowed_roles=['superadmin'])
def view_Userdetails(request, ticket_id):
    customer = CustomUser.objects.get(id=ticket_id)
    context = {
        "customer":customer,
        "tickets" : TicketSupport.objects.filter(created_by=customer)
    }
    return render(request, 'admin/viewuserdetail.html', context)