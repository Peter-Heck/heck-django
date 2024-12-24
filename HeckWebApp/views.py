from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.views import PasswordResetView
from .forms import PostForm, ProfileName, ProfileImage, ProfileBio
from django.contrib.auth.models import User as DjangoUser
from .models import Post, UserProfile
from datetime import datetime
from django.utils.timezone import localtime
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# Profile_count is used to keep the profile name unique
profile_count = 0

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            global profile_count
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            profile_name = 'unknown' + str(profile_count)
            profile_count = profile_count + 1
            user_profile = UserProfile.objects.create(user=user, name=profile_name, bio='')
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})
        

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', 'default')
        password = request.POST.get('password', 'default')
        # print(username)
        # print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"
            return render(request, 'accounts/login.html', {'error':error_message})
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('index')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')

# This is the home page
def index(request):
    users = UserProfile.objects.all()
    posts = _load_posts(request)
    # Post.objects.all()
    context = {
        'users': users,
        'posts': posts,
    }
    
    return render(request, 'home/index.html', context)

# This is the page view to edit your profile as well as make a post
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        uid = request.user.id
        profile = UserProfile.objects.get(user_id=uid)
        posts = _load_posts_protected(request)
        context = {
            'profile': profile,
            'posts': posts
        }
        return render(request, 'registration/protected.html', context)

# This is the public profile view
def profile(request, name):
    user = UserProfile.objects.get(name=name)
    posts = _load_posts_profile(request, name)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'registration/profile.html', context)

# These next few functions are used to load more posts on each view needed
def _load_posts(request):
    page = request.GET.get("page")
    posts = Post.objects.all().order_by('-post_date')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts

def list_load_posts_view(request):
    posts = _load_posts(request)
    context = {"posts": posts,}
    return render(request, "posts.html", context)

def _load_posts_profile(request, name):
    page = request.GET.get("page")
    user = UserProfile.objects.get(name=name)
    user_id = user.user_id
    posts = Post.objects.filter(author_id=user_id).order_by('-post_date')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts

def _load_posts_protected(request):
    page = request.GET.get("page")
    uid = request.user.id
    profile = UserProfile.objects.get(user_id=uid)
    posts = Post.objects.filter(author_id=uid).order_by('-post_date')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts

# This is the view to make a post
@login_required
def make_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            time = datetime.now()
            title = form.cleaned_data.get('title')
            author = request.user
            user_id = author.id
            creator = UserProfile.objects.get(user_id=user_id)
            try:
                image = request.FILES['image']
            except:
                image = None
            body = form.cleaned_data.get('body')
            post_date = time
            updated_on = time
            post = Post.objects.create(author=author, title=title, body=body, image=image, post_date=post_date, updated_on=updated_on, creator=creator)
            # print(post)
            # images = request.POST.get('images')
            # print(images)
            # images_posted = PostImages.objects.create(post=post, image=images)
            # print(images_posted)
            form.save()
            return redirect('protected')
    else:
        form = PostForm()
    return render(request, 'registration/create_post.html', {'form': form})

@login_required
def edit_profile_name(request):
    if request.method == 'POST':
        uid = request.user.id
        instance = UserProfile.objects.get(user_id=uid)
        form = ProfileName(request.POST, instance=instance, initial={'name': 'instance'})
        if form.is_valid():
            form.save()
            return redirect('protected')
    else:
        form = ProfileName()
    return render(request, 'registration/edit_profile_name.html', {'form': form})

@login_required
def edit_profile_image(request):
    if request.method == 'POST':
        uid = request.user.id
        current_user = UserProfile.objects.get(user_id=uid)
        form = ProfileImage(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('protected')
    else:
        form = ProfileImage()
    return render(request, 'registration/edit_profile_image.html', {'form': form})

@login_required
def edit_profile_bio(request):
    uid = request.user.id
    current_user = UserProfile.objects.get(user_id=uid)
    if request.method == 'POST':
        uid = request.user.id
        current_user = UserProfile.objects.get(user_id=uid)
        form = ProfileBio(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('protected')
    else:
        form = ProfileBio(initial={'bio': current_user.bio})
    return render(request, 'registration/edit_profile_bio.html', {'form': form})

# This is the privacy policy view
def privacy(request):
    return render(request, 'privacy.html')