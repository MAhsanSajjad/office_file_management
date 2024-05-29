from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as dj_login
from django.http import  HttpResponseRedirect
from user_app.forms import LoginForm 
from .forms import SignUpForm
import datetime
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import  Q


def index(request):
    custom_message = ''

    form = SignUpForm()
    # email = request.POST.get('email')
    # check_user = User.objects.filter(email=email).first()
    # if check_user:
    #     custom_message = 'This Email has already an account!'

    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=True)
            return redirect('/user-login')
        else:
            # Check if the email error occurred
            if 'email' in form.errors:
                custom_message = 'This Email has already an account!'
            else:
                custom_message = 'Password weak or did not match'
            # Render the form with errors
            form = SignUpForm(request.POST)
    else:
        form = SignUpForm()
    print('*******************', custom_message)

    context ={
        'custom_message':custom_message,
        'form':form
    }
    return render(request, 'adminpanel/registration.html', context)




def user_login(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            if user.is_active:
                dj_login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                form = LoginForm(request.POST or None)
    context={
        'form':form,
    }
    return render(request, 'adminpanel/login.html', context)

def upload_file(request):
    return render(request,'adminpanel/upload_file.html')

def dashboard(request):
    today = datetime.datetime.now()
    current_month = today.month
    current_year = date.today().year
    month_list = ['Jan', 'Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    user_list = []
    active_user_list = []
    inactive_user_list = []

    for m in range(current_month):
        months = m+1
        total_user_graph = User.objects.filter(
                                        date_joined__month=months, 
                                        date_joined__year=current_year)
        total_active_user_graph = User.objects.filter(
                                        is_active=True,
                                        date_joined__month=months, 
                                        date_joined__year=current_year)
        total_inactive_user_graph = User.objects.filter(
                                        is_active=False,
                                        date_joined__month=months, 
                                        date_joined__year=current_year)
        user_list.append(total_user_graph)
        active_user_list.append(total_active_user_graph)
        inactive_user_list.append(total_inactive_user_graph)

    total_profile = User.objects.filter(is_staff=False).count()
    total_active_user = User.objects.filter(is_active=True, is_staff=False).count()
    total_inactive_user = User.objects.filter(is_active=False, is_staff=False).count()
    context ={
        'month_list': month_list,
        'user_list': user_list,
        'active_user_list': active_user_list,
        'inactive_user_list': inactive_user_list,
        'total_profile': total_profile, 
        'total_active_user': total_active_user, 
        'total_inactive_user': total_inactive_user, 


    }

    return render(request,'adminpanel/dashboard.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/user-login')


# admin view all Profiles
@login_required(login_url='admin_panel_login')
def admin_panel_view_users(request):   
    all_profiles = User.objects.filter(is_staff=False).order_by('-date_joined')
    paginator = Paginator(all_profiles, 50)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)
    context = {
        'profiles': profiles,
    }
    return render(request, 'adminpanel/total_user.html', context)

# admin search user
@login_required(login_url='admin_panel_login')
def admin_panel_search_user(request):
    get_first_name = request.GET.get('first_name')
    get_last_name= request.GET.get('last_name')
    get_username = request.GET.get('username')
    get_email = request.GET.get('email')
    gender = request.GET.get('gender')
    all_profiles = None

    if get_first_name:
        first_name = get_first_name.strip()
    else:
        first_name = ''
    if get_last_name:
        last_name = get_last_name.strip()
    else:
        last_name = ''
    if get_username:
        username = get_username.strip()
    else:
        username = ''
    if get_email:
        email = get_email.strip()
    else:
        email = ''
    
    if gender and not email:
        all_profiles = User.objects.filter(
                                Q(first_name__icontains = first_name)&
                                Q(last_name__icontains = last_name)&
                                Q(username__icontains = username),
                                is_staff=False
                                )
    elif email and not gender:
        all_profiles = User.objects.filter(
                                Q(first_name__icontains = first_name)&
                                Q(last_name__icontains = last_name)&
                                Q(username__icontains = username)&
                                Q(email__iexact = email),
                                is_staff=False
                                )
    elif gender or email:
        all_profiles = User.objects.filter(
                                Q(gender=gender)&
                                Q(first_name__icontains = first_name)&
                                Q(last_name__icontains = last_name)&
                                Q(username__icontains = username)&
                                Q(email__iexact = email),
                                is_staff=False
                                )
    else:
        all_profiles = User.objects.filter(
                                Q(first_name__icontains = first_name)&
                                Q(last_name__icontains = last_name)&
                                Q(username__icontains = username),
                                is_staff=False
                                )
    paginator = Paginator(all_profiles, 20)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)
    context = {
        'profiles': profiles,
    }
    return render(request, 'adminpanel/search_user.html', context)

