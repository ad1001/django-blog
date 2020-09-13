from django.shortcuts import render
from .models import Story
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

#find active users
def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get("_auth_user_id"))
        print(data)
        print(user_id_list)
    users = list(User.objects.filter(id__in=user_id_list))
    sol = []
    users = list(map(str,users))
    return users

# find ip
def visitor_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#list view
def stories(request):
    context = {
        'stories': Story.objects.all()
    }
    return render(request,'stories.html',context)

# One specific page
@login_required(login_url='Login')
def story(request,pk):
    """
    how unique visitor works:
    requesting users ip is taken and saved in post if it is unique and count is updated
    how live counter works:
    all users with live session are checked. I have set active session to expire when browser closes via settings in blog. We check if the (previously) live users field of requested post are in having an active session if yes we let them be else pop them out. We add the current requesting user to list of live users and check length of the live users list. This length is currently live users for that post. 
    """
    active_users = get_current_users()
    ip = visitor_ip_address(request) 
    story = Story.objects.get(id=pk)
    if ip not in story.ips.split():
        story.ips = story.ips + ' ' + ip
        story.view_count += 1

    users_on_page = story.live_users.split()
    for user in users_on_page:
        if user in active_users:
            pass
        else:
            users_on_page.remove(user)
    if str(request.user) in users_on_page:
        pass
    else:
        users_on_page.append(str(request.user))
    live_count = len(users_on_page)
    users = ' '.join(users_on_page)
    story.live_users = users
    story.save()
    context= {'data': story,'live_count': live_count}
    return render(request,'story.html',context=context)

