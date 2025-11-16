from django.shortcuts import render, redirect, get_object_or_404
from tms.forms import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        if request.user.role == 'staff':
            logout(request)
    return render(request, 'home.html')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, "register.html", {"form":form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user = request.user
            if user.role == 'staff':
                return redirect('staffdashboard')
            
           
            else:
                return redirect('homepage')
    return render(request, 'login.html')


    
def user_logout(request):
    logout(request)
    return redirect('homepage')

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
            if request.user.role == 'staff' or request.user.is_superuser:
                if ticket.assigned_to is None:
                    ticket.assigned_to = request.user
                if ticket.status != 'in_progress':
                    ticket.status = 'in_progress'
                ticket.save()
            return redirect('replycomment', id=ticket.id)
    return render(request, 'user/ticketdetail.html', {'ticket':ticket, 'replies':replies, 'form':form})