# admin delete user
@login_required(login_url='admin_panel_login')
def admin_panel_delete_user(request):
    if request.method == 'POST':
        id = request.POST.get('aid')
        profile1 = User.objects.get(pk=id)
        profile1.delete()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False})

# admin block user
@login_required(login_url='admin_panel_login')
def admin_panel_block_user(request):
    if request.method == 'POST':
        id = request.POST.get('aid')
        profile1 = User.objects.get(pk=id)
        if profile1.is_active == False:
            profile1.is_active = True
            profile1.save()
        else:
            profile1.is_active = False
            profile1.save()

        return JsonResponse({'status': True})
    return JsonResponse({'status': False})


# admin view active user
@login_required(login_url='admin_panel_login')
def admin_panel_view_active_user(request):
    all_profiles = User.objects.filter(is_active=True, is_staff=False).order_by('-date_joined')
    paginator = Paginator(all_profiles, 50)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    context={
        'users':users,
    }
    return render(request, 'adminpanel/total_active_user.html', context)

# admin search  active user
@login_required(login_url='admin_panel_login')
def admin_panel_search_active_user(request):
    get_first_name = request.GET.get('first_name')
    get_last_name = request.GET.get('last_name')
    get_username = request.GET.get('username')
    gender = request.GET.get('gender')
    first_name = get_first_name.strip()
    last_name = get_last_name.strip()
    username = get_username.strip()
    if not first_name:
        first_name = ''
    if not last_name:
        last_name = ''
    if not username:
        username = ''
    if not gender:
        gender = ''
    if gender:
        all_profiles = User.objects.filter(
                            is_active = True, is_staff=False)
        paginator = Paginator(all_profiles, 20)
        page_number = request.GET.get('page')
        users = paginator.get_page(page_number)
    else:
        all_profiles=User.objects.filter(
                            Q(first_name__icontains = first_name) &
                            Q(last_name__icontains = last_name)&
                            Q(username__icontains = username), is_active=True, is_staff=False)
        paginator = Paginator(all_profiles, 20)
        page_number = request.GET.get('page')
        users = paginator.get_page(page_number)
    context = {
        'users': users,
    }
    return render(request, 'adminpanel/search_active_user.html', context)

# admin delete active user
@login_required(login_url='admin_panel_login')
def admin_panel_delete_active_user(request):
    if request.method == 'POST':
        id = request.POST.get('aid')
        profile1 = User.objects.get(pk=id)
        profile1.deleted()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False})

# admin view inactive user
@login_required(login_url='admin_panel_login')
def admin_panel_view_inactive_user(request):
    all_users = User.objects.filter(is_active=False, is_staff=False)
    paginator = Paginator(all_users, 50)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    context={
        'users':users,
    }
    return render(request, 'adminpanel/total_inactive_user.html', context)

# admin search inactive user
@login_required(login_url='admin_panel_login')
def admin_panel_search_inactive_user(request):
    get_first_name = request.GET.get('first_name')
    get_last_name = request.GET.get('last_name')
    get_username = request.GET.get('username')
    first_name = get_first_name.strip()
    last_name = get_last_name.strip()
    username = get_username.strip()
    if not first_name:
        first_name = ''
    if not last_name:
        last_name = ''
    if not username:
        username = ''
    all_profiles = User.objects.filter(
                        Q(first_name__icontains=first_name) &
                        Q(last_name__icontains=last_name)&
                        Q(username__icontains=username)
                        , is_active=False, is_staff=False)
    paginator = Paginator(all_profiles, 20)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    context = {
        'users': users,
    }
    return render(request, 'adminpanel/search_inactive_user.html', context)

