
from django.contrib import admin
from django.urls import path
from tms.views import *
from tms.admin_views import *
from tms.user_views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('register/', register , name='registerpage'),
    path('login', custom_login, name = 'login'),
    #path('after_login', after_login, name = 'loginrole'),
    path('logout', user_logout, name = 'logout'),

    # admin urls
    path('admindashboard/', dashboard, name='admindashboard'),
    path("admin-ticket/", manage_tickets, name='manageticket'),
    path("admin-assignticket/<int:ticket_id>/", assigned_ticket, name='assignticket'),
    path("admin-changeStatus/<int:id>/", change_status, name='changestatus'),
    path("admin-deleteTicket/<int:id>/", deleteTicket, name='deleteticket'),
    path("admin-user/", manage_user, name='manageuser'),
    path("admin-deleteuser/<int:id>/", delete_user, name='deleteuser'),
    path("admin-agent/", manage_agents, name='manageagent'),
    path("admin-createagent/", create_agent, name='createagent'),
    path("admin-reports/", manage_reports, name='managereport'),
    path("admin-ticketreply/<int:ticket_id>/", ticketReply, name='ticketreply'),

    # user panel 
    path("user-insertTicket/", insertTicket, name='insertTicket'),
    path("user-dashboard/", userDashboard, name='userdashboard'),
    path("user-ticketdetail/<int:ticket_id>/", ticketDetail, name='ticketdetail'),

    # Staff urls
    path('staff-dashboard/', staff_dashboard, name='staffdashboard'),
    path('staff-user/', manage_staff, name='managestaffuser'),
    path('staff-userticket/', managestaff_ticket, name='staffticket'),
    path('staff-replycomment<int:id>/', replyComment, name='replycomment'),
    path('staff-closedTicket<int:id>/', closed_ticket, name='closedticket'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
